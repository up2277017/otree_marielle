from otree.api import Bot

from . import C, Introduction, PaymentSummary, Results, Return, Send


class PlayerBot(Bot):
    def play_round(self):
        if self.round_number == 1:
            yield Introduction
        if self.player.role == C.INVESTOR_ROLE:
            yield Send, dict(sent_amount=5)
        else:
            yield Return, dict(returned_amount=5)
        yield Results
        if self.round_number == C.NUM_ROUNDS:
            yield PaymentSummary
