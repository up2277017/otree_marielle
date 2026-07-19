"""Assign every fixed worker pair once to a manager and treatment."""

import argparse
import csv
import random
from collections import Counter
from pathlib import Path

PERFORMANCE_ONLY = "performance_only"
PERFORMANCE_AND_HELP = "performance_and_help"
OUTPUT_FIELDS = (
    "treatment",
    "manager_slot",
    "decision_number",
    "pair_id",
    "worker_1_is_a",
    "assignment_seed",
)


def read_pair_ids(input_path: Path) -> list[int]:
    with input_path.open(newline="", encoding="utf-8-sig") as input_file:
        reader = csv.DictReader(input_file)
        if "pair_id" not in (reader.fieldnames or []):
            raise ValueError(f"{input_path} must contain a pair_id column.")

        pair_ids = []
        seen_pair_ids = set()
        for row_number, row in enumerate(reader, start=2):
            try:
                pair_id = int(row["pair_id"])
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Row {row_number}: pair_id must be a whole number.") from exc
            if pair_id in seen_pair_ids:
                raise ValueError(f"Row {row_number}: duplicate pair_id {pair_id}.")
            seen_pair_ids.add(pair_id)
            pair_ids.append(pair_id)

    if not pair_ids:
        raise ValueError(f"No worker pairs were found in {input_path}.")
    return pair_ids


def create_assignments(
    pair_ids: list[int],
    performance_managers: int,
    help_managers: int,
    max_pairs_per_manager: int,
    seed: int,
) -> list[dict]:
    if performance_managers < 1 or help_managers < 1:
        raise ValueError(
            "At least one performance-only manager and one "
            "performance-plus-helping manager are required."
        )
    if max_pairs_per_manager < 1 or max_pairs_per_manager > 25:
        raise ValueError("max_pairs_per_manager must be between 1 and 25.")

    manager_slots = [(PERFORMANCE_ONLY, slot) for slot in range(1, performance_managers + 1)] + [
        (PERFORMANCE_AND_HELP, slot) for slot in range(1, help_managers + 1)
    ]
    manager_count = len(manager_slots)
    if len(pair_ids) < manager_count:
        raise ValueError(
            f"There are {len(pair_ids)} pairs but {manager_count} managers. "
            "Every manager must receive at least one pair."
        )

    capacity = manager_count * max_pairs_per_manager
    if len(pair_ids) > capacity:
        additional_managers = (
            len(pair_ids) - capacity + max_pairs_per_manager - 1
        ) // max_pairs_per_manager
        raise ValueError(
            f"{manager_count} managers can evaluate at most {capacity} pairs, "
            f"but {len(pair_ids)} pairs are available. Add at least "
            f"{additional_managers} manager(s) or increase the permitted workload."
        )

    rng = random.Random(seed)
    shuffled_pair_ids = pair_ids.copy()
    rng.shuffle(shuffled_pair_ids)

    # Randomize which manager slots receive any partial workloads. Then give 25
    # pairs wherever possible while reserving at least one pair for every
    # remaining scheduled manager.
    allocation_order = list(range(manager_count))
    rng.shuffle(allocation_order)
    workloads_by_slot_index = {}
    remaining_pairs = len(pair_ids)
    for allocation_position, slot_index in enumerate(allocation_order):
        remaining_managers = manager_count - allocation_position
        workload = min(
            max_pairs_per_manager,
            remaining_pairs - (remaining_managers - 1),
        )
        workloads_by_slot_index[slot_index] = workload
        remaining_pairs -= workload

    if remaining_pairs != 0:
        raise RuntimeError("Internal error: manager workloads do not use every pair.")

    assignments = []
    pair_index = 0
    for slot_index, (treatment, manager_slot) in enumerate(manager_slots):
        workload = workloads_by_slot_index[slot_index]
        assigned_pair_ids = shuffled_pair_ids[pair_index : pair_index + workload]
        pair_index += workload
        rng.shuffle(assigned_pair_ids)

        for decision_number, pair_id in enumerate(assigned_pair_ids, start=1):
            assignments.append(
                dict(
                    treatment=treatment,
                    manager_slot=manager_slot,
                    decision_number=decision_number,
                    pair_id=pair_id,
                    worker_1_is_a=int(rng.choice([True, False])),
                    assignment_seed=seed,
                )
            )

    if pair_index != len(shuffled_pair_ids):
        raise RuntimeError("Internal error: not every pair was assigned.")
    return assignments


def write_assignments(output_path: Path, assignments: list[dict]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(assignments)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Assign every worker pair exactly once across performance-only and "
            "performance-plus-helping managers."
        )
    )
    parser.add_argument("--input", type=Path, required=True, help="worker_pairs.csv")
    parser.add_argument("--output", type=Path, required=True, help="manager_assignments.csv")
    parser.add_argument("--performance-managers", type=int, required=True)
    parser.add_argument("--help-managers", type=int, required=True)
    parser.add_argument("--max-pairs-per-manager", type=int, default=25)
    parser.add_argument("--seed", type=int, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    pair_ids = read_pair_ids(args.input)
    assignments = create_assignments(
        pair_ids=pair_ids,
        performance_managers=args.performance_managers,
        help_managers=args.help_managers,
        max_pairs_per_manager=args.max_pairs_per_manager,
        seed=args.seed,
    )
    write_assignments(args.output, assignments)

    treatment_counts = Counter(row["treatment"] for row in assignments)
    manager_counts = Counter((row["treatment"], row["manager_slot"]) for row in assignments)
    workloads = list(manager_counts.values())
    print(
        f"Assigned {len(assignments)} pairs exactly once across "
        f"{len(manager_counts)} managers using seed {args.seed}."
    )
    print(
        f"Performance-only decisions: {treatment_counts[PERFORMANCE_ONLY]}; "
        f"performance-plus-helping decisions: "
        f"{treatment_counts[PERFORMANCE_AND_HELP]}."
    )
    print(
        f"Manager workloads range from {min(workloads)} to {max(workloads)} pairs. "
        f"Output: {args.output}"
    )


if __name__ == "__main__":
    main()
