from otree.api import *

import random


doc = """
The experiment is a ten-row multiple price list with random-row payment.
"""


class C(BaseConstants):
    NAME_IN_URL = 'assignment_1_mpl'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    NUM_DECISIONS = 10
    HIGH_LOTTERY_PRIZE = Currency(12)
    LOW_LOTTERY_PRIZE = Currency(0)
    WIN_PROB = 50
    SAFE_AMOUNTS = range(1, NUM_DECISIONS + 1)



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

def make_mpl_field(row_number, safe_amount):
    return models.StringField(
        label=f"Decision {row_number}: What option do you choose?",
        choices=[
            [
                "safe",
                f"Receive {safe_amount} for certain",
            ],
            [
                "risky",
                (
                    f"{C.WIN_PROB}% chance of "
                    f"{C.HIGH_LOTTERY_PRIZE}, otherwise "
                    f"{C.LOW_LOTTERY_PRIZE}"
                ),
            ],
        ],
        widget=widgets.RadioSelect,
    )

class Player(BasePlayer):
    choice_mpl_1 = make_mpl_field(
        row_number=1,
        safe_amount=C.SAFE_AMOUNTS[0],
    )

    choice_mpl_2 = make_mpl_field(
        row_number=2,
        safe_amount=C.SAFE_AMOUNTS[1],
    )

    choice_mpl_3 = make_mpl_field(
        row_number=3,
        safe_amount=C.SAFE_AMOUNTS[2],
    )

    choice_mpl_4 = make_mpl_field(
        row_number=4,
        safe_amount=C.SAFE_AMOUNTS[3],
    )

    choice_mpl_5 = make_mpl_field(
        row_number=5,
        safe_amount=C.SAFE_AMOUNTS[4],
    )

    choice_mpl_6 = make_mpl_field(
        row_number=6,
        safe_amount=C.SAFE_AMOUNTS[5],
    )

    choice_mpl_7 = make_mpl_field(
        row_number=7,
        safe_amount=C.SAFE_AMOUNTS[6],
    )

    choice_mpl_8 = make_mpl_field(
        row_number=8,
        safe_amount=C.SAFE_AMOUNTS[7],
    )

    choice_mpl_9 = make_mpl_field(
        row_number=9,
        safe_amount=C.SAFE_AMOUNTS[8],
    )

    choice_mpl_10 = make_mpl_field(
        row_number=10,
        safe_amount=C.SAFE_AMOUNTS[9],
    )

# PAGES
class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [MyPage, ResultsWaitPage, Results]
