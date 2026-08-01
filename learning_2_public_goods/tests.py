from otree.api import Bot

from . import C, Contribute, FinalSummary, Introduction, Results


class PlayerBot(Bot):
    def play_round(self):
        if self.round_number == 1:
            yield Introduction
        yield Contribute, dict(contribution=10)
        yield Results
        if self.round_number == C.NUM_ROUNDS:
            yield FinalSummary
