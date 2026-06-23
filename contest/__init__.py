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
        #self.is_paid = True
        self.is_paid = self.round_number % 2 == 1
        # this is for paying odd rounds only
        for group in self.get_groups():
            group.setup_round()


class Group(BaseGroup):
    prize = models.CurrencyField()
    csf = models.StringField()

    def setup_round(self):
        #initialization occurs with setup round
        self.prize = C.PRIZE
        self.csf = "allpay"
        #here we can change the type of csf!
        for player in self.get_players():
            player.setup_round()

    def determine_outcome_share(self):
        #share rule
        total = 0
        for player in self.get_players():
            total += player.tickets_purchased
        #total = sum(player.tickets_purchased for player in self.get_player())
        for player in self.get_players():
            try:
                player.prize_won = player.tickets_purchased/total
            except ZeroDivisionError:
                player.prize_won = 1/len(self.get_players())
            

    def determine_outcome_allpay(self):
        for player in self.get_players():
            if player.tickets_purchased > player.coplayer.tickets_purchased:
                player.prize = 1
            elif player.tickets_purchased < player.coplayer.tickets_purchased:
                player.prize = 0
            else:
                player.prize = 0.5

    def determine_outcome(self):
        if self.csf == "share":
            self.determine_outcome_share()
        elif self.csf == "allpay":
            self.determine_outcome_allpay()
        for player in self.get_players():
            player.earnings = (
                player.endowment
                - player.tickets_purchased * player.cost_per_ticket
                + self.prize * player.prize_won
            )
            if self.subsession.is_paid:
                player.payoff = player.earnings


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

    @property
    def max_tickets_affordable(self):
        return int(self.endowment / self.cost_per_ticket)


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

    @staticmethod
    def error_message(player, values):
        if values["tickets_purchased"] < 0:
            return "You cannot buy a negative number of tickets."
# error messages and validation
        if values["tickets_purchased"] > player.max_tickets_affordable:
            return (
                f"Buying {values['tickets_purchased']} tickets would cost "
                f"{values['tickets_purchased'] * player.cost_per_ticket} "
                f"which is more than your endowment of {player.endowment}."
            )
        return None

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
