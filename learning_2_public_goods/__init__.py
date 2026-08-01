from otree.api import (
    BaseConstants,
    BaseGroup,
    BasePlayer,
    BaseSubsession,
    Currency,
    Page,
    WaitPage,
    models,
)

doc = """
Level 2: a repeated linear public-goods game with four-person groups.
"""


class C(BaseConstants):
    NAME_IN_URL = "learning-public-goods"
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 3
    ENDOWMENT = Currency(20)
    MULTIPLIER = 1.6


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()


class Player(BasePlayer):
    contribution = models.CurrencyField(
        min=0,
        max=C.ENDOWMENT,
        label="How much will you contribute to the group account?",
    )


def creating_session(subsession: Subsession):
    """Keep the same randomly formed groups in all three rounds."""
    if subsession.round_number == 1:
        subsession.group_randomly()
    else:
        subsession.group_like_round(1)


def set_payoffs(group: Group):
    players = group.get_players()
    group.total_contribution = sum(player.contribution for player in players)
    group.individual_share = group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP
    for player in players:
        player.payoff = C.ENDOWMENT - player.contribution + group.individual_share


class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Contribute(Page):
    form_model = "player"
    form_fields = ["contribution"]

    @staticmethod
    def vars_for_template(player: Player):
        return dict(rounds_left=C.NUM_ROUNDS - player.round_number)

    @staticmethod
    def error_message(player: Player, values):
        contribution = values["contribution"]
        if contribution % 1 != 0:
            return "For this teaching example, please contribute a whole number of pounds."


class ResultsWaitPage(WaitPage):
    title_text = "Waiting for your group"
    body_text = "The result is calculated when all four contributions have arrived."

    @staticmethod
    def after_all_players_arrive(group: Group):
        set_payoffs(group)


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(other_players=player.get_others_in_group())


class FinalSummary(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        rounds = player.in_all_rounds()
        return dict(
            rounds=rounds,
            total_contributed=sum(p.contribution for p in rounds),
            total_payoff=sum(p.payoff for p in rounds),
        )


page_sequence = [Introduction, Contribute, ResultsWaitPage, Results, FinalSummary]
