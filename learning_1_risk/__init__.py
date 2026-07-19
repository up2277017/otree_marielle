import random

from otree.api import (
    BaseConstants,
    BaseGroup,
    BasePlayer,
    BaseSubsession,
    Currency,
    Page,
    models,
    widgets,
)

doc = """
Level 1: an individual risky-choice task. Participants choose between a safe and
a risky lottery. One lottery is resolved and paid.
"""


class C(BaseConstants):
    NAME_IN_URL = "learning-risk"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    ENDOWMENT = Currency(5)
    SAFE_AMOUNT = Currency(4)
    HIGH_PRIZE = Currency(10)
    LOW_PRIZE = Currency(0)
    HIGH_PRIZE_PROBABILITY = 60


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    choice = models.StringField(
        label="Which option do you choose?",
        choices=[
            ["safe", "Option A: receive £4 for certain"],
            ["risky", "Option B: 60% chance of £10, otherwise £0"],
        ],
        widget=widgets.RadioSelect,
    )
    random_draw = models.IntegerField()
    lottery_won = models.BooleanField()


def resolve_choice(player: Player):
    """Make one server-side random draw and set this round's payoff."""
    player.random_draw = random.randint(1, 100)
    if player.choice == "safe":
        player.lottery_won = False
        player.payoff = C.SAFE_AMOUNT
    else:
        player.lottery_won = player.random_draw <= C.HIGH_PRIZE_PROBABILITY
        player.payoff = C.HIGH_PRIZE if player.lottery_won else C.LOW_PRIZE


class Introduction(Page):
    pass


class Decision(Page):
    form_model = "player"
    form_fields = ["choice"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        resolve_choice(player)


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            chosen_option="safe amount" if player.choice == "safe" else "lottery",
            total_payment=C.ENDOWMENT + player.payoff,
        )


page_sequence = [Introduction, Decision, Results]
