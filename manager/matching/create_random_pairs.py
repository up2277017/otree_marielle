"""Create fixed, reproducible random worker pairs for the manager study."""

import argparse
import csv
import random
from pathlib import Path

INPUT_FIELDS = ("worker_id", "correct_letters", "letters_revealed")
OUTPUT_FIELDS = (
    "pair_id",
    "worker_1_id",
    "worker_1_correct",
    "worker_1_help",
    "worker_2_id",
    "worker_2_correct",
    "worker_2_help",
    "matching_seed",
)
MIN_SCORE = 0
MAX_SCORE = 22


def score(value: str, field_name: str, row_number: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Row {row_number}: {field_name} must be a whole number.") from exc
    if not MIN_SCORE <= parsed <= MAX_SCORE:
        raise ValueError(
            f"Row {row_number}: {field_name} must be between {MIN_SCORE} and {MAX_SCORE}."
        )
    return parsed


def read_workers(input_path: Path) -> list[dict]:
    with input_path.open(newline="", encoding="utf-8-sig") as input_file:
        sample = input_file.read(4096)
        input_file.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        except csv.Error as exc:
            raise ValueError(
                "Could not identify the CSV separator. Save the Excel sheet as "
                "CSV UTF-8 (comma- or semicolon-delimited)."
            ) from exc

        reader = csv.DictReader(input_file, dialect=dialect)
        if reader.fieldnames != list(INPUT_FIELDS):
            raise ValueError("The raw CSV headings must be exactly: " + ", ".join(INPUT_FIELDS))
        workers = []
        seen_ids = set()
        for row_number, row in enumerate(reader, start=2):
            worker_id = row["worker_id"].strip()
            if not worker_id:
                raise ValueError(f"Row {row_number}: worker_id is missing.")
            if worker_id in seen_ids:
                raise ValueError(f"Row {row_number}: duplicate worker_id {worker_id!r}.")
            seen_ids.add(worker_id)
            workers.append(
                dict(
                    worker_id=worker_id,
                    correct_letters=score(row["correct_letters"], "correct_letters", row_number),
                    letters_revealed=score(
                        row["letters_revealed"], "letters_revealed", row_number
                    ),
                )
            )
    if len(workers) < 2:
        raise ValueError("At least two workers are required.")
    if len(workers) % 2 != 0:
        raise ValueError(
            f"The number of workers must be even, but found {len(workers)}. "
            "One worker would otherwise be left without a partner."
        )
    return workers


def create_pairs(workers: list[dict], seed: int) -> list[dict]:
    shuffled_workers = workers.copy()
    random.Random(seed).shuffle(shuffled_workers)
    pairs = []
    for pair_id, index in enumerate(range(0, len(shuffled_workers), 2), start=1):
        worker_1 = shuffled_workers[index]
        worker_2 = shuffled_workers[index + 1]
        pairs.append(
            dict(
                pair_id=pair_id,
                worker_1_id=worker_1["worker_id"],
                worker_1_correct=worker_1["correct_letters"],
                worker_1_help=worker_1["letters_revealed"],
                worker_2_id=worker_2["worker_id"],
                worker_2_correct=worker_2["correct_letters"],
                worker_2_help=worker_2["letters_revealed"],
                matching_seed=seed,
            )
        )
    return pairs


def write_pairs(output_path: Path, pairs: list[dict]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(pairs)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Randomly match any even number of workers into fixed pairs."
    )
    parser.add_argument("--input", type=Path, required=True, help="Raw worker CSV")
    parser.add_argument("--output", type=Path, required=True, help="Matched pair CSV")
    parser.add_argument(
        "--seed",
        type=int,
        required=True,
        help="Recorded random seed; reuse it to reproduce the same pairs",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    workers = read_workers(args.input)
    pairs = create_pairs(workers, args.seed)
    write_pairs(args.output, pairs)
    print(
        f"Created {len(pairs)} random pairs from {len(workers)} workers "
        f"using seed {args.seed}. Output: {args.output}"
    )


if __name__ == "__main__":
    main()
