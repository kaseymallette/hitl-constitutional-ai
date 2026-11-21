"""Run an experiment's prompt-generation conditions on one model.

Each condition in `experiments/<section>/conditions.json` is one way of asking a
model to write prompts: a system message, a user message, which seeds it sees,
and how many. The same conditions are run on every model, so differences in the
prompts come from the model, not the instructions. Each model's prompts go in
`experiments/<section>/<model>/<category>/<condition>.jsonl`.

The filters match generate_prompts.py: a prompt is rejected if it repeats an
earlier one, mentions a spouse, children, or siblings, stops mid-sentence,
starts with the same four words as three earlier prompts, opens on the same
topic as an earlier prompt, or, where the condition says so, hedges. Output is appended, so a stopped run can resume.

Usage:
    .venv\\Scripts\\python.exe scripts\\run_conditions.py --experiment 1.1 --model gemma3:4b --name gemma
"""

import argparse
import importlib.util
import json
import random
import time
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLLAMA_URL = "http://localhost:11434/api/chat"

_spec = importlib.util.spec_from_file_location("gp", ROOT / "scripts" / "generate_prompts.py")
gp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gp)


def chat(model: str, system: str, user: str, temperature: float) -> str | None:
    body = json.dumps({
        "model": model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "format": gp.SCHEMA,
        "stream": False,
        "think": False,
        "options": {"temperature": temperature},
    }).encode()
    request = urllib.request.Request(OLLAMA_URL, data=body, headers={"Content-Type": "application/json"})
    # Ollama occasionally returns a 500 or times out, for example while loading a
    # model; retry a few times before giving up on this request.
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                content = json.loads(response.read())["message"]["content"]
            break
        except (urllib.error.URLError, TimeoutError) as error:
            print(f"  request failed ({error}); retrying", flush=True)
            time.sleep(5 * (attempt + 1))
    else:
        return None
    try:
        message = json.loads(content)["message"]
    except (json.JSONDecodeError, KeyError, TypeError):
        return None
    message = message.strip().strip('"').strip()
    return message or None


STOP_WORDS = {"i", "im", "know", "supposed", "to", "be", "the", "a", "an", "and", "but", "my", "of", "in", "it",
              "is", "that", "like", "you", "just", "so", "for", "on", "with", "this", "all", "been", "ive",
              "about", "should", "always", "really"}


def topic(text: str, n: int = 4) -> set[str]:
    """The first few content words of a prompt, which name what it is about."""
    return set([w for w in gp.normalize(text).split() if w not in STOP_WORDS][:n])


def too_similar(message: str, kept: list[set[str]], threshold: float = 0.5) -> bool:
    """True if the message opens on the same topic as a prompt already kept.

    Catches prompts that say the same thing in different words, such as one
    model writing "I know I'm supposed to be optimizing my sleep schedule"
    eleven ways."""
    words = topic(message)
    if not words:
        return False
    return any(len(words & other) / len(words | other) >= threshold for other in kept)


def run(spec: dict, cond: dict, model: str, name: str, out: Path) -> None:
    seeds = spec["seed_sets"][cond["seeds"]]
    existing = []
    if out.exists():
        existing = [json.loads(l)["prompt"] for l in out.read_text(encoding="utf-8-sig").splitlines() if l.strip()]
    generated = list(existing)
    seen = {gp.normalize(p) for p in generated + seeds}
    openings = Counter(gp.opening(p) for p in generated)
    topics = [topic(p) for p in generated]
    rng = random.Random(cond["rng_seed"])
    target = spec["per_condition"]
    attempts = 0
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("a", encoding="utf-8", newline="\n") as f:
        while len(generated) < target and attempts < target * spec["max_attempts"]:
            attempts += 1
            pool = rng.sample(seeds, min(cond["examples"], len(seeds)))
            if cond["self_examples"] and len(generated) >= cond["self_examples"]:
                pool += rng.sample(generated, cond["self_examples"])
            elif cond["self_examples"]:
                pool = rng.sample(seeds, len(seeds))
            rng.shuffle(pool)
            shown = "\n".join(f"- {e}" for e in pool)
            message = chat(model, cond["system"], cond["user"].replace("{examples}", shown), spec["temperature"])
            if not message or not (10 <= len(message) <= 1500) or gp.normalize(message) in seen:
                continue
            if gp.EXCLUDED.search(message) or gp.looks_cut_off(message):
                continue
            if cond["reject_hedges"] and gp.HEDGES.search(message):
                continue
            if openings[gp.opening(message)] >= spec["max_same_opening"]:
                continue
            if spec.get("topic_filter") and too_similar(message, topics):
                continue
            topics.append(topic(message))
            openings[gp.opening(message)] += 1
            seen.add(gp.normalize(message))
            generated.append(message)
            record = {
                "id": f"{name}-{cond['name']}-{len(generated) - 1:03d}",
                "section": spec["section"],
                "category": spec["category"],
                "model": model,
                "source": cond["name"],
                "prompt": message,
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            f.flush()
    print(f"{name} {cond['name']}: {len(generated)} prompts ({attempts} attempts this run)", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--experiment", default="1.1")
    parser.add_argument("--model", required=True, help="Ollama tag, e.g. gemma3:4b")
    parser.add_argument("--name", required=True, help="folder name for this model, e.g. gemma")
    parser.add_argument("--conditions", nargs="*", help="only these conditions")
    parser.add_argument("--per-condition", type=int, help="override the number of prompts per condition")
    parser.add_argument("--topic-filter", action="store_true",
                        help="also reject prompts that open on the same topic as an earlier one (off by default; Llama's rounds did not use it)")
    parser.add_argument("--max-same-opening", type=int,
                        help="override how many prompts may share their first four words")
    args = parser.parse_args()

    experiment = ROOT / "experiments" / args.experiment
    spec = json.loads((experiment / "conditions.json").read_text(encoding="utf-8"))
    if args.per_condition:
        spec["per_condition"] = args.per_condition
    spec["topic_filter"] = args.topic_filter
    if args.max_same_opening:
        spec["max_same_opening"] = args.max_same_opening
    for cond in spec["conditions"]:
        if args.conditions and cond["name"] not in args.conditions:
            continue
        out = experiment / args.name / spec["category"] / f"{cond['name']}.jsonl"
        run(spec, cond, args.model, args.name, out)


if __name__ == "__main__":
    main()
