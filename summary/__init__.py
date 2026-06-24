from otree.api import *

import contest

#contest.player


doc = """
app to display summary of earnings
"""


class C(BaseConstants):
    NAME_IN_URL = 'summary'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    def collect_results(self):
        for player in self.get_players():
            player.earnings_contest = player.participant.vars.get["earnings_contest", Currency(67)]
            #line above is coming from contest store function!
            #by adding .get we can add a default value for earnings.
            #player.earnings_contest = sum(
            #    p.payoff for p in contest.Player.objects_filter(participant=player.participant)
            #)
            # the line above is another way to access information from other apps.
            # or p.payoff for p in player.in_contest_rounds()
            player.earnings_encryption = player.participant.vars.get["earnings_encryption", Currency(67)]
            player.earnings_encryption = Currency(1.50)
#we can do this at subsession level if we want everyone at the same. but do it player level if everyone can complete at different times.


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    earnings_contest = models.CurrencyField()
    earnings_encryption = models.CurrencyField()

    def in_contest_rounds(self):
        return contest.Player.objects_filter(particpant=self.participant)

# PAGES
class CollectResults(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession):
        subsession.collect_results()


class Results(Page):
    pass


page_sequence = [CollectResults, Results]

# this summary app is very useful to test things without having to go through every app.
