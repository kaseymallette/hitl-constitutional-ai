"""Combine all prompts and hold some out for evaluation.

Reads the hh-rlhf prompts and the generated prompts in `data/prompts/` and
writes two files:

- `train.jsonl`: prompts for Stage 1 and Stage 2.
- `eval.jsonl`: held-out prompts the trained model never sees. The author
  compares trained and untrained responses on these.

The held-out set takes a fixed number of prompts from each hh-rlhf source and
from each generated section, so every part of the constitution is evaluated.

Usage:
    .venv\\Scripts\\python.exe scripts\\split_prompts.py
"""

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path

PROMPTS = Path(__file__).resolve().parent.parent / "data" / "prompts"
SOURCES = ["hh_red_team.jsonl", "hh_helpful.jsonl", "generated.jsonl"]


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig") as f:
        return [json.loads(line) for line in f if line.strip()]


def write_jsonl(path: Path, records: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--eval-per-hh-source", type=int, default=25)
    parser.add_argument("--eval-per-section", type=int, default=4)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    groups = defaultdict(list)
    for name in SOURCES:
        for record in read_jsonl(PROMPTS / name):
            group = record["section"] if record["source"] == "generated" else record["source"]
            groups[group].append(record)

    train, held_out = [], []
    for group in sorted(groups):
        records = groups[group][:]
        rng.shuffle(records)
        n = args.eval_per_section if group[0].isdigit() else args.eval_per_hh_source
        held_out += records[:n]
        train += records[n:]
        print(f"{group:12s} train {len(records) - n:5d}  eval {n:3d}")

    rng.shuffle(train)
    write_jsonl(PROMPTS / "train.jsonl", train)
    write_jsonl(PROMPTS / "eval.jsonl", held_out)
    print(f"total        train {len(train):5d}  eval {len(held_out):3d}")


if __name__ == "__main__":
    main()
