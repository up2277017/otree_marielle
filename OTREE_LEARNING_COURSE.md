# Learning oTree through five behavioral-economics experiments

This course is written for the oTree project in this folder and for oTree 6.0.15.
The examples are deliberately independent of the existing `contest`, `encryption`,
`manager`, `quiz`, `splash`, and `summary` apps.

## How to use the course

For every level:

1. Run the example as a participant.
2. Open the app's `__init__.py` beside its HTML files in PyCharm.
3. Change one small constant, restart the server, and observe the result.
4. Complete the assignment without copying the solution from another app.
5. Run the bots and inspect the downloaded data before moving to the next level.

From PyCharm's terminal in `otree_marielle`, use:

```powershell
.venv\Scripts\otree.exe devserver
```

Open `http://localhost:8000/demo/`. For multiplayer demos, click the session and
open every participant link in a separate browser tab. To run automated players:

```powershell
.venv\Scripts\otree.exe test learning_1_risk
.venv\Scripts\otree.exe test learning_2_public_goods
.venv\Scripts\otree.exe test learning_3_ultimatum
.venv\Scripts\otree.exe test learning_4_auction_live
.venv\Scripts\otree.exe test learning_5_trust
```

The live auction is best tested interactively in three tabs because its purpose is
to teach browser/server messages. oTree's bot runner also requires the optional
`requests` package; if it is absent, install it in your virtual environment before
running these commands.

## The mental model you should learn first

```text
Project
└── Session (one configured run of one or more apps)
    ├── Participant (one human; persists across apps)
    └── App
        ├── Subsession (one round of the app)
        │   └── Group (a set of players in that round)
        │       └── Player (one participant's app/round record)
        └── Pages (the ordered screens and wait points)
```

`Participant` means the person across the whole session. `Player` means that
person's database record in one app and one round. This distinction explains why
level 5 stores its treatment on `participant` but its round earnings on `player`.

## Shared project configuration: `settings.py`

`SESSION_CONFIGS` is a list of dictionaries shown on oTree's demo/session-creation
screen. Important keys are:

- `name`: the internal unique config name.
- `display_name`: the friendly admin-screen name.
- `app_sequence`: app folders run, in order.
- `num_demo_participants`: default number of participant links.
- Custom keys such as `treatment`: available in Python as `session.config["treatment"]`.

`SESSION_CONFIG_DEFAULTS` supplies defaults inherited by every config. Currency
conversion and the participation fee belong here.

`PARTICIPANT_FIELDS` declares values that persist across rounds and apps. Level 5
uses `participant.trust_treatment` and `participant.trust_paid_round`.
`SESSION_FIELDS` does the same for session-wide values; level 5 uses
`session.trust_treatment_counts`.

`REAL_WORLD_CURRENCY_CODE = "GBP"` controls the displayed currency. `USE_POINTS =
False` means oTree displays real-world currency rather than abstract points.

---

# Level 1 — Individual choice under risk

Files: `learning_1_risk/__init__.py`, `Introduction.html`, `Decision.html`,
`Results.html`, and `tests.py`.

## Economic idea

A participant chooses a certain £4 or a lottery paying £10 with 60% probability.
The expected lottery value is £6, but a sufficiently risk-averse person may still
choose £4. This teaches individual decisions before multiplayer synchronization.

## Python, in execution order

`from otree.api import ...` imports oTree building blocks explicitly. Explicit
imports make it clear which names come from oTree.

`doc = "..."` describes the app in oTree's admin interface.

`class C(BaseConstants)` contains fixed parameters:

- `NAME_IN_URL` controls the participant URL fragment.
- `PLAYERS_PER_GROUP = None` makes this an individual task.
- `NUM_ROUNDS = 1` creates one Subsession/Player record per participant.
- `Currency(5)` creates an oTree money value that respects project currency settings.

`Subsession`, `Group`, and `Player` are always declared. Empty models use `pass`.
The decision is stored on `Player` because it belongs to one individual.

`models.StringField(...)` creates a database column and, when included in a form,
an HTML input. `label` is the question text. `choices` stores submitted values on
the left and participant-facing labels on the right. `widgets.RadioSelect` displays
the choices as radio buttons. `IntegerField` and `BooleanField` store the random
draw and whether the lottery won.

`resolve_choice(player)` is an ordinary Python function, not a special oTree hook.
It uses a server-side random draw and sets built-in `player.payoff`. Payoff is the
field oTree automatically aggregates into `participant.payoff`.

`class Decision(Page)` declares a screen. `form_model = "player"` tells oTree where
to save submitted values. `form_fields = ["choice"]` tells it which model field to
render and validate.

`before_next_page(player, timeout_happened)` is an oTree page hook. It runs after a
valid submission and before the next page. This is why the result exists when
`Results` loads.

`vars_for_template` returns a dictionary of extra template variables. The HTML can
use `{{ chosen_option }}` and `{{ total_payment }}`. oTree already supplies
`player`, `group`, `subsession`, `participant`, `session`, and `C` automatically.

`page_sequence` is the exact participant flow. A Page class not listed here will
never be shown.

## HTML commands

`{{ block title }}...{{ endblock }}` fills oTree's page-title area.
`{{ block content }}` fills the main form. `{{ C.ENDOWMENT }}` prints a Python
constant with oTree's currency formatting. `{{ formfields }}` renders every field
listed by the page. `{{ next_button }}` renders the submit button.

The Results table mixes plain HTML with oTree expressions. `{{ player.payoff }}`
reads the database record; `{{ total_payment }}` reads `vars_for_template`.

## Bot

`PlayerBot(Bot)` is an automated participant. `yield Introduction` visits a page.
`yield Decision, dict(choice="safe")` submits a form. The assertion checks the
payoff rule. `Submission(..., check_html=False)` is useful where exact page HTML
checking is unnecessary.

## Assignment 1 — Multiple price list

Build a new individual app with 10 rows. In every row, Option A is a certain amount
that rises from £1 to £10; Option B is always a 50% chance of £12. Ask for one A/B
choice per row, randomly select one row for payment, and report the participant's
first switch from risky to safe.

Requirements:

- Use ten stored fields and `get_form_fields()` to return them dynamically.
- Validate that all ten choices exist.
- Store the randomly paid row and payoff.
- Add a bot for someone who chooses risky in rows 1–6 and safe in rows 7–10.
- Explain why multiple switching can reveal inconsistent choice behavior.

---

# Level 2 — Repeated public-goods game

Files: `learning_2_public_goods/*`.

## Economic idea

Four people each receive £20. Contributions are multiplied by 1.6 and shared
equally. A contributed pound returns £0.40 privately, so free-riding is individually
tempting even though full contribution maximizes total group earnings.

## New Python commands

`PLAYERS_PER_GROUP = 4` makes oTree create four-person groups.
`NUM_ROUNDS = 3` repeats the entire `page_sequence` three times, creating a separate
Subsession, Group, and Player record in every round.

`models.CurrencyField(min=0, max=C.ENDOWMENT)` supplies both server-side validation
and an HTML numeric input. Never rely only on JavaScript validation: browser input
can be altered by participants.

`creating_session(subsession)` is a special app hook run once for every round when
the session is created. `subsession.group_randomly()` shuffles participants in
round 1. `group_like_round(1)` copies that grouping later, producing fixed partners.

`group.get_players()` returns the four Player records. The calculation stores group
outcomes on Group and each individual outcome on `player.payoff`.

`is_displayed(player)` conditionally includes a page. Introduction returns true
only in round 1. If a page is skipped, its other hooks do not run.

`error_message(player, values)` performs multi-field/page-level validation. It
returns a string to reject a submission or returns nothing to accept it. Here it
requires whole-pound contributions. For validation of one field, level 3 shows the
`field_name_error_message` form.

`WaitPage` blocks each player until everyone in that group arrives.
`after_all_players_arrive(group)` runs exactly once for the group, which prevents a
participant from viewing results before every contribution exists. Its argument is
a Group because the default wait scope is one group.

`title_text` and `body_text` customize the built-in wait screen.

`player.get_others_in_group()` returns group members except the current player.
`player.in_all_rounds()` returns this participant's Player objects from all rounds
of this app. It is appropriate in the final-round summary but not for another app.

## New HTML commands

`{{ formfield 'contribution' }}` renders one named field; this gives more layout
control than `{{ formfields }}`.

`{{ for other in other_players }} ... {{ endfor }}` loops through a Python list.
`forloop.last` is true on the last loop item and avoids a trailing comma.
`{{ if ... }} ... {{ endif }}` performs template-side display logic; important
payoff or validation logic should remain in Python.

Bootstrap classes such as `table`, `table-striped`, `alert`, and `card` style pages
without custom CSS because oTree includes Bootstrap.

## Assignment 2 — Public goods with punishment

Extend the game with a second decision stage. After seeing contributions, every
participant receives 5 punishment points and can assign 0–5 points to one other
group member. Each assigned point costs the punisher £1 and reduces the target's
payoff by £3.

Requirements:

- Store punishment decisions on Player and aggregate effects after a second wait.
- Use a dynamic choice list so participants cannot target themselves.
- Prevent spending more than 5 points with server-side validation.
- Show pre-punishment and final payoff separately.
- Keep fixed groups and run for five rounds.
- State a hypothesis about contribution change after punishment becomes possible.

---

# Level 3 — Sequential ultimatum game

Files: `learning_3_ultimatum/*`.

## Economic idea

The proposer divides £20. The responder can accept or reject; rejection destroys
the pie. Subgame-perfect equilibrium with purely self-interested money preferences
predicts a minimal positive offer and acceptance, while experiments often find
fair offers and rejection of low offers.

## New Python commands

Fields can live on `Group`. Both players need access to the same `offer` and
`accepted`, so these decisions belong to their pair rather than either Player.

`@property def role(self)` lets code and templates use `player.role` as if it were a
field. oTree recognizes role values for `group.get_player_by_role(role)`.
`id_in_group` is oTree's built-in position: 1 is proposer and 2 is responder here.

`player.get_others_in_group()[0]` obtains the paired player. For a known position,
`group.get_player_by_id(1)` is another option.

`form_model = "group"` writes the submitted form to the shared Group model. Only
the role whose `is_displayed` returns true sees each decision page.

The ordering `Offer -> WaitForOffer -> Respond` matters. The responder reaches the
wait page without seeing `Respond`; after the proposer submits, both are released,
the proposer skips `Respond`, and the responder sees the stored offer.

`comprehension_answer_error_message(player, value)` is dynamic validation for one
field. The method name must exactly be `<field>_error_message`.

`get_player_by_role` makes payoff code readable. `Currency(0)` explicitly creates a
money zero. The second WaitPage calculates payoffs only after the response exists.

## Assignment 3 — Strategy-method ultimatum game

Create a strategy-method version. Before seeing the actual offer, the responder
states accept/reject for each possible whole-pound offer from £0 to £20. The
proposer then chooses an offer and the matching stored response determines payoffs.

Requirements:

- Generate 21 responder fields or store decisions using an `ExtraModel`.
- Use `get_form_fields()` or raw HTML inputs to avoid repetitive page code.
- Randomize roles across rounds while ensuring each participant experiences both.
- Add a comprehension question with a useful error message.
- Compare direct-response and strategy-method elicitation in your written hypothesis.

---

# Level 4 — Real-time ascending auction

Files: `learning_4_auction_live/*`.

## Economic idea

Three bidders receive private values and openly raise the standing bid. The highest
bidder wins and pays the final bid. This illustrates price discovery, the risk of
overbidding, and real-time strategic interaction.

## New Python commands

`ExtraModel` stores a variable number of records. A Player has one `bid_count`, but
may create any number of `Bid` rows. `models.Link(Group)` and `models.Link(Player)`
link each bid event to its auction and bidder.

`Bid.create(...)` inserts an event. `Bid.filter(group=group)` retrieves events for
one auction. ExtraModels are excellent for clicks, messages, bids, slider movements,
or any event stream that does not fit one fixed column per Player.

`Auction.live_method(player, data)` receives a JavaScript object without submitting
the page. It validates every message on the server. Returning
`{player.id_in_group: message}` replies only to the sender. Returning `{0: message}`
broadcasts to every player in the group.

The message contains a `type`, a common pattern for routing several actions through
one live method. `load` restores state after a refresh, `bid` attempts a bid, and
`finish` ends the auction. The finish branch first checks that every player has bid.

`auction_state` builds one consistent response object. Converting currency to `int`
makes it straightforward to serialize into JSON and display in JavaScript.

`max(Currency(0), value - price)` prevents a negative teaching-demo payoff. In a
real study, decide in advance whether losses are allowed and how they interact with
show-up fees; do not silently impose this floor.

## New HTML and JavaScript commands

`{{ block styles }}` places page CSS in oTree's style area. Element IDs connect the
HTML to JavaScript. `type="button"` is essential: an ordinary button inside the
oTree form would submit the page.

`const myId = {{ player.id_in_group }};` passes a template number into JavaScript.
For larger or sensitive data, prefer a Page `js_vars()` method and access the global
`js_vars` object.

`addEventListener('click', ...)` reacts to browser interaction.
`liveSend({type: 'bid', amount: ...})` sends data through oTree's WebSocket.
`liveRecv(data)` is the specially named browser function oTree calls for server
messages. `textContent` safely updates displayed text.

When `data.finished` becomes true, `document.getElementById('form').submit()` sends
every participant past the live page. The normal WaitPage then ensures all three
have left it before results appear.

The page deliberately omits `{{ next_button }}`. Participants may leave only when
the live protocol finishes.

## Assignment 4 — Continuous double auction

Build a market with three buyers and three sellers. Buyers submit bids, sellers
submit asks, and a trade occurs whenever the best bid is at least the best ask.
Use the midpoint as the transaction price.

Requirements:

- Assign buyer values and seller costs privately.
- Store every order and transaction in separate ExtraModels.
- Broadcast the best bid, best ask, and trade history.
- Reject bids above buyer value and asks below seller cost on the server.
- Let each participant trade at most one unit.
- End automatically when no active buyer/seller pair can trade or a timer expires.
- Export event timestamps so you can reconstruct the order book.

---

# Level 5 — Repeated trust game and research workflow

Files: `learning_5_trust/*`.

## Economic idea

An investor sends part of £10, the experimenter triples it, and a trustee chooses a
return. Backward induction with narrow self-interest predicts no return and hence no
sending. Positive transfers measure trust and trustworthiness, subject to competing
motives such as altruism and inequality aversion.

## New Python commands

Treatment assignment occurs only when `round_number == 1`, then is stored on
`participant`. If it were stored only on Player, a new treatment could be assigned
in every round. A session config value of `identified` or `anonymous` forces a
treatment; `random` balances assignment by participant number.

`session.trust_treatment_counts` is session-wide metadata. It demonstrates a
`SESSION_FIELD`; it should not be used to reveal sensitive treatment information to
participants in a real blinded design.

`participant.trust_paid_round = random.randint(...)` is persistent across rounds.
At the end, `player.in_round(n)` retrieves the Player record from the selected round.
The example zeros every round's built-in payoff and assigns only selected-round
earnings, so oTree's total participant payoff is correct.

`group_randomly(fixed_id_in_group=True)` rematches partners but holds roles fixed.
Without the flag, the randomization would also change Investor/Trustee positions.

`timeout_seconds = 120` displays oTree's timer and automatically submits at zero.
`before_next_page(..., timeout_happened)` records attrition and supplies a defined
zero decision. Timeout behavior is part of the experimental design and must be
documented before data collection.

`returned_amount_max(player)` is dynamic field validation. It overrides the
field's maximum for that particular player/page, because the permitted return
depends on the amount just sent. Dynamic methods exist for `min`, `max`, `choices`,
and `label` using the same `<field>_<property>` naming pattern.

`custom_export(players)` is a generator. Its first `yield` creates CSV headers;
each later `yield` creates one data row. The result appears under oTree Admin → Data
as a custom export. This tidy format repeats identifiers, round, treatment, role,
decisions, outcome, selected round, and timeout status.

## Assignment 5 — Gift exchange with endogenous effort

Design a repeated principal-agent gift-exchange experiment. An employer offers a
wage; a worker accepts/rejects. After acceptance, the worker chooses costly effort.
Compare a fixed-partner treatment with stranger rematching.

Requirements:

- Use at least eight rounds and balanced session-level treatment assignment.
- Keep employer/worker roles fixed but implement fixed partners in one treatment
  and stranger matching in the other.
- Use a nonlinear effort-cost schedule displayed in a table.
- Validate wage and effort dynamically.
- Select one round for payment and include the participation fee.
- Record response times or meaningful decision events with an ExtraModel.
- Write bots for boundary cases, normal play, rejection, and timeout behavior.
- Produce a custom tidy export and a short preregistration: hypotheses, primary
  outcome, exclusion rule, treatment comparison, and planned statistical test.

---

# Core command index

## Models and hierarchy

- `BaseConstants`, `BaseSubsession`, `BaseGroup`, `BasePlayer`
- `models.StringField`, `IntegerField`, `BooleanField`, `CurrencyField`, `Link`
- Field options: `label`, `initial`, `choices`, `min`, `max`, `widget`
- Built-ins: `round_number`, `id_in_group`, `id_in_subsession`, `payoff`
- `get_players`, `get_groups`, `get_others_in_group`, `get_player_by_id`,
  `get_player_by_role`
- `in_round`, `in_all_rounds`, `group_randomly`, `group_like_round`

## Pages and forms

- `Page`, `WaitPage`, `page_sequence`
- `form_model`, `form_fields`, `get_form_fields`
- `is_displayed`, `vars_for_template`, `before_next_page`
- `error_message`, `<field>_error_message`, `<field>_max`
- `timeout_seconds`, `timeout_happened`
- `after_all_players_arrive`, `title_text`, `body_text`

## Templates and browser behavior

- `block title`, `block content`, `block styles`, `block scripts`
- `formfields`, `formfield`, `next_button`
- Variable output, `if`, `for`, Bootstrap HTML/CSS classes
- `liveSend`, `liveRecv`, DOM events, state updates, programmatic form submission

## Data and research operations

- `creating_session`, `session.config`
- `PARTICIPANT_FIELDS`, `SESSION_FIELDS`
- `participant`, `session`, `ExtraModel.create/filter`
- `custom_export`, `Bot`, `Submission`

This is the core oTree toolkit, not every API feature. Features intentionally left
for a later advanced course include `group_by_arrival_time`, rooms and participant
labels, chat, `read_csv`, `js_vars`, asynchronous live methods, REST export,
internationalization, custom admin reports, `app_after_this_page`, browser back
buttons, and deployment. You now have the concepts needed to learn those without
treating them as mysterious syntax.

## Debugging checklist

1. Read the first traceback line that points to your app, not only the final line.
2. Check indentation: a page hook accidentally nested in another function will not run.
3. Confirm every form field exists on the model named by `form_model`.
4. Confirm every Page is in `page_sequence` and has a same-named HTML file.
5. Put shared calculations after a WaitPage, when all required decisions exist.
6. Validate in Python even if JavaScript also validates.
7. After changing model fields, reset the development database only when it is safe
   to discard development sessions: `otree resetdb`.
8. Run bots, then manually test multiplayer timing with several tabs.
9. Download data and verify one row by hand before recruiting participants.
10. Freeze parameters, instructions, exclusion rules, and payment logic before launch.

## Official documentation

- oTree documentation: <https://otree.readthedocs.io/en/latest/>
- Models: <https://otree.readthedocs.io/en/latest/models.html>
- Pages: <https://otree.readthedocs.io/en/latest/pages.html>
- Forms: <https://otree.readthedocs.io/en/latest/forms.html>
- Groups: <https://otree.readthedocs.io/en/latest/multiplayer/groups.html>
- Wait pages: <https://otree.readthedocs.io/en/latest/multiplayer/waitpages.html>
- Live pages: <https://otree.readthedocs.io/en/latest/live.html>
