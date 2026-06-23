from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'encryption'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3
    PAYMENT_PER_CORRECT = 0.10


class Subsession(BaseSubsession):
    payment_per_correct = models.CurrencyField()
    lookup_table = models.StringField()
    word = models.StringField()

    def setup_round(self):
        self.payment_per_correct = Currency(C.PAYMENT_PER_CORRECT)
        self.word = ("AB")

    @property
    def lookup_dict(self):
        return{"A":1,
               "B":2,
        }

def creating_session(subsession):
    subsession.setup_round()

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    time_for_task = models.IntegerField()
    response_1 = models.IntegerField()
    response_2 = models.IntegerField()
    response_3 = models.IntegerField()
    response_4 = models.IntegerField()
    response_5 = models.IntegerField()
    response_6 = models.IntegerField()


# PAGES
class Intro(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class Decision(Page):
    form_model = "player"
    form_fields = [
        "response_1",
        "response_2",
    ]


class Results(Page):
    pass


page_sequence = [Intro,
                 Decision,
                 Results]
