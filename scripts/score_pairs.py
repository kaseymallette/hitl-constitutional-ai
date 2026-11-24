"""Score whether each pair of prompts opposes, the first measure of an experiment.

Each pair is scored as opposed, same side, no stance, or broken.

1. Rules mark a pair broken when either message has leftover JSON, such as
   "second": or a stray "}. Broken pairs are not sent to the judge.
2. A judge model labels each message on its own: which position it leans
   toward, or neither. The pair's score follows from the two labels.
   On two-sided topics, the positions come from the topic ("X vs. Y") or from
   experiments/<section>/scoring/opposing.json. On open topics, such as Best
   candy, the judge names the side's choice, then says whether the two
   choices are the same.
3. A sample of pairs is written out for the author to label by hand, and the
   author's labels are compared with the judge's.

The judge runs on the OpenAI Responses API. The key is read from the
OPENAI_API_KEY environment variable, or from a .env file at the repo root
(OPENAI_API_KEY=sk-...). A variable already set in the shell wins.
Output is appended, so a stopped run resumes.

Usage:
    .venv\\Scripts\\python.exe scripts\\score_pairs.py rules
    .venv\\Scripts\\python.exe scripts\\score_pairs.py judge --model <model id> --effort medium
    .venv\\Scripts\\python.exe scripts\\score_pairs.py summary
    .venv\\Scripts\\python.exe scripts\\score_pairs.py sample --per-group 10
    .venv\\Scripts\\python.exe scripts\\score_pairs.py agree
"""

import argparse
import collections
import csv
import json
import os
import random
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OPENAI_URL = "https://api.openai.com/v1/responses"
LABELS = ["opposed", "same side", "no stance", "broken"]
MODELS = {"llama3.2:3b": "Llama 3.2 3B", "gemma3:4b": "Gemma 3 4B", "qwen3.5:4b": "Qwen 3.5 4B"}

LEFTOVER_JSON = [
    re.compile(r'"\s*(first|second)\s*"\s*:'),  # a JSON key inside the message
    re.compile(r'"\s*[}\]]\s*$'),               # ends with "} or "]
    re.compile(r'"\s*,\s*$'),                   # ends with ",
    re.compile(r'"\s*}\s*{'),                   # "} { between two objects
]
PLACEHOLDER = re.compile(r"\{[^{}]*\}|\[[A-Z][^\[\]]*\]|^\s*Second:\s*$", re.MULTILINE)


def paths(section: str) -> dict:
    experiment = ROOT / "experiments" / section
    return {
        "pairs": experiment / "prompts" / "prompt_pairs.jsonl",
        "spec": experiment / "scoring" / "opposing.json",
        "scores": experiment / "scoring" / "opposing_pairs.jsonl",
        "sample": experiment / "scoring" / "opposing_sample.csv",
    }


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def leftover_json(text: str) -> bool:
    return any(p.search(text) for p in LEFTOVER_JSON)


def placeholders(text: str) -> list[str]:
    found = [m.group(0).strip() for m in PLACEHOLDER.finditer(text)]
    return [f if len(f) <= 40 else f[:37] + "..." for f in found]


def positions(spec: dict, topic: str) -> list[str] | None:
    if topic in spec["open_topics"]:
        return None
    if topic in spec["positions"]:
        return spec["positions"][topic]
    a, b = re.split(r" vs\. | versus ", topic, maxsplit=1)
    return [a.strip(), b.split(":")[0].strip()]


def load_env(path: Path = ROOT / ".env") -> None:
    """Set variables from a .env file without overriding ones already set."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        name = name.removeprefix("export ").strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        os.environ.setdefault(name, value)


def ask(model: str, effort: str, system: str, user: str, schema: dict) -> dict:
    load_env()
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise SystemExit("Set OPENAI_API_KEY before running the judge.")
    body = {
        "model": model,
        "instructions": system,
        "input": user,
        "store": False,
        "text": {"format": {"type": "json_schema", "name": "label", "schema": schema, "strict": True}},
    }
    if effort:
        body["reasoning"] = {"effort": effort}
    request = urllib.request.Request(
        OPENAI_URL,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
    )
    for attempt in range(5):
        try:
            with urllib.request.urlopen(request, timeout=300) as response:
                data = json.loads(response.read())
            break
        except urllib.error.HTTPError as error:
            if error.code in (429, 500, 502, 503, 504) and attempt < 4:
                print(f"  request failed ({error.code}); retrying", flush=True)
                time.sleep(10 * (attempt + 1))
                continue
            raise SystemExit(f"OpenAI API error {error.code}: {error.read().decode(errors='replace')}")
        except (urllib.error.URLError, TimeoutError) as error:
            print(f"  request failed ({error}); retrying", flush=True)
            time.sleep(10 * (attempt + 1))
    else:
        raise SystemExit("OpenAI API did not respond.")
    for item in data.get("output", []):
        if item.get("type") == "message":
            for part in item.get("content", []):
                if part.get("type") == "output_text":
                    return json.loads(part["text"])
    raise SystemExit(f"No text in the response: {json.dumps(data)[:500]}")


def schema(properties: dict) -> dict:
    return {"type": "object", "properties": properties, "required": list(properties), "additionalProperties": False}


def judge_pair(spec: dict, pair: dict, model: str, effort: str) -> dict:
    sides = positions(spec, pair["topic"])
    if sides:
        label_schema = schema({"position": {"type": "string", "enum": ["A", "B", "neither"]}})
        found = []
        for key in ("first", "second"):
            user = (spec["two_sided"].replace("{topic}", pair["topic"]).replace("{a}", sides[0])
                    .replace("{b}", sides[1]).replace("{message}", pair[key]))
            answer = ask(model, effort, spec["system"], user, label_schema)["position"]
            found.append(None if answer == "neither" else sides[0] if answer == "A" else sides[1])
        same = found[0] == found[1] if all(found) else None
    else:
        choice_schema = schema({"choice": {"type": ["string", "null"]}})
        found = []
        for key in ("first", "second"):
            user = spec["open"].replace("{topic}", pair["topic"]).replace("{message}", pair[key])
            choice = ask(model, effort, spec["system"], user, choice_schema)["choice"]
            found.append(choice.strip() if choice and choice.strip() else None)
        same = None
        if all(found):
            user = (spec["same_choice"].replace("{topic}", pair["topic"])
                    .replace("{first}", found[0]).replace("{second}", found[1]))
            same = ask(model, effort, spec["system"], user, schema({"same": {"type": "boolean"}}))["same"]
    label = "no stance" if not all(found) else "same side" if same else "opposed"
    return {"first_position": found[0], "second_position": found[1], "label": label}


def score_record(pair: dict, judged: dict | None, broken: bool, model: str | None, effort: str | None) -> dict:
    return {
        "id": pair["id"],
        "model": pair["model"],
        "category": pair["category"],
        "area": pair["area"],
        "topic": pair["topic"],
        "broken": broken,
        "placeholders": placeholders(pair["first"]) + placeholders(pair["second"]),
        "first_position": judged["first_position"] if judged else None,
        "second_position": judged["second_position"] if judged else None,
        "label": "broken" if broken else judged["label"],
        "judge": None if broken else model,
        "effort": None if broken else effort,
    }


def cmd_rules(p: dict, args) -> None:
    pairs = read_jsonl(p["pairs"])
    broken = [r for r in pairs if leftover_json(r["first"]) or leftover_json(r["second"])]
    marked = [r for r in pairs if r not in broken and (placeholders(r["first"]) or placeholders(r["second"]))]
    print(f"{len(broken)} of {len(pairs)} pairs are broken (leftover JSON):")
    for r in broken:
        print(f"  {r['id']}  {r['topic']}")
    print(f"\n{len(marked)} more have placeholders or labels but are judged as usual:")
    for r in marked:
        print(f"  {r['id']}  {placeholders(r['first']) + placeholders(r['second'])}")


def cmd_judge(p: dict, args) -> None:
    spec = json.loads(p["spec"].read_text(encoding="utf-8"))
    pairs = read_jsonl(p["pairs"])
    done = {r["id"] for r in read_jsonl(p["scores"])}
    todo = [r for r in pairs if r["id"] not in done]
    if args.limit:
        todo = todo[: args.limit]
    print(f"{len(done)} pairs already scored, {len(todo)} to score", flush=True)
    p["scores"].parent.mkdir(parents=True, exist_ok=True)
    with p["scores"].open("a", encoding="utf-8", newline="\n") as f:
        for n, pair in enumerate(todo, 1):
            broken = leftover_json(pair["first"]) or leftover_json(pair["second"])
            judged = None if broken else judge_pair(spec, pair, args.model, args.effort)
            record = score_record(pair, judged, broken, args.model, args.effort)
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            f.flush()
            print(f"  {n}/{len(todo)} {pair['id']}: {record['label']}", flush=True)


def cmd_summary(p: dict, args) -> None:
    scores = read_jsonl(p["scores"])
    groups = collections.defaultdict(collections.Counter)
    for r in scores:
        groups[(r["model"], r["category"])][r["label"]] += 1
    print("| Model | Category | Pairs | " + " | ".join(l.capitalize() for l in LABELS) + " |")
    print("|---|---|---|" + "---|" * len(LABELS))
    for model in MODELS:
        for category in ("certain", "uncertain"):
            counts = groups.get((model, category))
            if not counts:
                continue
            total = sum(counts.values())
            cells = " | ".join(f"{counts[l]} ({100 * counts[l] / total:.0f}%)" for l in LABELS)
            print(f"| {MODELS[model]} | {category.capitalize()} | {total} | {cells} |")


def cmd_sample(p: dict, args) -> None:
    if p["sample"].exists() and not args.force:
        raise SystemExit(f"{p['sample']} exists; pass --force to replace it and lose any labels in it.")
    pairs = read_jsonl(p["pairs"])
    groups = collections.defaultdict(list)
    for r in pairs:
        groups[(r["model"], r["category"])].append(r)
    rng = random.Random(args.seed)
    sample = []
    for key in sorted(groups):
        sample += rng.sample(groups[key], min(args.per_group, len(groups[key])))
    rng.shuffle(sample)  # so the author does not label one model at a time
    p["sample"].parent.mkdir(parents=True, exist_ok=True)
    with p["sample"].open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "topic", "first", "second", "label"])
        for r in sample:
            writer.writerow([r["id"], r["topic"], r["first"], r["second"], ""])
    print(f"Wrote {len(sample)} pairs to {p['sample']}. Fill the label column with: {', '.join(LABELS)}.")


def cmd_agree(p: dict, args) -> None:
    judged = {r["id"]: r["label"] for r in read_jsonl(p["scores"])}
    with p["sample"].open(encoding="utf-8-sig", newline="") as f:
        rows = [r for r in csv.DictReader(f) if r["label"].strip()]
    rows = [r for r in rows if r["id"] in judged]
    bad = [r["label"] for r in rows if r["label"].strip().lower() not in LABELS]
    if bad:
        raise SystemExit(f"Unknown labels in the sample: {sorted(set(bad))}. Use: {', '.join(LABELS)}.")
    if not rows:
        raise SystemExit("No pairs are both labeled in the sample and scored by the judge.")
    pairs = [(r["label"].strip().lower(), judged[r["id"]]) for r in rows]
    agree = sum(a == j for a, j in pairs)
    n = len(pairs)
    observed = agree / n
    author, judge = collections.Counter(a for a, _ in pairs), collections.Counter(j for _, j in pairs)
    expected = sum(author[l] * judge[l] for l in LABELS) / (n * n)
    kappa = (observed - expected) / (1 - expected) if expected < 1 else 1.0
    print(f"{n} pairs labeled by both. Agreement: {agree}/{n} ({100 * observed:.0f}%). Cohen's kappa: {kappa:.2f}.")
    print("\nRows: the author's label. Columns: the judge's label.")
    print("| Author \\ Judge | " + " | ".join(LABELS) + " |")
    print("|---|" + "---|" * len(LABELS))
    for a in LABELS:
        print(f"| {a} | " + " | ".join(str(sum(1 for x, y in pairs if x == a and y == j)) for j in LABELS) + " |")
    misses = [(r["id"], r["label"].strip().lower(), judged[r["id"]]) for r in rows if r["label"].strip().lower() != judged[r["id"]]]
    if misses:
        print("\nDisagreements:")
        for id_, a, j in misses:
            print(f"  {id_}: author {a}, judge {j}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--experiment", default="1.1")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("rules", help="list the pairs the rules mark broken; no API calls")
    judge = sub.add_parser("judge", help="score every pair not yet scored")
    judge.add_argument("--model", required=True, help="OpenAI model id")
    judge.add_argument("--effort", default="medium", help="reasoning effort, or empty for none")
    judge.add_argument("--limit", type=int, help="score only this many pairs, to try the judge first")
    sub.add_parser("summary", help="print the scores as a table")
    sample = sub.add_parser("sample", help="write a sample of pairs for the author to label")
    sample.add_argument("--per-group", type=int, default=10, help="pairs per model and category")
    sample.add_argument("--seed", type=int, default=11)
    sample.add_argument("--force", action="store_true")
    sub.add_parser("agree", help="compare the author's sample labels with the judge's")
    args = parser.parse_args()
    p = paths(args.experiment)
    {"rules": cmd_rules, "judge": cmd_judge, "summary": cmd_summary,
     "sample": cmd_sample, "agree": cmd_agree}[args.command](p, args)


if __name__ == "__main__":
    main()
