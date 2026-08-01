from otree.api import Bot, Submission

from . import Auction, Introduction, Results


class PlayerBot(Bot):
    """A smoke bot; use three real browser tabs to exercise WebSocket bidding."""

    def play_round(self):
        yield Introduction
        yield Submission(Auction, check_html=False)
        yield Results
