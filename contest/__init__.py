from otree.api import *


doc = """
Implmentation of Contests games with selectable CSF
"""


class C(BaseConstants):
    NAME_IN_URL = 'contest'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class SetupRound(WaitPage):
    pass

class Intro(Page):
    pass


class Decision(Page):
    pass


class WaitForDecisions(WaitPage):
    pass

class Outcome(Page):
    pass


class EndBlock(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [SetupRound,
                 Intro,
                 Decision,
                 WaitForDecisions,
                 Outcome,
                 EndBlock
            ]
