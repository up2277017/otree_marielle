from os import environ

SESSION_CONFIGS = [
    # ------------------------------------------------------------------
    # oTree learning curriculum. Start with level 1 and progress in order.
    # Each app is also runnable by itself from oTree's demo page.
    # ------------------------------------------------------------------
    dict(
        name="learning_1_risk",
        display_name="Learning 1 - Individual Risk Choice",
        app_sequence=["learning_1_risk"],
        num_demo_participants=1,
    ),
    dict(
        name="learning_2_public_goods",
        display_name="Learning 2 - Public Goods",
        app_sequence=["learning_2_public_goods"],
        num_demo_participants=4,
    ),
    dict(
        name="learning_3_ultimatum",
        display_name="Learning 3 - Ultimatum Game",
        app_sequence=["learning_3_ultimatum"],
        num_demo_participants=2,
    ),
    dict(
        name="learning_4_auction_live",
        display_name="Learning 4 - Live Ascending Auction",
        app_sequence=["learning_4_auction_live"],
        num_demo_participants=3,
    ),
    dict(
        name="learning_5_trust",
        display_name="Learning 5 - Repeated Trust Game",
        app_sequence=["learning_5_trust"],
        num_demo_participants=2,
        treatment="random",
    ),
    dict(
        name="splash_demo",
        app_sequence=["splash"],
        num_demo_participants=3,
    ),
    dict(
        name="quiz_demo",
        app_sequence=["quiz"],
        num_demo_participants=3,
    ),
    dict(
        name="contest_share_testing",
        app_sequence=["contest"],
        num_demo_participants=2,
        csf="share",
        endowment=10,
    ),
    dict(
        name="contest_allpay_testing",
        app_sequence=["contest"],
        num_demo_participants=2,
        csf="allpay",
        endowment=10,
    ),
    dict(
        name="contest_lottery_testing",
        app_sequence=["contest"],
        num_demo_participants=2,
        csf="lottery",
        endowment=10,
    ),
    dict(
        name="encryption",
        app_sequence=["encryption"],
        num_demo_participants=3,
    ),
    dict(
        name="summary",
        app_sequence=[
            "contest",
            "summary",
        ],
        csf="allpay",
        endowment=10,
        num_demo_participants=2,
    ),
    dict(
        name="manager_performance_only",
        display_name="Manager Study – Performance Only",
        app_sequence=["manager"],
        num_demo_participants=1,
        manager_treatment="performance_only",
        show_help=False,
    ),
    dict(
        name="manager_performance_and_help",
        display_name="Manager Study – Performance and Helping",
        app_sequence=["manager"],
        num_demo_participants=1,
        manager_treatment="performance_and_help",
        show_help=True,
    ),
    dict(
        name="Assignment_1",
        display_name="Assignment 1 - MPL Risk",
        app_sequence=["assignment_1_mpl"],
        num_demo_participants=1,
    ),
    dict(
        name="Basic_assignment",
        display_name="Assignment 0 - Learning OTREE commands",
        app_sequence=["basic_assignment"],
        num_demo_participants=1,
    ),
]
# note that stuff added here can be changed direcly in the browser before the experimet is run.
# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=0.00,
    doc=""
)

PARTICIPANT_FIELDS = [
    "earnings_contest",
    "encryption_contest",
    # Used by learning level 5 to persist information across rounds/apps.
    "trust_treatment",
    "trust_paid_round",
]
#can add earnings_contest and earnings_encryption so that you can use as attribute later in contest and encryption py
SESSION_FIELDS = ["trust_treatment_counts"]
#participant vars and session vars same things can be done

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = "en"

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = "GBP"
USE_POINTS = False

ADMIN_USERNAME = "admin"
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get("OTREE_ADMIN_PASSWORD")

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = "8668690891855"
