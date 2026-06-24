import string

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
        self.word = ("ABABA")
        self.lookup_table = string.ascii_uppercase

    @property
    def lookup_dict(self):
        lookup = {}
        for letter in string.ascii_uppercase:
            lookup[letter] = self.lookup_table.index(letter)+1
        return lookup

    @property
    def correct_response(self):
        return [self.lookup_dict[letter] for letter in self.word]
        return [
            self.lookup_dict[self.word[0]],
            self.lookup_dict[self.word[1]],
            self.lookup_dict[self.word[2]],
            self.lookup_dict[self.word[3]],
            self.lookup_dict[self.word[4]],
        ]



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    time_for_task = models.IntegerField()
    response_1 = models.IntegerField()
    response_2 = models.IntegerField()
    response_3 = models.IntegerField()
    response_4 = models.IntegerField()
    response_5 = models.IntegerField()
    is_correct = models.BooleanField()

    @property
    def response_fields(self):
        return [
            "response_1",
            "response_2",
            "response_3",
            "response_4",
            "response_5",
        ]

    @property
    def response(self):
        return [
            self.response_1,
            self.response_2,
            self.response_3,
            self.response_4,
            self.response_5,
        ]

   # def check_response(self):
        self.is_correct(
            self.response_1 == self.subsession.lookup_dict[self.subsession.word[0]] and
            self.response_2 == self.subsession.lookup_dict[self.subsession.word[1]] and
            self.response_3 == self.subsession.lookup_dict[self.subsession.word[2]] and
            self.response_4 == self.subsession.lookup_dict[self.subsession.word[3]] and
            self.response_5 == self.subsession.lookup_dict[self.subsession.word[4]]
        )
        if self.is_correct:
            self.payoff = self.subsession.payment_per_correct

    def check_response(self):
            self.is_correct = self.response == self.subsession.correct_response
            if self.is_correct:
                self.payoff = self.subsession.payment_per_correct

    def creating_session(subsession):
        subsession.setup_round()

# PAGES
class Intro(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class Decision(Page):
    form_model = "player"


    @staticmethod
    def get_form_fields(player):
        return player.response_fields

    @staticmethod
    def before_next_page(player,timeout_happened):
        player.check_response()


class Results(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS


page_sequence = [Intro,
                 Decision,
                 Results]
