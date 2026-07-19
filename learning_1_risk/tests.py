from otree.api import Bot, Submission

from . import C, Decision, Introduction, Results


class PlayerBot(Bot):
    def play_round(self):
        yield Introduction
        yield Decision, dict(choice="safe")
        assert self.player.payoff == C.SAFE_AMOUNT
        yield Submission(Results, check_html=False)
