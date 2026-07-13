from otree.api import *
import random


doc = """
Manager study: participants evaluate 25 pairs of workers and divide 100 pence
between Worker A and Worker B. The session config determines whether helping
information is shown.
"""


class C(BaseConstants):
    NAME_IN_URL = 'manager'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3
    TOTAL_PENCE = 100


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Pair information shown in this round
    pair_id = models.IntegerField()

    # Internal pseudo-worker IDs, stored for later merging but never displayed
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


# -----------------------------------------------------------------------------
# TEMPORARY PSEUDO DATA
# Replace this list later with the real 25 worker pairs from Qualtrics.
# Each worker has: ID, number correct (0-22), and number revealed/helped (0-22).
# -----------------------------------------------------------------------------
PSEUDO_PAIRS = [
    dict(pair_id=1,  w1_id='W001', w1_correct=18, w1_help=4,  w2_id='W002', w2_correct=18, w2_help=16),
    dict(pair_id=2,  w1_id='W003', w1_correct=21, w1_help=0,  w2_id='W004', w2_correct=12, w2_help=0),
    dict(pair_id=3,  w1_id='W005', w1_correct=9,  w1_help=20, w2_id='W006', w2_correct=20, w2_help=3),
    dict(pair_id=4,  w1_id='W007', w1_correct=15, w1_help=10, w2_id='W008', w2_correct=15, w2_help=10),
    dict(pair_id=5,  w1_id='W009', w1_correct=22, w1_help=22, w2_id='W010', w2_correct=6,  w2_help=2),
    dict(pair_id=6,  w1_id='W011', w1_correct=14, w1_help=2,  w2_id='W012', w2_correct=14, w2_help=18),
    dict(pair_id=7,  w1_id='W013', w1_correct=19, w1_help=8,  w2_id='W014', w2_correct=11, w2_help=8),
    dict(pair_id=8,  w1_id='W015', w1_correct=7,  w1_help=22, w2_id='W016', w2_correct=21, w2_help=1),
    dict(pair_id=9,  w1_id='W017', w1_correct=17, w1_help=6,  w2_id='W018', w2_correct=16, w2_help=14),
    dict(pair_id=10, w1_id='W019', w1_correct=10, w1_help=0,  w2_id='W020', w2_correct=10, w2_help=22),
    dict(pair_id=11, w1_id='W021', w1_correct=20, w1_help=5,  w2_id='W022', w2_correct=13, w2_help=17),
    dict(pair_id=12, w1_id='W023', w1_correct=12, w1_help=12, w2_id='W024', w2_correct=12, w2_help=4),
    dict(pair_id=13, w1_id='W025', w1_correct=16, w1_help=19, w2_id='W026', w2_correct=19, w2_help=7),
    dict(pair_id=14, w1_id='W027', w1_correct=8,  w1_help=6,  w2_id='W028', w2_correct=18, w2_help=6),
    dict(pair_id=15, w1_id='W029', w1_correct=22, w1_help=0,  w2_id='W030', w2_correct=22, w2_help=15),
    dict(pair_id=16, w1_id='W031', w1_correct=13, w1_help=9,  w2_id='W032', w2_correct=17, w2_help=9),
    dict(pair_id=17, w1_id='W033', w1_correct=5,  w1_help=21, w2_id='W034', w2_correct=20, w2_help=2),
    dict(pair_id=18, w1_id='W035', w1_correct=18, w1_help=13, w2_id='W036', w2_correct=14, w2_help=5),
    dict(pair_id=19, w1_id='W037', w1_correct=11, w1_help=3,  w2_id='W038', w2_correct=11, w2_help=19),
    dict(pair_id=20, w1_id='W039', w1_correct=19, w1_help=11, w2_id='W040', w2_correct=16, w2_help=1),
    dict(pair_id=21, w1_id='W041', w1_correct=6,  w1_help=15, w2_id='W042', w2_correct=15, w2_help=15),
    dict(pair_id=22, w1_id='W043', w1_correct=21, w1_help=4,  w2_id='W044', w2_correct=9,  w2_help=18),
    dict(pair_id=23, w1_id='W045', w1_correct=14, w1_help=22, w2_id='W046', w2_correct=14, w2_help=0),
    dict(pair_id=24, w1_id='W047', w1_correct=17, w1_help=7,  w2_id='W048', w2_correct=20, w2_help=12),
    dict(pair_id=25, w1_id='W049', w1_correct=8,  w1_help=8,  w2_id='W050', w2_correct=8,  w2_help=14),
]


def creating_session(subsession: Subsession):
    """Assign 25 pseudo pairs to every manager when the session is created."""
    if subsession.round_number != 1:
        return

    #if len(PSEUDO_PAIRS) != C.NUM_ROUNDS:
    if len(PSEUDO_PAIRS) < C.NUM_ROUNDS:
        raise ValueError(
            f"PSEUDO_PAIRS must contain at least {C.NUM_ROUNDS} pairs, "
            f"but it contains {len(PSEUDO_PAIRS)}."
        )

    for first_round_player in subsession.get_players():
        # Each manager sees all 25 pairs in an independently randomized order.
        ordered_pairs = random.sample(PSEUDO_PAIRS, k=C.NUM_ROUNDS)

        for round_number, pair in enumerate(ordered_pairs, start=1):
            player = first_round_player.in_round(round_number)
            player.pair_id = pair['pair_id']

            # Randomize left/right position so the original worker is not always A.
            swap_workers = random.choice([True, False])

            if not swap_workers:
                player.worker_a_id = pair['w1_id']
                player.worker_a_correct = pair['w1_correct']
                player.worker_a_help = pair['w1_help']

                player.worker_b_id = pair['w2_id']
                player.worker_b_correct = pair['w2_correct']
                player.worker_b_help = pair['w2_help']
            else:
                player.worker_a_id = pair['w2_id']
                player.worker_a_correct = pair['w2_correct']
                player.worker_a_help = pair['w2_help']

                player.worker_b_id = pair['w1_id']
                player.worker_b_correct = pair['w1_correct']
                player.worker_b_help = pair['w1_help']


# -----------------------------------------------------------------------------
# PAGES
# -----------------------------------------------------------------------------
class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


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
        return dict(show_help=player.session.config['show_help'])


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
    def vars_for_template(player: Player):
        return dict(
            show_help=player.session.config['show_help'],
            decision_number=player.round_number,
            total_decisions=C.NUM_ROUNDS,
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
        return player.round_number == C.NUM_ROUNDS


page_sequence = [
    Introduction,
    WhatYouWillSee,
    YourTask,
    PaymentReminder,
    Allocation,
    Completion,
]
