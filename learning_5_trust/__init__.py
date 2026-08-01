import random

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
Level 5: a repeated trust game with treatments, rematching, timeouts,
cross-round payment selection, and a custom data export.
"""


class C(BaseConstants):
    NAME_IN_URL = "learning-repeated-trust"
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 5
    ENDOWMENT = Currency(10)
    MULTIPLIER = 3
    DECISION_TIMEOUT = 120
    TRUSTEE_ROLE = "Trustee"
    INVESTOR_ROLE = "Investor"
    IDENTIFIED = "identified"
    ANONYMOUS = "anonymous"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    sent_amount = models.CurrencyField(min=0, max=C.ENDOWMENT)
    returned_amount = models.CurrencyField(min=0)
    tripled_amount = models.CurrencyField()


class Player(BasePlayer):
    round_earnings = models.CurrencyField(initial=0)
    timed_out = models.BooleanField(initial=False)

    @property
    def role(self):
        return C.INVESTOR_ROLE if self.id_in_group == 1 else C.TRUSTEE_ROLE

    @property
    def treatment(self):
        return self.participant.trust_treatment


def creating_session(subsession: Subsession):
    """Assign persistent treatments/payment rounds and create stranger matching."""
    if subsession.round_number == 1:
        counts = {C.IDENTIFIED: 0, C.ANONYMOUS: 0}
        configured_treatment = subsession.session.config.get("treatment", "random")
        for player in subsession.get_players():
            if configured_treatment in [C.IDENTIFIED, C.ANONYMOUS]:
                treatment = configured_treatment
            else:
                treatment = C.IDENTIFIED if player.id_in_subsession % 2 else C.ANONYMOUS
            player.participant.trust_treatment = treatment
            player.participant.trust_paid_round = random.randint(1, C.NUM_ROUNDS)
            counts[treatment] += 1
        subsession.session.trust_treatment_counts = counts
        subsession.group_randomly()
    else:
        # Re-match across groups while keeping investors as investors and trustees as trustees.
        subsession.group_randomly(fixed_id_in_group=True)


def set_round_earnings(group: Group):
    investor = group.get_player_by_role(C.INVESTOR_ROLE)
    trustee = group.get_player_by_role(C.TRUSTEE_ROLE)
    investor.round_earnings = C.ENDOWMENT - group.sent_amount + group.returned_amount
    trustee.round_earnings = group.tripled_amount - group.returned_amount


def set_final_payoff(player: Player):
    """Only the participant's pre-selected random round counts for payment."""
    paid_round = player.participant.trust_paid_round
    for round_player in player.in_all_rounds():
        round_player.payoff = Currency(0)
    paid_player = player.in_round(paid_round)
    paid_player.payoff = paid_player.round_earnings


def counterpart_label(player: Player):
    """Return a stable code only in the identified-information treatment."""
    if player.treatment == C.IDENTIFIED:
        other_player = player.get_others_in_group()[0]
        return f"Participant {other_player.participant.code}"
    return "Anonymous participant"


class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return dict(treatment_counts=player.session.trust_treatment_counts)


class Send(Page):
    form_model = "group"
    form_fields = ["sent_amount"]
    timeout_seconds = C.DECISION_TIMEOUT

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.INVESTOR_ROLE

    @staticmethod
    def vars_for_template(player: Player):
        return dict(counterpart_label=counterpart_label(player))

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.timed_out = True
            player.group.sent_amount = Currency(0)


class WaitForInvestor(WaitPage):
    pass


class Return(Page):
    form_model = "group"
    form_fields = ["returned_amount"]
    timeout_seconds = C.DECISION_TIMEOUT

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.TRUSTEE_ROLE

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        group.tripled_amount = group.sent_amount * C.MULTIPLIER
        return dict(
            maximum_return=group.tripled_amount,
            counterpart_label=counterpart_label(player),
        )

    @staticmethod
    def returned_amount_max(player: Player):
        return player.group.sent_amount * C.MULTIPLIER

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.timed_out = True
            player.group.returned_amount = Currency(0)


class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        # Compute here because both decisions are now guaranteed to exist.
        group.tripled_amount = group.sent_amount * C.MULTIPLIER
        set_round_earnings(group)


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(counterpart_label=counterpart_label(player))

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.round_number == C.NUM_ROUNDS:
            set_final_payoff(player)


class PaymentSummary(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        paid_round = player.participant.trust_paid_round
        return dict(
            all_rounds=player.in_all_rounds(),
            paid_round=paid_round,
            paid_earnings=player.in_round(paid_round).round_earnings,
        )


def custom_export(players):
    """Create a tidy, researcher-friendly CSV in oTree's Data > Custom export."""
    yield [
        "session_code",
        "participant_code",
        "round",
        "treatment",
        "role",
        "sent",
        "returned",
        "round_earnings",
        "paid_round",
        "timed_out",
    ]
    for player in players:
        yield [
            player.session.code,
            player.participant.code,
            player.round_number,
            player.treatment,
            player.role,
            player.group.sent_amount,
            player.group.returned_amount,
            player.round_earnings,
            player.participant.trust_paid_round,
            player.timed_out,
        ]


page_sequence = [
    Introduction,
    Send,
    WaitForInvestor,
    Return,
    ResultsWaitPage,
    Results,
    PaymentSummary,
]
