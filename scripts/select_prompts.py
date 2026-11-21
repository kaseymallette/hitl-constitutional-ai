"""Hand-pick prompts from earlier generation rounds into one labeled set.

Each round of generation showed a different bias, so the final set is chosen by
the author: a fixed number of prompts from each round, labeled with the round
they came from.

  review  Writes a checklist of every prompt in the chosen rounds, grouped by
          round. The author checks the box next to each prompt to keep.
  build   Reads the checked boxes and writes the set, with each prompt's round
          recorded in its "source" field.

Usage:
    .venv\\Scripts\\python.exe scripts\\select_prompts.py review --experiment 1.1 --rounds certain
    .venv\\Scripts\\python.exe scripts\\select_prompts.py build --experiment 1.1 --rounds certain
"""

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINE = re.compile(r"^- \[([ xX])\] \*\*(?P<id>[^*]+)\*\* ")


def rounds(pilot: Path, prefix: str) -> dict[str, list[dict]]:
    """Each round is a file in pilot/<prefix>/, such as pilot/certain/career_bias.jsonl."""
    found = {}
    for path in sorted((pilot / prefix).glob("*.jsonl")):
        name = path.stem
        with path.open(encoding="utf-8-sig") as f:
            records = [json.loads(line) for line in f if line.strip()]
        for i, record in enumerate(records):
            record["source"] = name
            record["id"] = f"{name}-{i:03d}"
        found[name] = records
    return found


def review(experiment: Path, prefix: str, per_round: int) -> None:
    found = rounds(experiment / "pilot", prefix)
    out = experiment / f"review_{prefix}.md"
    lines = [
        f"# Review: {prefix} prompts",
        "",
        f"Check the box next to each prompt to keep, {per_round} from each round. "
        "Then run `select_prompts.py build`.",
        "",
    ]
    for name, records in found.items():
        lines += [f"## {name} ({len(records)} prompts)", ""]
        for record in records:
            text = " ".join(record["prompt"].split())
            lines.append(f"- [ ] **{record['id']}** {text}")
        lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"wrote {out} ({sum(len(r) for r in found.values())} prompts in {len(found)} rounds)")


def build(experiment: Path, prefix: str, per_round: int) -> None:
    found = rounds(experiment / "pilot", prefix)
    by_id = {r["id"]: r for records in found.values() for r in records}
    checked = []
    for line in (experiment / f"review_{prefix}.md").read_text(encoding="utf-8").splitlines():
        match = LINE.match(line)
        if match and match.group(1).lower() == "x":
            checked.append(by_id[match.group("id")])

    counts = {name: 0 for name in found}
    for record in checked:
        counts[record["source"]] += 1
    for name, n in counts.items():
        flag = "" if n == per_round else f"  (expected {per_round})"
        print(f"{name:28s} {n:3d}{flag}")

    out = experiment / "prompts.jsonl"
    with out.open("w", encoding="utf-8", newline="\n") as f:
        for record in checked:
            keep = {k: record[k] for k in ("id", "section", "category", "source", "prompt") if k in record}
            f.write(json.dumps(keep, ensure_ascii=False) + "\n")
    print(f"wrote {out} ({len(checked)} prompts)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["review", "build"])
    parser.add_argument("--experiment", default="1.1")
    parser.add_argument("--rounds", default="certain", help="folder of the rounds in pilot/")
    parser.add_argument("--per-round", type=int, default=25)
    args = parser.parse_args()
    experiment = ROOT / "experiments" / args.experiment
    if args.command == "review":
        review(experiment, args.rounds, args.per_round)
    else:
        build(experiment, args.rounds, args.per_round)


if __name__ == "__main__":
    main()
