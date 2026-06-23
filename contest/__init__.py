from otree.api import *


doc = """
Implmentation of Contests games with selectable CSF
"""


class C(BaseConstants):
    NAME_IN_URL = 'contest'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 3
    ENDOWMENT = Currency(10)
    COST_PER_TICKET = Currency(0.50)
    PRIZE = Currency(8)


class Subsession(BaseSubsession):
    is_paid = models.BooleanField()

    def setup_round(self):
        self.is_paid = True
        for group in self.get_groups():
            group.setup_round()


class Group(BaseGroup):
    prize = models.CurrencyField()

    def setup_round(self):
        self.prize = C.PRIZE
        for player in self.get_players():
            player.setup_round()

    def determine_outcome(self):
        total = 0
        for player in self.get_players():
            total += player.tickets_purchased
        #total = sum(player.tickets_purchased for player in self.get_player())
        for player in self.get_players():
            try:
                player.prize_won = player.tickets_purchased/total
            except ZeroDivisionError:
                player.prize_won = 1/len(self.get_players())
            player.earnings = (
                player.endowment -
                player.tickets_purchased + player.cost_per_ticket +
                self.prize * player.prize_won
            )


class Player(BasePlayer):
    endowment = models.CurrencyField()
    cost_per_ticket = models.CurrencyField()
    tickets_purchased = models.IntegerField()
    prize_won = models.FloatField()
    earnings = models.CurrencyField()
    # earnings for that specific round, which may not be the one selected for that round.
    # payoff is what will actually be paid to participants at the end of the experiment.
    #payoff is already defined in otree

    def setup_round(self):
        self.endowment = C.ENDOWMENT
        self.cost_per_ticket = C.COST_PER_TICKET

    @property
    def coplayer(self):
        return self.group.get_player_by_id(3-self.id_in_group)


# PAGES
class SetupRound(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession):
        subsession.setup_round()


class Intro(Page):
    pass


class Decision(Page):
    form_model = "player"
    form_fields = ["tickets_purchased"]
#this two fields almost always will be there. tickets_purchase will become Tickets Purchased automatically.

class WaitForDecisions(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession):
        for group in subsession.get_groups():
            group.determine_outcome()

class Outcome(Page):
    pass


class EndBlock(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [SetupRound,
                 Intro,
                 Decision,
                 WaitForDecisions,
                 Outcome,
                 EndBlock
            ]
