"""Extract red-team and helpfulness prompts from Anthropic/hh-rlhf.

As in Bai et al. (2022), a prompt is the first human turn of a conversation.
Red-team prompts come from `red-team-attempts`; helpfulness prompts come from
`helpful-base`. Each source is deduplicated, filtered by length, and sampled
with a fixed seed so the result can be reproduced.

Usage:
    .venv\\Scripts\\python.exe scripts\\extract_hh_prompts.py
"""

import argparse
import json
import random
import re
from pathlib import Path

from datasets import load_dataset

OUT_DIR = Path(__file__).resolve().parent.parent / "data" / "prompts"
FIRST_HUMAN_TURN = re.compile(r"Human:(.*?)(?:\n\nAssistant:|$)", re.DOTALL)


def first_human_turn(conversation: str) -> str | None:
    match = FIRST_HUMAN_TURN.search(conversation)
    if not match:
        return None
    return " ".join(match.group(1).split())


def collect(texts, min_chars: int, max_chars: int) -> list[str]:
    seen = set()
    prompts = []
    for text in texts:
        prompt = first_human_turn(text)
        if not prompt or not (min_chars <= len(prompt) <= max_chars):
            continue
        key = prompt.lower()
        if key in seen:
            continue
        seen.add(key)
        prompts.append(prompt)
    return prompts


def write_jsonl(path: Path, source: str, prompts: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for i, prompt in enumerate(prompts):
            record = {"id": f"{source}-{i:05d}", "source": source, "prompt": prompt}
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--red-team", type=int, default=2025, help="red-team prompts to sample")
    parser.add_argument("--helpful", type=int, default=2025, help="helpfulness prompts to sample")
    parser.add_argument("--min-chars", type=int, default=10)
    parser.add_argument("--max-chars", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    rng = random.Random(args.seed)

    red_team = load_dataset("Anthropic/hh-rlhf", data_dir="red-team-attempts", split="train")
    red_prompts = collect(red_team["transcript"], args.min_chars, args.max_chars)

    helpful = load_dataset("Anthropic/hh-rlhf", data_dir="helpful-base", split="train")
    helpful_prompts = collect(helpful["chosen"], args.min_chars, args.max_chars)

    print(f"red-team: {len(red_prompts)} unique prompts, sampling {args.red_team}")
    print(f"helpful:  {len(helpful_prompts)} unique prompts, sampling {args.helpful}")

    write_jsonl(OUT_DIR / "hh_red_team.jsonl", "hh-red-team", rng.sample(red_prompts, args.red_team))
    write_jsonl(OUT_DIR / "hh_helpful.jsonl", "hh-helpful", rng.sample(helpful_prompts, args.helpful))
    print(f"wrote {OUT_DIR}")


if __name__ == "__main__":
    main()
