import random

from otree.api import (
    BaseConstants,
    BaseGroup,
    BasePlayer,
    BaseSubsession,
    Currency,
    ExtraModel,
    Page,
    WaitPage,
    models,
)

doc = """
Level 4: a real-time ascending auction using liveSend/liveRecv and ExtraModel.
"""


class C(BaseConstants):
    NAME_IN_URL = "learning-live-auction"
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1
    MINIMUM_INCREMENT = Currency(1)
    VALUE_MIN = 12
    VALUE_MAX = 30


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    highest_bid = models.CurrencyField(initial=0)
    highest_bidder_id = models.IntegerField(initial=0)
    auction_finished = models.BooleanField(initial=False)


class Player(BasePlayer):
    private_value = models.CurrencyField()
    bid_count = models.IntegerField(initial=0)


class Bid(ExtraModel):
    """Unlike Player fields, this table can store any number of bid events."""

    group = models.Link(Group)
    player = models.Link(Player)
    amount = models.CurrencyField()
    sequence = models.IntegerField()


def creating_session(subsession: Subsession):
    subsession.group_randomly()
    for player in subsession.get_players():
        player.private_value = Currency(random.randint(C.VALUE_MIN, C.VALUE_MAX))


def auction_state(group: Group, error=None):
    bids = Bid.filter(group=group)
    return dict(
        type="state",
        highest_bid=int(group.highest_bid),
        highest_bidder_id=group.highest_bidder_id,
        bid_count=len(bids),
        can_finish=all(player.bid_count > 0 for player in group.get_players()),
        finished=group.auction_finished,
        error=error,
    )


def finalize_auction(group: Group):
    winner_id = group.highest_bidder_id
    for player in group.get_players():
        if player.id_in_group == winner_id:
            player.payoff = max(Currency(0), player.private_value - group.highest_bid)
        else:
            player.payoff = Currency(0)


class Introduction(Page):
    pass


class Auction(Page):
    @staticmethod
    def live_method(player: Player, data):
        group = player.group
        message_type = data.get("type")

        if message_type == "load":
            return {player.id_in_group: auction_state(group)}

        if group.auction_finished:
            return {player.id_in_group: auction_state(group, "The auction has ended.")}

        if message_type == "bid":
            try:
                amount = Currency(int(data.get("amount")))
            except (TypeError, ValueError):
                return {player.id_in_group: auction_state(group, "Enter a whole-number bid.")}

            minimum = group.highest_bid + C.MINIMUM_INCREMENT
            if amount < minimum:
                return {
                    player.id_in_group: auction_state(
                        group, f"The next bid must be at least {minimum}."
                    )
                }

            group.highest_bid = amount
            group.highest_bidder_id = player.id_in_group
            player.bid_count += 1
            Bid.create(
                group=group,
                player=player,
                amount=amount,
                sequence=len(Bid.filter(group=group)) + 1,
            )
            return {0: auction_state(group)}

        if message_type == "finish":
            if not all(p.bid_count > 0 for p in group.get_players()):
                return {
                    player.id_in_group: auction_state(
                        group, "Every bidder must place at least one bid first."
                    )
                }
            group.auction_finished = True
            finalize_auction(group)
            return {0: auction_state(group)}

        return {player.id_in_group: auction_state(group, "Unknown message.")}


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            won=player.id_in_group == player.group.highest_bidder_id,
            bids=Bid.filter(group=player.group),
        )


page_sequence = [Introduction, Auction, ResultsWaitPage, Results]
