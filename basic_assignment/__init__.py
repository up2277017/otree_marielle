from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'basic_assignment'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 2
    ENDOWMENT = Currency(10)
    MAX_CONTRIBUTION = 10
    MIN_CONTRIBUTION = 0
    MAX_SHARED_CONT = 20


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution_group = models.IntegerField()
    equal_share_per_participant = models.IntegerField()


class Player(BasePlayer):
    nickname = models.StringField()
    read_instructions = models.IntegerField(
        label = "Have you read the instructions?",
        choices = [[1, "Yes"], [2, "No"]],
        widget = widgets.RadioSelect(),
    )
    prediction = models.IntegerField(
        label = "How much do you think will be the other participant's contribution?",
        min = 1,
        max = 10,
        widget = widgets.RadioSelectHorizontal(),
    )
    own_contribution = models.IntegerField(
        label = "How much do you want to contribute the shared box",
        min = 1,
        max = 10,
    )
    retained_tokens = models.IntegerField()
    total_contribution = models.IntegerField()
    equal_share = models.CurrencyField()

def calculate_retained_tokens(player: Player):
    player.retained_tokens = C.ENDOWMENT - player.own_contribution
    return player.retained_tokens

def group_calculation(group: Group):
    players_in_group = group.get_players()
    group.total_contribution = 0
    for player in players_in_group:
        group.total_contribution += player.own_contribution
    group.equal_share = 0.5 * group.total_contribution
    for player in players_in_group:
        player.payoff = group.equal_share + player.retained_tokens

def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        subsession.group_randomly()
    else:
        subsession.group_like_round(1)

# PAGES
class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Profile(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    form_model = "player"
    form_fields = ["nickname", "read_instructions"]

    @staticmethod
    def error_message(player: Player, values):
        if values["read_instructions"] == 2:
            return "Make sure you read the instructions!"


class Decision(Page):
    #form_model = "player"
    #form_fields = ["own_contribution", "prediction"]

    @staticmethod
    def get_form_fields(player: Player):
        return ["own_contribution", "prediction"]
    @staticmethod
    def error_message(player: Player, values):
        if values["own_contribution"] < 5:
            return "Your contribution must be 5 or more for this example"

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        calculate_retained_tokens(player)

class PayoffWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        group_calculation(group)

    title_text = "Wait Page"
    body_text = "Please wait for the remaining participants to submit their contributions."

class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        others_players = player.get_others_in_group()
        partner = others_players[0]
        partner_contribution = partner.own_contribution
        return dict(other_contribution = partner_contribution)

class FinalSummary(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    @staticmethod
    def vars_for_template(player):
        all_records = player.in_all_rounds()
        own_contribution_total = sum(player.own_contribution for player in all_records)
        payoff_total = sum(player.payoff for player in all_records)
        return dict(contribution_total_html = own_contribution_total,
                    payoff_total_html = payoff_total)



page_sequence = [Introduction, Profile, Decision, PayoffWaitPage, Results, FinalSummary]
