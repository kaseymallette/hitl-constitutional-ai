"""Generate pairs of opposing opinions for an experiment.

The instructions and topics are in experiments/<section>/prompts/generation.json and
are the same for every model. Each request names one area, one topic, and one
category (certain or uncertain) and asks for one pair. No examples are sent. A
pair is rejected only if it is malformed or repeats an earlier prompt word for
word.

Every model's pairs, certain and uncertain, in every area, go in one file,
experiments/<section>/prompts/prompt_pairs.jsonl, one pair per line, labeled
with the model. Output is appended, so a stopped run resumes.

Usage:
    .venv\\Scripts\\python.exe scripts\\generate_pairs.py --model llama3.2:3b --name llama --category certain --areas "Food and drink"
"""

import argparse
import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLLAMA_URL = "http://localhost:11434/api/chat"
SCHEMA = {
    "type": "object",
    "properties": {
        "first": {"type": "string"},
        "second": {"type": "string"},
    },
    "required": ["first", "second"],
}


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def normalize(text: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9 ]", "", text.lower()).split())


def chat(model: str, system: str, user: str, temperature: float) -> dict | None:
    body = json.dumps({
        "model": model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "format": SCHEMA,
        "stream": False,
        "think": False,
        "options": {"temperature": temperature},
    }).encode()
    request = urllib.request.Request(OLLAMA_URL, data=body, headers={"Content-Type": "application/json"})
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
        pair = json.loads(content)
        return {k: pair[k].strip().strip('"').strip() for k in ("first", "second")}
    except (json.JSONDecodeError, KeyError, TypeError, AttributeError):
        return None


def usable(pair: dict | None, seen: set[str]) -> bool:
    if not pair or not all(10 <= len(pair[k]) <= 1000 for k in ("first", "second")):
        return False
    first, second = normalize(pair["first"]), normalize(pair["second"])
    return first != second and first not in seen and second not in seen


def run(spec: dict, model: str, name: str, category: str, area: str, out: Path) -> None:
    records = []
    if out.exists():
        records = [json.loads(l) for l in out.read_text(encoding="utf-8").splitlines() if l.strip()]
    records = [r for r in records if r["model"] == model]
    seen = {normalize(r[k]) for r in records for k in ("first", "second")}
    records = [r for r in records if r["category"] == category and r["area"] == area]
    done = {r["topic"] for r in records}
    attempts = 0
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("a", encoding="utf-8", newline="\n") as f:
        for topic in spec["areas"][area]:
            if topic in done:
                continue
            user = (spec["user"].replace("{area}", area).replace("{topic}", topic)
                    .replace("{category_line}", spec["categories"][category]))
            for _ in range(spec["max_attempts_per_pair"]):
                attempts += 1
                pair = chat(model, spec["system"], user, spec["temperature"])
                if not usable(pair, seen):
                    continue
                seen.update({normalize(pair["first"]), normalize(pair["second"])})
                record = {
                    "id": f"{name}-{category}-{slug(area)}-{len(records):02d}",
                    "section": spec["section"],
                    "model": model,
                    "category": category,
                    "area": area,
                    "topic": topic,
                    **pair,
                }
                records.append(record)
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
                f.flush()
                break
            else:
                print(f"  no usable pair for {topic!r}", flush=True)
    print(f"{name} {category} {area}: {len(records)} pairs ({attempts} attempts this run)", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--experiment", default="1.1")
    parser.add_argument("--model", required=True, help="Ollama tag, e.g. llama3.2:3b")
    parser.add_argument("--name", required=True, help="folder name for this model, e.g. llama")
    parser.add_argument("--category", required=True, choices=["certain", "uncertain"])
    parser.add_argument("--areas", nargs="*", help="only these areas (default: every area with topics)")
    args = parser.parse_args()

    experiment = ROOT / "experiments" / args.experiment
    spec = json.loads((experiment / "prompts" / "generation.json").read_text(encoding="utf-8"))
    for area, topics in spec["areas"].items():
        if (args.areas and area not in args.areas) or not topics:
            continue
        out = experiment / "prompts" / "prompt_pairs.jsonl"
        run(spec, args.model, args.name, args.category, area, out)


if __name__ == "__main__":
    main()
