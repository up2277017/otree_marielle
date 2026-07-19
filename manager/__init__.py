import csv
from pathlib import Path

from otree.api import *

doc = """
Manager study: each manager evaluates a scheduled set of up to 25 unique worker
pairs and divides 100 pence between Worker A and Worker B. Each pair is assigned
once overall to either the performance-only or performance-plus-helping treatment.
"""


class C(BaseConstants):
    NAME_IN_URL = 'manager'
    PLAYERS_PER_GROUP = None
    # oTree creates this many possible rounds. The assignment schedule can give
    # an individual manager fewer rounds, and the unused rounds stay hidden.
    NUM_ROUNDS = 25
    TOTAL_PENCE = 100
    PERFORMANCE_ONLY = "performance_only"
    PERFORMANCE_AND_HELP = "performance_and_help"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Assignment metadata, repeated across rounds for transparent exports.
    manager_slot = models.IntegerField()
    manager_treatment = models.StringField()
    assigned_pair_count = models.IntegerField(min=1, max=25)
    assignment_seed = models.IntegerField()
    worker_1_is_a = models.BooleanField()

    # Pair information shown in this round
    pair_id = models.IntegerField()

    # Internal worker IDs, stored for later merging but never displayed
    worker_a_id = models.StringField()
    worker_b_id = models.StringField()

    worker_a_correct = models.IntegerField(min=0, max=22)
    worker_b_correct = models.IntegerField(min=0, max=22)
    worker_a_help = models.IntegerField(min=0, max=22)
    worker_b_help = models.IntegerField(min=0, max=22)

    # Manager's allocation decision
    allocation_a = models.IntegerField(
        label='Amount given to Worker A (in pence)',
        min=0,
        max=100,
    )
    allocation_b = models.IntegerField(
        label='Amount given to Worker B (in pence)',
        min=0,
        max=100,
    )


DATA_DIRECTORY = Path(__file__).with_name("data")
PAIR_DATA_PATH = DATA_DIRECTORY / "worker_pairs.csv"
ASSIGNMENT_DATA_PATH = DATA_DIRECTORY / "manager_assignments.csv"


def load_worker_pairs() -> list[dict]:
    """Load and validate the fixed pairs created before the oTree session."""
    required_fields = {
        "pair_id",
        "worker_1_id",
        "worker_1_correct",
        "worker_1_help",
        "worker_2_id",
        "worker_2_correct",
        "worker_2_help",
    }
    try:
        pair_file = PAIR_DATA_PATH.open(newline="", encoding="utf-8-sig")
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Missing {PAIR_DATA_PATH}. Run manager/matching/create_random_pairs.py "
            "before starting oTree."
        ) from exc

    with pair_file:
        reader = csv.DictReader(pair_file)
        missing_fields = required_fields.difference(reader.fieldnames or [])
        if missing_fields:
            raise ValueError(
                f"{PAIR_DATA_PATH} is missing columns: {sorted(missing_fields)}"
            )

        pairs = []
        pair_ids = set()
        worker_ids = set()
        for row_number, row in enumerate(reader, start=2):
            try:
                pair = dict(
                    pair_id=int(row["pair_id"]),
                    w1_id=row["worker_1_id"].strip(),
                    w1_correct=int(row["worker_1_correct"]),
                    w1_help=int(row["worker_1_help"]),
                    w2_id=row["worker_2_id"].strip(),
                    w2_correct=int(row["worker_2_correct"]),
                    w2_help=int(row["worker_2_help"]),
                )
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"Invalid value in {PAIR_DATA_PATH} on row {row_number}."
                ) from exc

            if pair["pair_id"] in pair_ids:
                raise ValueError(f"Duplicate pair_id {pair['pair_id']}.")
            pair_ids.add(pair["pair_id"])
            for worker_number in (1, 2):
                worker_id = pair[f"w{worker_number}_id"]
                if not worker_id:
                    raise ValueError(f"Missing worker ID on row {row_number}.")
                if worker_id in worker_ids:
                    raise ValueError(f"Worker {worker_id!r} appears in more than one pair.")
                worker_ids.add(worker_id)
                for measure in ("correct", "help"):
                    value = pair[f"w{worker_number}_{measure}"]
                    if not 0 <= value <= 22:
                        raise ValueError(
                            f"{measure} must be between 0 and 22 on row {row_number}."
                        )
            pairs.append(pair)

    if not pairs:
        raise ValueError(f"No worker pairs were found in {PAIR_DATA_PATH}.")
    return pairs


WORKER_PAIRS = load_worker_pairs()
WORKER_PAIRS_BY_ID = {pair["pair_id"]: pair for pair in WORKER_PAIRS}


def load_manager_assignments() -> dict[tuple[str, int], list[dict]]:
    """Load a schedule in which every worker pair is assigned exactly once."""
    required_fields = {
        "treatment",
        "manager_slot",
        "decision_number",
        "pair_id",
        "worker_1_is_a",
        "assignment_seed",
    }
    try:
        assignment_file = ASSIGNMENT_DATA_PATH.open(
            newline="", encoding="utf-8-sig"
        )
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Missing {ASSIGNMENT_DATA_PATH}. Run "
            "manager/matching/create_manager_assignments.py before starting oTree."
        ) from exc

    assignments_by_manager = {}
    assigned_pair_ids = set()
    assignment_seeds = set()
    valid_treatments = {C.PERFORMANCE_ONLY, C.PERFORMANCE_AND_HELP}
    with assignment_file:
        reader = csv.DictReader(assignment_file)
        missing_fields = required_fields.difference(reader.fieldnames or [])
        if missing_fields:
            raise ValueError(
                f"{ASSIGNMENT_DATA_PATH} is missing columns: {sorted(missing_fields)}"
            )

        for row_number, row in enumerate(reader, start=2):
            treatment = row["treatment"].strip()
            if treatment not in valid_treatments:
                raise ValueError(
                    f"Invalid treatment {treatment!r} on row {row_number}."
                )
            try:
                assignment = dict(
                    treatment=treatment,
                    manager_slot=int(row["manager_slot"]),
                    decision_number=int(row["decision_number"]),
                    pair_id=int(row["pair_id"]),
                    worker_1_is_a=bool(int(row["worker_1_is_a"])),
                    assignment_seed=int(row["assignment_seed"]),
                )
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"Invalid value in {ASSIGNMENT_DATA_PATH} on row {row_number}."
                ) from exc

            if assignment["manager_slot"] < 1:
                raise ValueError(f"manager_slot must be positive on row {row_number}.")
            if row["worker_1_is_a"].strip() not in {"0", "1"}:
                raise ValueError(
                    f"worker_1_is_a must be 0 or 1 on row {row_number}."
                )
            if not 1 <= assignment["decision_number"] <= C.NUM_ROUNDS:
                raise ValueError(
                    f"decision_number must be between 1 and {C.NUM_ROUNDS} "
                    f"on row {row_number}."
                )
            if assignment["pair_id"] not in WORKER_PAIRS_BY_ID:
                raise ValueError(
                    f"Unknown pair_id {assignment['pair_id']} on row {row_number}."
                )
            if assignment["pair_id"] in assigned_pair_ids:
                raise ValueError(
                    f"pair_id {assignment['pair_id']} is assigned more than once."
                )
            assigned_pair_ids.add(assignment["pair_id"])
            assignment_seeds.add(assignment["assignment_seed"])

            manager_key = (treatment, assignment["manager_slot"])
            assignments_by_manager.setdefault(manager_key, []).append(assignment)

    expected_pair_ids = set(WORKER_PAIRS_BY_ID)
    if assigned_pair_ids != expected_pair_ids:
        missing_pair_ids = sorted(expected_pair_ids - assigned_pair_ids)
        raise ValueError(
            f"Every pair must be assigned exactly once. Missing pair IDs: "
            f"{missing_pair_ids}."
        )
    if len(assignment_seeds) != 1:
        raise ValueError(
            f"All rows in {ASSIGNMENT_DATA_PATH} must use the same assignment seed."
        )

    for manager_key, assignments in assignments_by_manager.items():
        assignments.sort(key=lambda assignment: assignment["decision_number"])
        decision_numbers = [
            assignment["decision_number"] for assignment in assignments
        ]
        expected_numbers = list(range(1, len(assignments) + 1))
        if decision_numbers != expected_numbers:
            raise ValueError(
                f"Manager {manager_key} must have consecutive decision numbers "
                f"starting at 1; found {decision_numbers}."
            )
    for treatment in valid_treatments:
        slots = sorted(
            manager_slot
            for assignment_treatment, manager_slot in assignments_by_manager
            if assignment_treatment == treatment
        )
        if slots and slots != list(range(1, len(slots) + 1)):
            raise ValueError(
                f"Manager slots for {treatment!r} must be consecutive starting at 1; "
                f"found {slots}."
            )
    return assignments_by_manager


MANAGER_ASSIGNMENTS = load_manager_assignments()


def creating_session(subsession: Subsession):
    """Copy this round's predetermined assignment into each manager's row."""
    treatment = subsession.session.config["manager_treatment"]
    scheduled_slots = sorted(
        manager_slot
        for assignment_treatment, manager_slot in MANAGER_ASSIGNMENTS
        if assignment_treatment == treatment
    )
    players = subsession.get_players()
    if subsession.round_number == 1 and len(players) != len(scheduled_slots):
        raise ValueError(
            f"The {treatment!r} schedule contains {len(scheduled_slots)} manager "
            f"slots, but this oTree session was created with {len(players)} "
            "participants. Create the session with the scheduled participant count."
        )

    for player in players:
        manager_slot = player.id_in_subsession
        manager_key = (treatment, manager_slot)
        assignments = MANAGER_ASSIGNMENTS.get(manager_key)
        if not assignments:
            raise ValueError(f"No assignments found for manager {manager_key}.")

        assigned_pair_count = len(assignments)
        assignment_seed = assignments[0]["assignment_seed"]
        player.manager_slot = manager_slot
        player.manager_treatment = treatment
        player.assigned_pair_count = assigned_pair_count
        player.assignment_seed = assignment_seed

        assignment = next(
            (
                assignment
                for assignment in assignments
                if assignment["decision_number"] == subsession.round_number
            ),
            None,
        )
        if assignment is None:
            continue

        pair = WORKER_PAIRS_BY_ID[assignment["pair_id"]]
        player.pair_id = pair["pair_id"]
        player.worker_1_is_a = assignment["worker_1_is_a"]

        if assignment["worker_1_is_a"]:
            player.worker_a_id = pair["w1_id"]
            player.worker_a_correct = pair["w1_correct"]
            player.worker_a_help = pair["w1_help"]
            player.worker_b_id = pair["w2_id"]
            player.worker_b_correct = pair["w2_correct"]
            player.worker_b_help = pair["w2_help"]
        else:
            player.worker_a_id = pair["w2_id"]
            player.worker_a_correct = pair["w2_correct"]
            player.worker_a_help = pair["w2_help"]
            player.worker_b_id = pair["w1_id"]
            player.worker_b_correct = pair["w1_correct"]
            player.worker_b_help = pair["w1_help"]


# -----------------------------------------------------------------------------
# PAGES
# -----------------------------------------------------------------------------
class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return dict(total_decisions=player.assigned_pair_count)


class WhatYouWillSee(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return dict(show_help=player.session.config['show_help'])


class YourTask(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            show_help=player.session.config['show_help'],
            total_decisions=player.assigned_pair_count,
        )


class PaymentReminder(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return dict(show_help=player.session.config['show_help'])


class Allocation(Page):
    form_model = 'player'
    form_fields = ['allocation_a', 'allocation_b']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= player.assigned_pair_count

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            show_help=player.session.config['show_help'],
            decision_number=player.round_number,
            total_decisions=player.assigned_pair_count,
        )

    @staticmethod
    def error_message(player: Player, values):
        allocation_a = values.get('allocation_a')
        allocation_b = values.get('allocation_b')

        # Missing values are handled by the required fields themselves.
        if allocation_a is None or allocation_b is None:
            return

        total = allocation_a + allocation_b
        if total != C.TOTAL_PENCE:
            difference = C.TOTAL_PENCE - total
            if difference > 0:
                return (
                    f'The two amounts currently add up to {total}p. '
                    f'Please allocate the remaining {difference}p so that the total is exactly 100p.'
                )
            return (
                f'The two amounts currently add up to {total}p. '
                f'Please reduce the total by {-difference}p so that the total is exactly 100p.'
            )


class Completion(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == player.assigned_pair_count

    @staticmethod
    def vars_for_template(player: Player):
        return dict(total_decisions=player.assigned_pair_count)


page_sequence = [
    Introduction,
    WhatYouWillSee,
    YourTask,
    PaymentReminder,
    Allocation,
    Completion,
]
