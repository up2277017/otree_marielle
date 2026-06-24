import random

from otree.api import *


doc = """
Implmentation of Contests games with selectable CSF
"""


class C(BaseConstants):
    NAME_IN_URL = 'contest'
    PLAYERS_PER_GROUP = 2
    #NUM_ROUNDS = 3
    NUM_ROUNDS = 1
    NUM_PAID_ROUNDS = 1
    ENDOWMENT = 10
    COST_PER_TICKET = Currency(0.50)
    PRIZE = Currency(8)


class Subsession(BaseSubsession):
    is_paid = models.BooleanField(initial=False)

    def setup_round(self):
        #self.is_paid = True
        #self.is_paid = self.round_number % 2 == 1
        # this is for paying odd rounds only
        if self.round_number == 1:
            self.setup_paid_rounds()
        for group in self.get_groups():
            group.setup_round()
        self.setup_groups()
        for group in self.get_groups():
            group.setup_round()

    def setup_groups(self):
        self.group_randomly()

    def setup_paid_rounds(self):
        for rd in random.sample(self.in_rounds(1, C.NUM_ROUNDS),
                                k = C.NUM_PAID_ROUNDS):
            rd.is_paid = True


class Group(BaseGroup):
    prize = models.CurrencyField()
    csf = models.StringField()

    def setup_round(self):
        #initialization occurs with setup round
        self.prize = C.PRIZE
        self.csf = self.session.config["csf"]
        # this links back to the setting.py where I have the different types of csf as well. there are three (look at dic...)
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
                player.prize_won = 1
            elif player.tickets_purchased < player.coplayer.tickets_purchased:
                player.prize_won = 0
            else:
                player.prize_won = 0.5
    def determine_outcome_lottery(self):
        try:
            winner = random.choices(self.get_players(),
                                weights = [p.tickets_purchased for p in self.get_players()],
                                k = 1)[0]
        except ValueError:
            winner = random.choices(self.get_players())
        for player in self.get_players():
            if player == winner:
                player.prize_won = 1
            else:
                player.prize_won = 0

    def determine_outcome(self):
        csf = self.session.config["csf"]
        if self.csf == "share":
            self.determine_outcome_share()
        elif self.csf == "allpay":
            self.determine_outcome_allpay()
        elif self.csf == "lottery":
            self.determine_outcome_lottery()
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
        self.endowment = self.session.config.get("endowment", C.ENDOWMENT)
        self.cost_per_ticket = C.COST_PER_TICKET

    @property
    def coplayer(self):
        return self.group.get_player_by_id(3-self.id_in_group)

    @property
    def max_tickets_affordable(self):
        return int(self.endowment / self.cost_per_ticket)

    def in_paid_rounds(self):
        return [rd for rd in self.in_all_rounds() if rd.subsession.is_paid]

    def store_payoffs(self):
        #self.participant.vars["earnings_contest"] = Currency(2)
        self.participant.vars["earnings_contest"] = (
            sum(p.payoff for p in self.in_all_rounds())
        )
    # phython dicitonary to store variables. participant command here for overarching storing variables.
    # participant variable useful to coomunicate info between apps
    # right now its storing 2 pound for all participants


# PAGES
class SetupRound(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession):
        subsession.setup_round()


class Intro(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
    # this is to omit a specific page, this page will only be shown in round 1.


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

    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS
    # C.NUM ROUNDS means that the last round wont be displayed whether last round is 3 or 4 or whatever.
    @staticmethod
    def before_next_page(player,timeout_happened):
        player.store_payoffs()
        #example of calling a function, this function needs to be written in class(player)


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
