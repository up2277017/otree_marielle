from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'posted_price_assignment'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 3
    SELLER_PROD_COST = Currency(2)
    BUYER_VALUE = Currency(10)
    BUYER_ROLE = "buyer"
    SELLER_ROLE = "seller"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    seller_posted_price = models.CurrencyField(
        label = "For how much would you like to sell your product?",
    )
    buyer_decision = models.IntegerField(
        label = "Do you accept or reject the seller's price",
        choices = [[1, "Accept"], [0, "Reject"]],
        widget = widgets.RadioSelectHorizontal()
    )
    trade_occurred = models.BooleanField()
    buyer_timeout = models.BooleanField(initial=False)

class Player(BasePlayer):
    pass

def seller_posted_price_max(group: Group):
    this_session_price_cap = Currency(group.session.config["price_cap"])
    return this_session_price_cap

def seller_posted_price_min(group: Group):
    return C.SELLER_PROD_COST

#def retrieve_players_by_role(group: Group):
    buyer_players = group.get_player_by_role(C.BUYER_ROLE)
    seller_players = group.get_player_by_role(C.SELLER_ROLE)
    return buyer_players, seller_players

def calculate_outcomes(group: Group):
    buyer_player = group.get_player_by_role(C.BUYER_ROLE)
    seller_player = group.get_player_by_role(C.SELLER_ROLE)
    if group.buyer_decision == 1:
        group.trade_occurred = True
    else:
        group.trade_occurred = False
    if group.trade_occurred:
        buyer_player.payoff = (C.BUYER_VALUE - group.seller_posted_price)
        seller_player.payoff = (group.seller_posted_price - C.SELLER_PROD_COST)
    else:
        buyer_player.payoff = Currency(0)
        seller_player.payoff = Currency(0)


# PAGES
class Introduction(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

class RoleInfo(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class Seller(Page):
    @staticmethod
    def is_displayed(player):
        return player.role == C.SELLER_ROLE
    form_model = "group"
    form_fields = ["seller_posted_price"]
    preserve_unsubmitted_inputs = True

class BuyerWaitPage(WaitPage):
    title_text = "Wait Page"
    body_text = "Please wait for the seller to post their price."

class Buyer(Page):
    @staticmethod
    def is_displayed(player):
        return player.role == C.BUYER_ROLE
    form_model = "group"
    form_fields = ["buyer_decision"]

    @staticmethod
    def get_timeout_seconds(player):
        time = player.session.config["decision_seconds"]
        return time

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.group.buyer_timeout = True
            player.group.buyer_decision = 0
        else:
            player.group.buyer_timeout = False

class CalculateResults(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        calculate_outcomes(group)

class Outcomes(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

        readable_decision = group.field_display("buyer_decision")

        return dict(
            decision_label=readable_decision,
        )

class FinalSummary(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        all_players = player.in_all_rounds()
        total_payoff = sum(player.payoff for player in all_players)
        return dict(all_players=all_players,
                    total_payoff=total_payoff,)

page_sequence = [Introduction, RoleInfo, Seller, BuyerWaitPage, Buyer, CalculateResults, Outcomes, FinalSummary]
