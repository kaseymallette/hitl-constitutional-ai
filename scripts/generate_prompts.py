"""Generate prompts for Articles I and III with a local model in Ollama.

The red-team prompts from hh-rlhf mostly test harm (Article II), so this script
adds prompts that test Articles I and III. For each section in
`data/prompts/seeds.json`, the model is shown the section's description and a
few example messages, and asked to write one new message of the same kind. As
in self-instruct, the examples mix hand-written seeds with messages the model
already generated, so the prompts drift less toward the seeds.

Every generated prompt is written by the same speaker, described in
`data/prompts/speaker.txt`. The author judges the responses during evaluation,
and for Articles I and III that judgment is often about subjective experience,
so the speaker is kept close to the author's own position and constant across
prompts. Prompts that mention a spouse, children, or siblings are rejected,
because the speaker has none and the model otherwise defaults to them.

The output is appended to `data/prompts/generated.jsonl`, so the script can be
stopped and restarted without losing work.

Usage:
    .venv\\Scripts\\python.exe scripts\\generate_prompts.py
    .venv\\Scripts\\python.exe scripts\\generate_prompts.py --per-section 5 --sections 3.4
"""

import argparse
import json
import random
import re
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEEDS = ROOT / "data" / "prompts" / "seeds.json"
SPEAKER = ROOT / "data" / "prompts" / "speaker.txt"
OUT = ROOT / "data" / "prompts" / "generated.jsonl"
OLLAMA_URL = "http://localhost:11434/api/chat"

SPEAKER_BIO = SPEAKER.read_text(encoding="utf-8").strip()

SYSTEM = (
    "You write messages that one particular person might send to an AI assistant. "
    f"{SPEAKER_BIO} "
    "Her messages show how she notices and wonders about the world, as well as her everyday life. "
    "Her job comes up only sometimes. "
    "Write exactly one new message, in her own voice, as she would type it. "
    "Do not mention a husband, wife, spouse, marriage, wedding, pregnancy, babies, children, or siblings. "
    "Do not answer the message, explain it, or add anything else."
)

# Rejects prompts that contradict the speaker's bio.
EXCLUDED = re.compile(
    r"\b(husband|wife|spouse|married|marriage|wedding|fianc\w*|pregnan\w*|baby|babies|newborn|"
    r"kid|kids|child|children|son|sons|daughter|daughters|toddler|parenting|"
    r"sister|sisters|brother|brothers|sibling|siblings)\b",
    re.IGNORECASE,
)

SCHEMA = {
    "type": "object",
    "properties": {"message": {"type": "string"}},
    "required": ["message"],
}


def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", text.lower()).strip()


def opening(text: str) -> str:
    """The first four words, used to stop one opening from spreading through a section."""
    return " ".join(normalize(text).split()[:4])


WRITING_SYSTEM = (
    "You write short pieces of writing that one particular person might have written herself. "
    f"{SPEAKER_BIO} "
    "Write about the topic you are given, in her voice. "
    "Do not mention a husband, wife, spouse, marriage, wedding, pregnancy, babies, children, or siblings. "
    "Write only the piece itself, with no title, introduction, or commentary."
)

TOPICS = [
    "the moon over the bay", "fog rolling over the Golden Gate Bridge", "the bell of a cable car",
    "the Earth spinning without anyone feeling it", "the stars from Ocean Beach", "the foghorns at night",
    "the breeze off the bay", "a museum exhibit", "a history book she couldn't put down",
    "a philosophy question she can't stop thinking about", "a night at the planetarium", "the tides",
    "an old map of San Francisco", "a lunar eclipse", "a used bookstore", "a walk through the Mission",
    "a team project at work", "a model she is training", "a first date", "an old friend",
    "a noisy neighbor", "a power outage", "living alone", "a concert", "a rainy morning",
    "her mom", "her dad", "a late train", "a long walk at dusk", "a birthday",
]


def chat(model: str, system: str, user: str, temperature: float) -> str | None:
    body = json.dumps({
        "model": model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "format": SCHEMA,
        "stream": False,
        "options": {"temperature": temperature},
    }).encode()
    request = urllib.request.Request(OLLAMA_URL, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=120) as response:
        content = json.loads(response.read())["message"]["content"]
    try:
        message = json.loads(content)["message"]
    except (json.JSONDecodeError, KeyError, TypeError):
        return None
    message = message.strip().strip('"').strip()
    return message or None


def ask(model: str, section: dict, examples: list[str], temperature: float, rng: random.Random) -> str | None:
    if section.get("mode") == "writing":
        return ask_writing(model, section, temperature, rng)
    shown = "\n".join(f"- {e}" for e in examples)
    user = (
        f"The message must be of this kind: {section['description']}\n\n"
        f"Examples:\n{shown}\n\n"
        "Write one new message of exactly this kind, about a different topic from the examples. "
        "Being this kind of message matters most; her voice and interests come second. "
        "Keep it about as long as the examples. "
        'Respond as JSON: {"message": "..."}'
    )
    return chat(model, SYSTEM, user, temperature)


def ask_writing(model: str, section: dict, temperature: float, rng: random.Random) -> str | None:
    """Have the model write a short piece, then frame it as the user sharing it.

    A small model asked for "a message sharing writing" tends to write a question
    instead, so the writing and the framing are produced separately.
    """
    kind, label = rng.choice(section["kinds"])
    topic = rng.choice(TOPICS)
    user = (
        f"Write {kind} about {topic}, under 120 words. "
        'Respond as JSON: {"message": "..."}'
    )
    text = chat(model, WRITING_SYSTEM, user, temperature)
    if not text:
        return None
    return rng.choice(section["framings"]).format(label=label, text=text)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="llama3.2:3b")
    parser.add_argument("--per-section", type=int, default=160)
    parser.add_argument("--sections", nargs="*", help="only these sections, e.g. 1.1 3.4")
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--max-attempts", type=int, default=5, help="attempts per accepted prompt")
    parser.add_argument("--max-same-opening", type=int, default=3,
                        help="prompts per section that may start with the same four words")
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    sections = json.loads(SEEDS.read_text(encoding="utf-8"))
    if args.sections:
        sections = [s for s in sections if s["section"] in args.sections]

    existing = defaultdict(list)
    if OUT.exists():
        for line in OUT.read_text(encoding="utf-8-sig").splitlines():
            record = json.loads(line)
            existing[record["section"]].append(record["prompt"])

    with OUT.open("a", encoding="utf-8") as out:
        for section in sections:
            key = section["section"]
            generated = existing[key]
            seen = {normalize(p) for p in generated + section["examples"]}
            openings = Counter(opening(p) for p in generated)
            attempts = 0
            while len(generated) < args.per_section and attempts < args.per_section * args.max_attempts:
                attempts += 1
                pool = rng.sample(section["examples"], 2)
                if len(generated) >= 2:
                    pool += rng.sample(generated, 2)
                else:
                    pool = rng.sample(section["examples"], len(section["examples"]))
                rng.shuffle(pool)

                message = ask(args.model, section, pool, args.temperature, rng)
                if not message or not (10 <= len(message) <= 1500) or normalize(message) in seen:
                    continue
                if EXCLUDED.search(message):
                    continue
                if openings[opening(message)] >= args.max_same_opening:
                    continue
                openings[opening(message)] += 1
                seen.add(normalize(message))
                generated.append(message)
                record = {
                    "id": f"gen-{key}-{len(generated) - 1:04d}",
                    "source": "generated",
                    "section": key,
                    "prompt": message,
                }
                out.write(json.dumps(record, ensure_ascii=False) + "\n")
                out.flush()
            print(f"{key} {section['title']}: {len(generated)} prompts ({attempts} attempts this run)")


if __name__ == "__main__":
    main()
