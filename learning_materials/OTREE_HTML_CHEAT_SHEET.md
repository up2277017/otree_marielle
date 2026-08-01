# oTree and HTML Cheat Sheet

This is a reference sheet, not a complete app. Syntax examples are generic and
are not solutions to the Command Gym assignment.

## 1. Terminal commands

| Command | Purpose |
|---|---|
| `otree startapp app_name` | Create a new app folder |
| `otree devserver` | Run the local development server |
| `otree test config_name` | Run bots for a session configuration |
| `otree test config_name --export` | Run bots and export their data |
| `otree resetdb` | Delete development-session data and recreate the schema |

### Windows virtual-environment form

In this project, prefix commands with the executable in `.venv\Scripts`.

```powershell
.\.venv\Scripts\otree.exe startapp app_name
.\.venv\Scripts\otree.exe devserver
```

### Warning about `resetdb`

`resetdb` is destructive. Back up `db.sqlite3` if the development data matters.
For disposable practice, an in-memory development database is safer.

---

# 2. `settings.py`

## `SESSION_CONFIGS`

A list of dictionaries describing runnable session configurations.

| Key | Meaning |
|---|---|
| `name` | Unique internal configuration name |
| `display_name` | Readable Admin name |
| `app_sequence` | Ordered list of app-folder names |
| `num_demo_participants` | Default demo participant count |
| `participation_fee` | Fixed participation payment |
| `real_world_currency_per_point` | Point-to-money conversion |
| `doc` | Researcher-facing configuration explanation |
| Custom key | Your own session parameter |

Minimal example:

```python
SESSION_CONFIGS = [
    dict(
        name="practice",
        display_name="Practice session",
        app_sequence=["practice_app"],
        num_demo_participants=2,
    ),
]
```

### Parameters that change between sessions

Define custom parameters in the session configurations in `settings.py`, then
read the selected configuration's values inside the app. Two configurations
can run the same app with different parameters:

```python
SESSION_CONFIGS = [
    dict(
        name="low_cap",
        display_name="Low price cap",
        app_sequence=["market_app"],
        num_demo_participants=2,
        price_cap=8,
    ),
    dict(
        name="high_cap",
        display_name="High price cap",
        app_sequence=["market_app"],
        num_demo_participants=2,
        price_cap=10,
    ),
]
```

When a session is created, its selected configuration is available in the app
through `session.config`. Access it from whichever object your function
receives:

```python
# Function receives Player
price_cap = player.session.config["price_cap"]

# Function receives Group
price_cap = group.session.config["price_cap"]

# Function receives Subsession
price_cap = subsession.session.config["price_cap"]
```

Use square brackets when the parameter is required. Use `.get()` when a
fallback is appropriate:

```python
session.config["parameter_name"]
session.config.get("parameter_name", fallback)
```

### Python access versus HTML access

In Python, access a required configuration key with square brackets:

```python
price_cap = player.session.config["price_cap"]
```

In an oTree HTML template, use dot notation instead:

```html
<p>The price cap is {{ session.config.price_cap }}.</p>
```

Do not copy the Python square-bracket expression directly into a template:

```html
<!-- Do not use this Python syntax in an oTree template. -->
{{ session.config["price_cap"] }}
```

If the value needs conversion, calculation, or a convenient display name, read
it in `vars_for_template()` and return it to HTML:

```python
class ExamplePage(Page):

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            displayed_cap=cu(player.session.config["price_cap"]),
        )
```

```html
<p>The price cap is {{ displayed_cap }}.</p>
```

The selected value is shared by all participants in that created session. A
different session can select a different configuration while running exactly
the same app code.

Use `C` for a value fixed across every session running the app. Use a custom
`session.config` parameter when the researcher should be able to vary the value
between sessions.

## `SESSION_CONFIG_DEFAULTS`

Values inherited by every session configuration unless overridden.

```python
SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=0.00,
)
```

## `PARTICIPANT_FIELDS`

Names of values that persist for one participant across rounds and apps.

```python
PARTICIPANT_FIELDS = ["treatment"]

participant.some_name = value
player.participant.some_name = value
```

The name must first appear in `PARTICIPANT_FIELDS`. For example, after
declaring `"treatment"`, use `player.participant.treatment` in an app.

## `SESSION_FIELDS`

Names of values shared by the whole session.

```python
SESSION_FIELDS = ["market_condition"]

session.some_name = value
player.session.some_name = value
```

The name must first appear in `SESSION_FIELDS`. Every participant then reads
the same session-level value.

## Project-wide settings

| Setting | Meaning |
|---|---|
| `LANGUAGE_CODE` | Project language |
| `REAL_WORLD_CURRENCY_CODE` | GBP, EUR, USD, etc. |
| `USE_POINTS` | Display Currency as points or money |
| `ADMIN_USERNAME` | Admin username |
| `ADMIN_PASSWORD` | Admin password |
| `SECRET_KEY` | Application security key |

---

# 3. App structure

Every app normally declares:

```python
class C(BaseConstants):
    ...

class Subsession(BaseSubsession):
    ...

class Group(BaseGroup):
    ...

class Player(BasePlayer):
    ...
```

## Object hierarchy

```text
Session
└── App
    └── Subsession (one round)
        └── Group
            └── Player
```

Participant represents the human across the complete session. Player represents
that human in one app round.

---

# 4. Constants

| Constant | Purpose |
|---|---|
| `C.NAME_IN_URL` | App URL name |
| `C.PLAYERS_PER_GROUP` | Group size; `None` for individual/all-in-one-group |
| `C.NUM_ROUNDS` | Number of app rounds |
| Your own constant | Fixed app parameter |

Use `C` for fixed parameters. Use `session.config` for parameters intended to
vary between sessions.

---

# 5. Model fields

| Field | Stores |
|---|---|
| `models.StringField()` | Short text |
| `models.LongStringField()` | Multi-line/long text |
| `models.IntegerField()` | Whole number |
| `models.FloatField()` | Decimal number |
| `models.DecimalField()` | Exact configurable decimal |
| `models.CurrencyField()` | oTree Currency |
| `models.BooleanField()` | True/False |

## Choosing which object owns a field

| Location | Use it when the value belongs to |
|---|---|
| `Player` | One participant in one app round |
| `Group` | One group in one app round |
| `Subsession` | The whole session within one app round |
| Participant field | One participant across rounds and apps |
| Session field | The whole session across apps and rounds |

For example, an individual decision belongs on Player, while a total shared by
all members of a group belongs on Group. The model name used in calculations
must match the field's declaration:

```python
def store_example(player: Player, group: Group):
    player.individual_decision = 5
    group.group_total = 10
```

`player.group_total` and `group.group_total` would be two different fields.

## Currency fields and Currency values

`models.CurrencyField()` declares a database field. `cu(...)` creates an oTree
Currency value that can be stored in that field or in `player.payoff`:

```python
class Player(BasePlayer):
    earnings = models.CurrencyField()


def set_earnings(player: Player):
    player.earnings = cu(2.5)
    player.payoff = player.earnings
```

Use `IntegerField` for whole-number responses and `CurrencyField` for points,
tokens, or money that may enter the payoff.

## Common field options

```python
models.IntegerField(
    label="Question shown to participant",
    initial=0,
    min=0,
    max=100,
    choices=[[1, "First"], [2, "Second"]],
)
```

| Option | Meaning |
|---|---|
| `label` | Participant-facing question |
| `initial` | Starting/default stored value |
| `min` | Minimum valid value |
| `max` | Maximum valid value |
| `choices` | Allowed stored/displayed pairs |
| `blank=True` | Permit an empty value where supported |
| `widget=widgets.RadioSelect` | Show radio buttons |
| `widget=widgets.RadioSelectHorizontal` | Horizontal radio buttons |

## Stored value versus displayed label

```python
choices=[
    ["internal_a", "Participant sees A"],
    ["internal_b", "Participant sees B"],
]
```

The database stores the left value.

---

# 6. Built-in attributes

## Player

| Command | Meaning |
|---|---|
| `player.payoff` | Official payoff in this round |
| `player.round_number` | Current round |
| `player.id_in_group` | Position inside the group |
| `player.id_in_subsession` | Position in the round |
| `player.group` | Current Group |
| `player.subsession` | Current Subsession |
| `player.participant` | Persistent Participant |
| `player.session` | Current Session |

## Subsession

A Subsession represents one round of one app for the entire session.

| Command | Meaning |
|---|---|
| `subsession.round_number` | Current app round; round numbers begin at `1` |
| `subsession.session` | The overall Session containing this Subsession |
| `subsession.get_players()` | All Player objects in the current round |
| `subsession.get_groups()` | All Group objects in the current round |

A custom field placed in `Subsession` stores one value for the whole session
in each round:

```python
class Subsession(BaseSubsession):
    market_price = models.CurrencyField()
```

If the app has three rounds, it has three separate Subsession objects, so it
can have three separate `market_price` values.

## Participant

| Command | Meaning |
|---|---|
| `participant.code` | Random participant code |
| `participant.label` | External/room label if supplied |
| `participant.id_in_session` | Position in session |
| `participant.payoff` | Sum of round payoffs |
| `participant.payoff_plus_participation_fee()` | Converted payoff plus fee |

## Session

| Command | Meaning |
|---|---|
| `session.code` | Session code |
| `session.num_participants` | Actual participant count |
| `session.config` | Session configuration dictionary |

---

# 7. Getting Players and Groups

| Command | Returns |
|---|---|
| `subsession.get_players()` | All Players in the round |
| `subsession.get_groups()` | All Groups in the round |
| `group.get_players()` | Players in one group, ordered by `id_in_group` |
| `group.get_player_by_id(n)` | Player with position `n` |
| `group.get_player_by_role(role)` | Player whose `role` matches |
| `player.get_others_in_group()` | Other Players in the same group |
| `player.get_others_in_subsession()` | Other Players in the round |

These methods return Player objects or lists of Player objects:

```python
players = group.get_players()
player_2 = group.get_player_by_id(2)
other_players = player.get_others_in_group()
```

In a two-player group, retrieve the single partner with:

```python
partner = player.get_others_in_group()[0]
partner_decision = partner.some_field
```

---

# 8. Group formation

| Command | Meaning |
|---|---|
| `subsession.group_randomly()` | Randomize groups and positions |
| `subsession.group_randomly(fixed_id_in_group=True)` | Rematch while keeping positions |
| `subsession.group_like_round(n)` | Copy matching from round `n` |
| `subsession.get_group_matrix()` | Inspect group arrangement |
| `subsession.set_group_matrix(matrix)` | Set group arrangement |
| `group.set_players(players)` | Reorder Player objects within one Group |

Common fixed-matching pattern:

```python
def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        subsession.group_randomly()
    else:
        subsession.group_like_round(1)
```

This randomizes groups in round 1 and copies those groups into every later
round.

To inspect or modify a complete grouping:

```python
matrix = subsession.get_group_matrix()
matrix[0].reverse()
subsession.set_group_matrix(matrix)
```

Each inner list is one group. When setting a matrix, include every Player
exactly once.

## Session-creation hook

```python
def creating_session(subsession: Subsession):
    ...
```

Runs once for every app round when the session is created.

### Using `subsession.round_number` in Python

`subsession.round_number` gives the number of the round currently being
created. It is especially useful inside `creating_session()` because oTree
calls that function separately for every round.

```python
def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        # Instructions here run only while round 1 is being created.
        ...
```

You can use it to give different rounds different settings or to select a
round-specific item from a Python list:

```python
value_for_this_round = C.ROUND_VALUES[subsession.round_number - 1]
```

The `- 1` is necessary because oTree round numbers begin at `1`, whereas
Python list indexes begin at `0`. In functions that receive a `player`, the
equivalent current-round attribute is `player.round_number`.

---

# 9. Across-round commands

These operate within the same app.

| Command | Returns |
|---|---|
| `player.in_round(n)` | This participant's Player in round `n` |
| `player.in_rounds(a, b)` | Player records from rounds `a` through `b` |
| `player.in_previous_rounds()` | Player records before the current round |
| `player.in_all_rounds()` | Player records from every app round |
| `subsession.in_round(n)` | The app's Subsession in round `n` |
| `subsession.in_rounds(a, b)` | Subsessions from rounds `a` through `b` |
| `subsession.in_previous_rounds()` | Subsessions before the current round |
| `subsession.in_all_rounds()` | Subsessions from every app round |

Examples:

```python
if player.round_number > 1:
    previous_player = player.in_round(player.round_number - 1)
    previous_payoff = previous_player.payoff

all_player_records = player.in_all_rounds()
total_payoff = sum(p.payoff for p in all_player_records)
```

`in_rounds(2, 4)` includes rounds 2, 3, and 4. These methods return separate
database objects from those rounds; they do not copy values into the current
round.

The same method family also exists for Group, but Group history is hard to
interpret if groups are reshuffled.

Use participant fields—not `in_all_rounds()`—to move data between apps.

---

# 10. Ordinary helper functions

## Defining a function versus making it run

`def` creates a Python function. The colon begins its indented body, but
neither `def` nor the colon executes the function.

There are three important categories in an oTree app:

| Function category | Naming rule | Who calls it? |
|---|---|---|
| Ordinary Python helper | You choose the name | Your own code must call it |
| oTree hook | Must use an exact oTree name | oTree calls it automatically |
| Field-specific function | Exact field name plus a special suffix | oTree calls it for that field |

An ordinary helper can have a name you choose:

```python
def calculate_bonus(player: Player):
    player.bonus = player.score * 2
```

It runs only when another part of the code calls it:

```python
calculate_bonus(player)
```

An oTree hook has a reserved name and runs at the corresponding point in the
experiment:

```python
def creating_session(subsession: Subsession):
    # oTree calls this when it creates each app round.
    ...
```

Other exact-name hooks include `is_displayed`, `vars_for_template`,
`before_next_page`, `get_timeout_seconds`, and
`after_all_players_arrive`.

A field-specific function combines the exact field name with an oTree suffix:

```text
Field:     offer
Functions: offer_min, offer_max, offer_choices, offer_error_message
```

For example, `offer_max(...)` supplies the maximum for `offer`. A differently
named function such as `maximum_offer(...)` is valid ordinary Python, but
oTree will not automatically connect it to the field.

## Calling ordinary helpers

Use ordinary Python functions for economic logic:

```python
def calculate_something(player: Player):
    ...

def calculate_group_outcome(group: Group):
    ...
```

They do not run automatically. A Page hook, WaitPage hook, or another called
function must execute them.

For example, a Player calculation can be called from `before_next_page()`:

```python
class Decision(Page):

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        calculate_something(player)
```

A Group calculation that needs every group member's decision is normally
called from a WaitPage's `after_all_players_arrive()`.

---

# 11. Page basics

```python
class SomePage(Page):
    pass
```

A Page named `SomePage` normally uses `SomePage.html`.

## `page_sequence`

```python
page_sequence = [FirstPage, DecisionPage, ResultsPage]
```

The sequence repeats every round.

---

# 12. Page forms

## Fixed fields

```python
class Decision(Page):
    form_model = "player"
    form_fields = ["field_a", "field_b"]
```

Use `"group"` if the fields are declared on Group.

## Dynamic fields

```python
class Decision(Page):
    form_model = "player"

    @staticmethod
    def get_form_fields(player: Player):
        if player.round_number == 1:
            return ["field_a"]
        return ["field_b"]
```

This replaces the fixed `form_fields` attribute. Both returned names must
already be declared fields on the stated `form_model`.

## Important rule

`{{ formfields }}` renders only the fields selected by the current Page. It does
not render every model field.

---

# 13. Principal Page methods

## Conditional display

```python
class Instructions(Page):

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
```

This example shows the Page only in round 1. If the function returns `False`,
the Page and its `before_next_page` are skipped.

## Pass values to HTML

Each item in the returned dictionary creates a template variable. The name on
the left is used in HTML, and the value on the right is the Python value sent
to that variable:

```python
class ExampleResults(Page):

    @staticmethod
    def vars_for_template(player: Player):
        doubled_value = player.decision * 2
        return dict(
            value_for_display=doubled_value,
        )
```

The matching HTML uses the dictionary key:

```html
<p>The doubled value is {{ value_for_display }}.</p>
```

`vars_for_template()` is also useful when the value is not automatically
available under a convenient name. For example, retrieve another Player inside
the function and pass one of that Player's fields to HTML:

```python
class ExampleResults(Page):

    @staticmethod
    def vars_for_template(player: Player):
        other_players = player.get_others_in_group()
        other_player = other_players[0]
        return dict(
            other_decision=other_player.decision,
        )
```

The matching HTML is:

```html
<p>The other participant chose {{ other_decision }}.</p>
```

`get_others_in_group()` returns a list. Using `[0]` is appropriate when groups
contain exactly two Players, because there is exactly one other Player.

You do not need `vars_for_template()` for objects that oTree already supplies
to every template. These can be read directly in HTML:

```html
{{ player.some_field }}
{{ group.some_field }}
{{ subsession.round_number }}
{{ participant.code }}
{{ session.code }}
{{ C.SOME_CONSTANT }}
```

Values created only inside `vars_for_template()` are display-only unless the
calculation is also assigned to a declared model, participant, or session
field.

Refreshing the Page runs `vars_for_template` again.

## Pass values to JavaScript

```python
class ExamplePage(Page):

    @staticmethod
    def js_vars(player: Player):
        return dict(limit=C.MAXIMUM_VALUE)
```

HTML JavaScript reads:

```javascript
console.log(js_vars.limit);
```

`js_vars()` sends data to browser JavaScript. It does not store values sent
back by JavaScript; use a form field or a live method for that.

## Run logic after a valid submission

`before_next_page()` runs on the server after the participant submits the
Page, after normal form validation and saving, but before oTree moves the
participant to the next Page.

Typical uses include:

- calculating and storing a result from the submitted fields;
- setting `player.payoff`;
- copying a value to a declared participant or session field;
- calling an ordinary helper function, such as a decision resolver;
- handling a Page timeout.

Example:

```python
class Decision(Page):
    form_model = "player"
    form_fields = ["choice"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.choice = 0
        calculate_result(player)
```

`timeout_happened` is a Boolean:

- `False`: the participant submitted the Page normally;
- `True`: the Page was automatically submitted because its timer expired.

On a timeout, form values may be missing or replaced with type-specific empty
values, so set a deliberate fallback before performing calculations when
necessary.

If `is_displayed()` returns `False`, the Page is skipped and its
`before_next_page()` does not run. The function normally changes stored
objects directly and does not need to return anything.

The HTML connection is:

1. `{{ formfields }}` or `{{ formfield "field_name" }}` displays the inputs.
2. `{{ next_button }}` submits the form.
3. oTree validates and saves the submitted model fields.
4. `before_next_page()` runs in Python.
5. oTree proceeds to the next Page in `page_sequence`.

## Static timeout

```python
class TimedDecision(Page):
    timeout_seconds = 60
```

This automatically submits the Page after 60 seconds.

## Dynamic timeout

```python
class TimedDecision(Page):

    @staticmethod
    def get_timeout_seconds(player: Player):
        if player.round_number == 1:
            return 60
        return 30
```

Use `get_timeout_seconds()` instead of `timeout_seconds` when the limit depends
on the participant, round, treatment, or session configuration.

## Back button

```python
allow_back_button = True
```

Template:

```html
{{ back_button }}
```

It cannot go back through a WaitPage or into a previous app.

---

# 14. Validation

## Field-level fixed validation

Set fixed limits and choices when declaring the model field:

```python
class Player(BasePlayer):
    offer = models.IntegerField(
        min=0,
        max=10,
        choices=[0, 5, 10],
    )
```

## One-field custom error

This is a module-level function. Its name must begin with the exact model-field
name:

```python
def offer_error_message(player: Player, value):
    if value > player.budget:
        return "The offer cannot exceed your budget."
```

If the field is named `offer`, oTree automatically calls
`offer_error_message()`.

## Whole-form custom error

This method belongs inside the Page that contains the fields:

```python
class Allocation(Page):
    form_model = "player"
    form_fields = ["amount_a", "amount_b"]

    @staticmethod
    def error_message(player: Player, values):
        if values["amount_a"] + values["amount_b"] > 100:
            return "The two amounts cannot total more than 100."
```

`values` is the submitted form dictionary.

## Dynamic field properties

These are module-level functions whose names begin with the exact model-field
name:

```python
def offer_min(player: Player):
    return 0

def offer_max(player: Player):
    return player.budget

def offer_choices(player: Player):
    return [0, 5, 10]
```

The argument is the object that owns the field: use Player for a Player field
and Group for a Group field. For example, a dynamic function for
`Group.posted_price` receives `group: Group`.

### Group-field example

Suppose Group declares a field named `group_bid`:

```python
class Group(BaseGroup):
    group_bid = models.CurrencyField()
```

Its dynamic minimum function must be at module level and must use the exact
field name followed by `_min`:

```python
def group_bid_min(group: Group):
    return C.LOWEST_BID
```

oTree automatically calls `group_bid_min(group)` when it builds and validates
a form containing `group_bid`. You do not call the function yourself.

The naming connection is exact:

```text
Group field:       group_bid
Minimum function: group_bid_min
Function argument: Group, because Group owns the field
Returned value:   lowest permitted group_bid
```

These special functions belong after the model classes and before the Page
classes, at the same indentation level as `creating_session()`. Do not place
them inside Group or inside the Page.

For a dynamic label, return the label text through `vars_for_template()`:

```python
class Offer(Page):
    form_model = "player"
    form_fields = ["offer"]

    @staticmethod
    def vars_for_template(player: Player):
        return dict(offer_label=f"Your budget is {player.budget}.")
```

Then pass it to the template command:

```html
{{ formfield "offer" label=offer_label }}
```

---

# 15. WaitPages

```python
def calculate_group_result(group: Group):
    # Read every group member's submitted fields and store the outcome.
    ...


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = calculate_group_result
```

## Normal group wait

Waits for everyone in the current Group.

```python
class ResultsWaitPage(WaitPage):

    @staticmethod
    def after_all_players_arrive(group: Group):
        calculate_group_result(group)
```

These are two alternative ways to connect the same helper function. Use this
hook for calculations requiring every group member's decision. Do not use both
forms on the same WaitPage.

## Entire-round wait

Set `wait_for_all_groups = True` inside the WaitPage class. The arrival hook
then receives Subsession instead of Group:

```python
class MarketWaitPage(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession: Subsession):
        # This runs once after all groups in the round arrive.
        ...
```

## Custom text

```python
class ResultsWaitPage(WaitPage):
    title_text = "Please wait"
    body_text = "Waiting for the other participant."
```

## Arrival-time grouping

```python
class MatchingWaitPage(WaitPage):
    group_by_arrival_time = True
```

This forms groups from participants as they reach the WaitPage. The WaitPage
must be the first Page in `page_sequence`. If it has `is_displayed()`, base the
condition only on the round number, not on participant characteristics.

---

# 16. Roles

The recommended fixed-role pattern is to define constants whose names end in
`_ROLE`:

```python
class C(BaseConstants):
    BUYER_ROLE = "Buyer"
    SELLER_ROLE = "Seller"
```

oTree then assigns the roles according to `id_in_group`, and you can use
`player.role` directly:

```python
class BuyerDecision(Page):

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.BUYER_ROLE
```

Common uses:

```python
player.role
buyer = group.get_player_by_role(C.BUYER_ROLE)
```

Role constants support fixed roles and integrate directly with
`group.get_player_by_role(...)`. A custom Python `@property` can calculate a
fixed or changing label, but it is not a universal replacement for oTree's
role system and can be incompatible with role lookup if used without the
automatic role constants.

For dynamic designs, first consider keeping the `_ROLE` constants and changing
players' group positions with `group.set_players(...)`. If roles depend on
treatments or other changing data, use a deliberately designed custom field or
helper and test all role lookups; do not define both automatic roles and a
second conflicting source of role truth.

## Changing roles by rearranging positions

With automatic `_ROLE` constants, roles follow `id_in_group`. Reordering a
Group's Player objects therefore reassigns both their positions and automatic
roles.

For a two-player group, this generic helper swaps the two positions:

```python
def swap_group_positions(group: Group):
    players = group.get_players()
    group.set_players([players[1], players[0]])
```

`group.set_players(...)` expects a list of Player objects in the desired new
order, not a list of participant IDs. The first Player in the list becomes
`id_in_group == 1`, the second becomes `id_in_group == 2`, and oTree updates
their automatic roles accordingly.

Call the rearrangement before any role-specific decision Pages or payoff
calculations in that round. For example, call it during session creation when
the change is known in advance, or from an appropriate WaitPage when it depends
on events during the experiment.

Important distinctions:

- `group.set_players(...)` rearranges positions within one Group.
- `subsession.set_group_matrix(...)` can move Players between Groups.
- Each round has separate Player and Group objects, so changing one round does
  not automatically rearrange every later round.
- After rearranging, use `player.role` and
  `group.get_player_by_role(C.SOME_ROLE)` rather than assuming an old position.

---

# 17. Payoffs

Store official round earnings in:

```python
player.payoff = cu(10)
```

For a group calculation:

```python
def set_payoffs(group: Group):
    for player in group.get_players():
        player.payoff = player.retained_amount + group.shared_return
```

`player.payoff` stores one round's official earnings. `participant.payoff`
combines the participant's payoffs across apps and rounds.

Do not confuse:

```text
Temporary Python variable
Custom earnings field
Built-in player.payoff
participant.payoff
```

Only assigning a temporary variable does not record the value.

---

# 18. Bots

Basic structure:

```python
class PlayerBot(Bot):
    def play_round(self):
        yield SomePage
        yield DecisionPage, dict(amount=5)
        assert self.player.amount == 5
```

Do not yield WaitPages. oTree handles them.

Use assertions to test stored decisions and calculated outcomes.

---

# 19. ExtraModel and live pages

Use ExtraModel for a variable number of events, such as bids, clicks, or messages.

```python
class Event(ExtraModel):
    player = models.Link(Player)
    value = models.IntegerField()
```

Create and retrieve:

```python
Event.create(player=player, value=5)
events = Event.filter(player=player)
```

`create()` stores one new row. `filter()` returns a list of matching rows.

Live Page Python:

```python
class LiveDecision(Page):

    @staticmethod
    def live_method(player: Player, data):
        response = dict(received=data)
        return {player.id_in_group: response}
```

The browser calls `live_method()` when its JavaScript executes `liveSend(...)`.
The returned dictionary maps recipient `id_in_group` values to response data.

Recipient `0` broadcasts to the group:

```python
return {0: response}
```

Browser JavaScript:

```javascript
liveSend({type: 'message'});

function liveRecv(data) {
    // update page
}
```

Messages are not automatically stored; assign model fields or create ExtraModel
records.

---

# 20. Data exports

## Custom export

```python
def custom_export(players):
    yield ["column_1", "column_2"]
    for player in players:
        yield [player.some_field, player.some_other_field]
```

The first yielded row is the header.

## Recording rule

| Value location | Recorded as model data? |
|---|---:|
| Declared model field assigned a value | Yes |
| Built-in `player.payoff` | Yes |
| Declared participant/session field | Yes |
| Local Python variable | No |
| `vars_for_template` value only | No |
| JavaScript variable only | No |
| Live message without model assignment | No |

---

# 21. oTree template blocks

```html
{{ block title }}
Page title
{{ endblock }}

{{ block content }}
Main content
{{ endblock }}
```

Optional organization:

```html
{{ block styles }}
<style>
    /* CSS */
</style>
{{ endblock }}

{{ block scripts }}
<script>
    // JavaScript
</script>
{{ endblock }}
```

---

# 22. Template variables

Automatically available:

```html
{{ player.some_field }}
{{ group.some_field }}
{{ subsession.round_number }}
{{ participant.code }}
{{ session.code }}
{{ C.SOME_CONSTANT }}
```

Also available: names returned by `vars_for_template()`.

---

# 23. oTree form commands in HTML

| Command | Meaning |
|---|---|
| `{{ formfields }}` | Render all fields selected by the Page |
| `{{ formfield 'field_name' }}` | Render one selected field |
| `{{ formfield_errors 'field_name' }}` | Render errors for a custom/raw field |
| `{{ next_button }}` | Render submit/Next button |
| `{{ back_button }}` | Render oTree back button when enabled |

For ordinary automatic rendering:

```html
{{ formfield "offer" }}
{{ next_button }}
```

For a raw custom input, its `name` must exactly match a field selected by the
Page, and you should display its validation errors:

```html
<input name="offer" type="number">
{{ formfield_errors "offer" }}
{{ next_button }}
```

---

# 24. Template conditions

```html
{{ if condition }}
    Content
{{ elif other_condition }}
    Other content
{{ else }}
    Fallback content
{{ endif }}
```

Use conditions for display. Keep payment and validation logic in Python.

For example:

```html
{{ if player.round_number == 1 }}
    <p>This text appears only in round 1.</p>
{{ endif }}
```

---

# 25. Template loops

```html
{{ for item in items }}
    {{ item }}
{{ endfor }}
```

Inside a loop:

```html
{{ forloop.counter }}
{{ forloop.first }}
{{ forloop.last }}
```

Example pattern:

```html
{{ for p in rounds }}
    <p>Round {{ p.round_number }}</p>
{{ endfor }}
```

---

# 26. Core HTML tags

## Text

```html
<h1>Main heading</h1>
<h2>Section heading</h2>
<h3>Subheading</h3>
<p>Paragraph</p>
<strong>Important text</strong>
<em>Emphasized text</em>
<br>
<hr>
```

## Lists

```html
<ul>
    <li>Bullet item</li>
</ul>

<ol>
    <li>Numbered item</li>
</ol>
```

## Links and images

```html
<a href="https://example.com">Link text</a>
<img src="image-path" alt="Description">
```

## Containers

```html
<div>Block container</div>
<span>Inline container</span>
```

## Tables

```html
<table>
    <thead>
        <tr>
            <th>Round</th>
            <th>Payoff</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>1</td>
            <td>10</td>
        </tr>
    </tbody>
    <tfoot>
        <tr>
            <th>Total</th>
            <th>10</th>
        </tr>
    </tfoot>
</table>
```

| Tag | Meaning |
|---|---|
| `<table>` | Complete table |
| `<thead>` | Heading section |
| `<tbody>` | Main data section |
| `<tfoot>` | Totals/summary section; it does not calculate the total |
| `<tr>` | Table row |
| `<th>` | Header cell |
| `<td>` | Data cell |

## Buttons

```html
<button type="button">Does not submit by default</button>
<button type="submit">Submits the form</button>
```

Inside oTree, prefer `{{ next_button }}` for ordinary submission.

---

# 27. Bootstrap classes included with oTree

## Alerts

```html
<div class="alert alert-info">Information</div>
<div class="alert alert-warning">Warning</div>
<div class="alert alert-success">Success</div>
<div class="alert alert-danger">Error/danger</div>
```

## Tables

```html
<table class="table">
<table class="table table-striped">
<table class="table table-bordered">
```

## Cards

```html
<div class="card">
    <div class="card-body">
        Content
    </div>
</div>
```

## Spacing

Common patterns:

```html
class="mt-3"
class="mb-3"
class="p-3"
```

`m` means margin, `p` means padding, `t` top, and `b` bottom.

---

# 28. CSS basics

```html
<style>
    .my-class {
        color: navy;
        font-weight: bold;
        margin-bottom: 1rem;
    }
</style>
```

Apply:

```html
<p class="my-class">Text</p>
```

Stable oTree selectors include:

| Selector | Element |
|---|---|
| `.otree-body` | Main Page body |
| `.otree-title` | Page title |
| `.otree-wait-page` | WaitPage |
| `.otree-timer` | Timer |
| `.otree-btn-next` | Next button |
| `.otree-form-errors` | Form error box |

---

# 29. JavaScript basics

Self-contained input-preview example:

```html
<input id="amount-input" type="number">
<p>Preview: <span id="amount-output"></span></p>

<script>
    const input = document.getElementById("amount-input");
    const output = document.getElementById("amount-output");

    input.addEventListener("input", () => {
        const value = input.value;
        output.textContent = value;
    });
</script>
```

JavaScript improves interaction but is not trustworthy for official payoff
calculation. Recalculate and validate important outcomes in Python.

---

# 30. Debugging checklist

1. Does the app folder name match `app_sequence`?
2. Does every Page appear in `page_sequence`?
3. Does every ordinary Page have a same-named HTML file? Standard WaitPages
   use oTree's built-in template.
4. Does `form_model` match the model containing the field?
5. Does every `form_fields` name exist?
6. Is the helper function actually called?
7. Does a skipped Page contain logic that was expected to run?
8. Does group logic run only after all required Players submit?
9. Is the value assigned to a declared field rather than a local variable?
10. Does the value appear in the downloaded data?
11. Does refreshing a Page unexpectedly change an outcome?
12. Did a timeout leave required fields empty?
13. Are you inspecting the correct app and round?
14. Do bot assertions check values, not only navigation?

# Official references

- https://otree.readthedocs.io/en/latest/
- https://otree.readthedocs.io/en/latest/models.html
- https://otree.readthedocs.io/en/latest/pages.html
- https://otree.readthedocs.io/en/latest/forms.html
- https://otree.readthedocs.io/en/latest/templates.html
- https://otree.readthedocs.io/en/latest/multiplayer/groups.html
- https://otree.readthedocs.io/en/latest/multiplayer/waitpages.html
- https://otree.readthedocs.io/en/latest/rounds.html
- https://otree.readthedocs.io/en/latest/timeouts.html
- https://otree.readthedocs.io/en/latest/bots.html
