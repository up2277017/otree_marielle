from otree.api import (
    BaseConstants,
    BaseGroup,
    BasePlayer,
    BaseSubsession,
    Currency,
    Page,
    WaitPage,
    models,
    widgets,
)

doc = """
Level 3: a sequential ultimatum game demonstrating roles and conditional pages.
"""


class C(BaseConstants):
    NAME_IN_URL = "learning-ultimatum"
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 3
    PIE = Currency(20)
    PROPOSER_ROLE = "Proposer"
    RESPONDER_ROLE = "Responder"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    offer = models.CurrencyField(
        min=0,
        max=C.PIE,
        label="How much of the £20 pie do you offer to the responder?",
    )
    accepted = models.BooleanField(
        choices=[[True, "Accept"], [False, "Reject"]],
        widget=widgets.RadioSelect,
        label="Do you accept the offer?",
    )


class Player(BasePlayer):
    comprehension_answer = models.IntegerField(
        label="If an offer is rejected, how much does each person earn?",
        choices=[[0, "£0"], [10, "£10"], [20, "£20"]],
        widget=widgets.RadioSelect,
    )

    @property
    def role(self):
        return C.PROPOSER_ROLE if self.id_in_group == 1 else C.RESPONDER_ROLE

    @property
    def other_player(self):
        return self.get_others_in_group()[0]


def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        subsession.group_randomly()
    else:
        subsession.group_like_round(1)


def set_payoffs(group: Group):
    proposer = group.get_player_by_role(C.PROPOSER_ROLE)
    responder = group.get_player_by_role(C.RESPONDER_ROLE)
    if group.accepted:
        proposer.payoff = C.PIE - group.offer
        responder.payoff = group.offer
    else:
        proposer.payoff = Currency(0)
        responder.payoff = Currency(0)


class Introduction(Page):
    form_model = "player"
    form_fields = ["comprehension_answer"]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def comprehension_answer_error_message(player: Player, value):
        if value != 0:
            return "Not quite. A rejection gives both players £0."


class Offer(Page):
    form_model = "group"
    form_fields = ["offer"]

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.PROPOSER_ROLE


class WaitForOffer(WaitPage):
    title_text = "Waiting for the proposal"
    body_text = "The responder can decide after the proposer submits an offer."


class Respond(Page):
    form_model = "group"
    form_fields = ["accepted"]

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.RESPONDER_ROLE

    @staticmethod
    def vars_for_template(player: Player):
        return dict(proposer_keeps=C.PIE - player.group.offer)


class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        set_payoffs(group)


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(proposer_keeps=C.PIE - player.group.offer)


page_sequence = [Introduction, Offer, WaitForOffer, Respond, ResultsWaitPage, Results]
