from otree.api import Bot

from . import C, Introduction, Offer, Respond, Results


class PlayerBot(Bot):
    def play_round(self):
        if self.round_number == 1:
            yield Introduction, dict(comprehension_answer=0)
        if self.player.role == C.PROPOSER_ROLE:
            yield Offer, dict(offer=8)
        else:
            yield Respond, dict(accepted=True)
        yield Results
