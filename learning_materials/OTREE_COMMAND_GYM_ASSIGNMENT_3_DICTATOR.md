# oTree Command Gym 3: Framed Dictator Allocation

This is the third build-it-yourself assignment in the progressive oTree
course. It assumes that you have attempted:

1. Command Gym 1: the repeated public-goods exercise;
2. Command Gym 2: the posted-price Buyer-Seller game.

This guide gives you precise objectives, locations, commands, and checkpoints.
It deliberately does **not** provide a completed app. Write each piece yourself
and ask for a small hint when a checkpoint fails.

---

# The experiment you will build

Build a four-round, two-person dictator-allocation experiment.

Each pair contains:

- one **Allocator**;
- one **Recipient**.

Partners remain fixed across all four rounds, but roles alternate:

| Round | Participant who began in position 1 | Participant who began in position 2 |
|---:|---|---|
| 1 | Allocator | Recipient |
| 2 | Recipient | Allocator |
| 3 | Allocator | Recipient |
| 4 | Recipient | Allocator |

Thus, every participant makes two allocation decisions and is passive in two
rounds. In each round:

1. the pair receives a round-specific endowment;
2. the Allocator chooses how much to transfer to the Recipient;
3. the Recipient makes no decision and waits;
4. the Allocator keeps the endowment minus the transfer;
5. the Recipient earns the transfer;
6. both participants see the result and their history.

Use these endowments:

| Round | Endowment |
|---:|---:|
| 1 | 10 |
| 2 | 12 |
| 3 | 16 |
| 4 | 20 |

Each pair is assigned one of two instruction framings:

- **Neutral:** describe the task as dividing an allocation budget;
- **Ownership:** describe the Allocator as initially owning the endowment.

The mathematical rules must be identical in both treatments. Only the wording
changes. Both members of a pair must receive the same treatment, and it must
remain unchanged across rounds.

At session creation, randomly select one paid round for each pair. Both members
of the pair use the same paid round. At the end, only the earnings from that
round become official oTree payoff.

This design is useful in behavioral economics because it combines distributional
choice, framing, repeated decisions, and random-round incentive payment.

---

# What is new in Assignment 3

The main new oTree ideas are:

- `PARTICIPANT_FIELDS` for values that persist across rounds;
- `SESSION_FIELDS` for information shared by the entire session;
- a field on `Subsession` that can differ by round;
- `subsession.get_groups()`;
- assigning a treatment to a whole pair;
- `random.randint(...)`;
- using a list with `round_number - 1`;
- `group.get_players()` and `group.set_players(...)`;
- changing automatic roles by rearranging `id_in_group` positions;
- distinguishing Python list indexes from oTree positions;
- `player.in_round(...)`;
- `player.in_rounds(...)`;
- `player.in_previous_rounds()`;
- separating provisional round earnings from official `player.payoff`;
- paying one randomly selected round;
- `js_vars(player)`;
- a small JavaScript earnings preview;
- displaying a persistent treatment and a selected paid round in HTML.

You will also keep practising:

- constants, model ownership, and Currency types;
- `creating_session()`;
- fixed partners and changing automatic roles;
- Player and Group forms;
- dynamic field bounds;
- field-specific validation;
- role-specific Pages;
- WaitPages and `after_all_players_arrive()`;
- ordinary helper functions;
- `vars_for_template()`;
- `before_next_page()`;
- template conditions, loops, and tables;
- bots, assertions, and data auditing.

This assignment does **not** yet require `live_method()`, `liveSend()`, or
`ExtraModel`. Those belong in a later assignment focused on real-time events.

---

# How to work through it

For each mission:

1. read only that mission;
2. identify the file in which the change belongs;
3. make the smallest required change;
4. save it;
5. run the checkpoint;
6. do not continue while the checkpoint is failing.

Use this help ladder:

1. explain what you think the command should do;
2. consult the relevant cheat-sheet section;
3. inspect the first meaningful line of the error;
4. ask for a small hint;
5. show your own attempt;
6. ask for completed code only if you explicitly want the answer.

---

# Part A: Plan the experiment

## Mission 1: Draw the economic sequence

### Objective

Understand which participant acts and which participant waits.

### Your task

Copy this flow into a note and fill in the missing role at each point:

```text
Round instructions
       ↓
________ chooses a transfer
       ↓
________ waits for that transfer
       ↓
Both reach one synchronization point
       ↓
Round earnings are calculated
       ↓
Both see the round result and history
```

Then explain why this game needs only one decision WaitPage, whereas the
posted-price game needed two.

### Checkpoint

You can state exactly when the transfer exists and when it is safe to calculate
both participants' earnings.

---

## Mission 2: Make the data-ownership map

### Objective

Choose the correct oTree object before declaring fields.

### Your task

Complete the final column yourself:

| Value | Persistence needed | Entered or calculated? | Correct owner |
|---|---|---|---|
| Current round's endowment | One value for everyone in one round | Assigned | Decide |
| Transfer | One value for a pair in one round | Entered | Decide |
| Round earnings | Different for each person in one round | Calculated | Decide |
| Treatment | Stable for a participant across rounds | Assigned | Decide |
| Paid round | Stable for a participant across rounds | Assigned | Decide |
| Treatment counts | Shared by the entire session | Calculated | Decide |
| Official payoff | Different for each participant | Built in | Decide |
| Current role | Determined again in each round | Built in from position | Decide |

### Reasoning questions

1. Why is the transfer not two separate Player fields?
2. Why is a treatment not a normal Player field if it must persist?
3. Why is the current endowment a useful Subsession field rather than only a
   local variable?
4. Why do you need a separate `round_earnings` field if `player.payoff` exists?
5. Why should you not create a separate StringField called `role`?

### Checkpoint

You can explain the difference among Player, Group, Subsession, Participant,
and Session storage in this experiment.

---

# Part B: Create and register the app

## Mission 3: Create a separate app

### Objective

Protect all existing learning apps.

### Your task

1. Run oTree's app-creation command.
2. Give the new folder a clear name such as `dictator_assignment`.
3. Do not reuse or edit `basic_assignment` or `posted_price_assignment`.
4. Confirm that the new folder has `__init__.py` and starter templates/tests
   appropriate for your oTree version.

### Command to practise

```text
otree startapp
```

### Checkpoint

The new folder exists beside the previous apps, and the previous apps have not
changed.

---

## Mission 4: Add the session configuration

### Objective

Make the new app runnable from the oTree admin interface.

### Your task

In `settings.py`, add a new entry to `SESSION_CONFIGS` with:

- a unique `name`;
- a clear `display_name`;
- an `app_sequence` containing only your new app;
- a demo participant count that is a multiple of two.

Keep the existing configurations unchanged.

### Commands to practise

- `SESSION_CONFIGS`
- `dict(...)`
- `app_sequence`
- `num_demo_participants`

### Checkpoint

The new configuration appears in the admin interface and can create a session
with two participants.

---

## Mission 5: Declare persistent fields in `settings.py`

### Objective

Create storage that exists outside an individual Player round record.

### Your task

Add the following names to `PARTICIPANT_FIELDS`:

- a name for the persistent framing treatment;
- a name for the randomly selected paid round.

Add a name to `SESSION_FIELDS` for the session-wide treatment counts.

If these settings lists already exist, add names to the existing lists rather
than defining the settings twice.

### Commands to practise

```python
PARTICIPANT_FIELDS = [
    # Add the persistent participant-level names here.
]

SESSION_FIELDS = [
    # Add the shared session-level name here.
]
```

The comments show the placement without supplying the field-name answers.

### Important distinction

Declaring a name in `PARTICIPANT_FIELDS` or `SESSION_FIELDS` makes that custom
attribute available. You do not also declare the same value with
`models.StringField()` in `Player` or `Session`.

### Checkpoint

You can explain why these names belong in `settings.py`, while
`round_earnings` will belong in the app's Player class.

---

# Part C: Constants and models

## Mission 6: Declare the constants

### Objective

Create the values that never change between sessions.

### Your task

In `C`, declare:

- a URL name;
- two players per group;
- four rounds;
- the four endowments as a Python list of Currency values;
- automatic Allocator and Recipient role constants;
- two treatment-name constants.

### New list idea

The endowments should be one ordered collection, not four unrelated constants.
You will later retrieve the correct item using the round number.

Declare the Allocator `_ROLE` constant before the Recipient `_ROLE` constant.
With automatic roles, the first role constant belongs to `id_in_group == 1`
and the second belongs to `id_in_group == 2`. Later, you will change which
Participant occupies each position.

### Commands to practise

- `Currency(...)` or `cu(...)`
- Python lists
- `_ROLE` constants

### Checkpoint

You can point to the first, second, third, and fourth item in the endowment list
and explain why their Python indexes are 0, 1, 2, and 3.

---

## Mission 7: Declare the Subsession field

### Objective

Store one current endowment for the whole round.

### Your task

Give `Subsession` one Currency field called `round_endowment`.

Do not give it a participant-facing label because participants will not edit
this field.

### Command to practise

```python
class Subsession(BaseSubsession):
    # Declare the field here.
```

### Checkpoint

You can explain why a four-round app creates four Subsession records and can
therefore store four different `round_endowment` values.

---

## Mission 8: Declare the Group transfer

### Objective

Store the pair's one shared allocation decision.

### Your task

Give `Group` one Currency field called `transfer`.

Requirements:

- the participant should see a clear label;
- the minimum can be fixed at zero;
- do not put the round-specific maximum directly in the field declaration.

### Question

Why is `max=C.ROUND_ENDOWMENTS` invalid, even though the list contains every
possible endowment?

### Checkpoint

There is exactly one transfer value per pair per round.

---

## Mission 9: Declare Player fields

### Objective

Store individual outcomes and a comprehension response.

### Your task

Give `Player`:

1. a Currency field for `round_earnings`, initialized to zero;
2. an Integer or Boolean field for one comprehension-check response.

The comprehension question should test the rule:

> If the endowment is 12 and the Allocator transfers 5, how much does the
> Recipient earn?

Use radio buttons with human-readable choices.

### Commands to practise

- `models.CurrencyField(initial=...)`
- `models.IntegerField(choices=...)` or `models.BooleanField(choices=...)`
- `widgets.RadioSelect`

### Checkpoint

You can distinguish the stored choice value from the label shown beside its
radio button.

---

# Part D: Build session creation carefully

## Mission 10: Store the endowment for every round

### Objective

Connect oTree round numbers to Python list positions.

### Your task

Create `creating_session(subsession)` and, on every call:

1. read `subsession.round_number`;
2. convert it to the matching zero-based list index;
3. retrieve that endowment from your constant list;
4. assign it to `subsession.round_endowment`.

### Pattern to reason from

```python
value_for_round = C.SOME_LIST[subsession.round_number - 1]
```

Use your own constant and field names.

### Why the `- 1` matters

oTree rounds start at 1. Python list positions start at 0. Without the
subtraction, round 1 would incorrectly use the second endowment.

### Checkpoint

Create a session and inspect all four Subsession records. Their stored values
must be 10, 12, 16, and 20 in order.

---

## Mission 11: Keep partners but alternate roles

### Objective

Randomize partners only once, then change positions in even rounds so that
automatic roles alternate.

### Your task

Extend `creating_session()`:

1. In round 1, randomize groups and positions.
2. In every later round, first copy the grouping from round 1. This restores
   the original pairs and original position order as a clean baseline.
3. In rounds 2 and 4, loop over the current Subsession's Groups.
4. For each even-round Group, retrieve its ordered list of two Player objects.
5. Pass those same two Player objects to `group.set_players(...)` in reversed
   list order.
6. In rounds 1 and 3, leave the copied order unchanged.

### Commands to practise

- `subsession.group_randomly()`
- `subsession.group_like_round(1)`
- `subsession.get_groups()`
- `group.get_players()`
- `group.set_players(...)`
- `subsession.round_number`
- `% 2` for detecting an even round
- Python list indexes `[0]` and `[1]`

### The two numbering systems

Suppose this call returns an ordered Python list:

```python
players = group.get_players()
```

Then:

- `players[0]` means the first item in the Python list;
- `players[1]` means the second item in the Python list;
- oTree positions are instead numbered `id_in_group == 1` and
  `id_in_group == 2`.

The numbers inside square brackets select existing Player objects. They are
not the new oTree positions. The order in the list you pass to
`group.set_players(...)` determines the new positions:

- the first passed Player becomes `id_in_group == 1`;
- the second passed Player becomes `id_in_group == 2`.

Do not pass participant IDs, participant codes, or numbers to
`group.set_players(...)`; pass a list containing the actual Player objects.

### Automatic-role consequence

Automatic `_ROLE` constants follow `id_in_group`. After you reverse the two
Player objects in an even round, their positions change and their automatic
roles change with those positions. You do not assign `player.role` directly.

### Checkpoint

For both participant links, record partner, `id_in_group`, and role in every
round. The partner must remain the same, while position and role follow the
round pattern shown at the start of this assignment. Each participant must be
Allocator exactly twice.

---

## Mission 12: Assign a persistent pair treatment

### Objective

Use Participant storage and `subsession.get_groups()`.

### Your task

Only while round 1 is being created:

1. retrieve all groups in the Subsession;
2. assign each group to one of the two framing treatments;
3. retrieve the two Player objects in that group;
4. store the same treatment on each Player's Participant object.

Aim for approximately balanced treatment numbers. One manageable method is to
alternate treatments across the already-randomized groups. You may use
`enumerate(..., start=1)` and test whether the group number is odd or even.

### Commands to practise

- `subsession.get_groups()`
- `group.get_players()`
- `player.participant`
- assignment to a declared Participant field
- `enumerate(...)`
- `% 2` for odd/even alternation

### Do not do this in every round

If you assign the treatment again in rounds 2–4, you risk changing a persistent
condition. Participant storage lets you assign once and read many times.

### Checkpoint

Both members of every pair have the same treatment, and their treatment is
unchanged in rounds 2–4 even though their roles change.

---

## Mission 13: Select one paid round per pair

### Objective

Create a persistent random incentive rule.

### Your task

Still inside the round-1 group loop:

1. import Python's `random` module at the top of the app;
2. draw one integer between 1 and `C.NUM_ROUNDS`, inclusive;
3. assign that same integer to the paid-round Participant field of both
   players in the pair.

### Command to practise

```python
random.randint(lower_bound, upper_bound)
```

`randint` includes both endpoints, so rounds 1 and 4 must both be possible.

### Checkpoint

Each pair has one valid paid round from 1 through 4, and the two partners'
stored values match.

---

## Mission 14: Store session-wide treatment counts

### Objective

Practise a custom Session field.

### Your task

During round-1 creation:

1. count how many groups receive each treatment;
2. create one dictionary containing both counts;
3. assign the dictionary to your declared Session field through
   `subsession.session`.

### Commands to practise

- Python dictionary creation and updating
- `subsession.session`
- assignment to a declared Session field

### Scope check

The stored numbers should count pairs, not Player records. A two-person pair
must add one to its treatment count, not two.

### Checkpoint

The two treatment counts add up to the number of groups in the session.

---

# Part E: Dynamic validation and instructions

## Mission 15: Add the round-specific maximum transfer

### Objective

Reuse dynamic validation with a new object path.

### Your task

Create the specially named maximum function belonging to the Group field
`transfer`.

It should:

1. receive the Group object because the field belongs to Group;
2. reach the current Subsession from that Group;
3. return the stored `round_endowment` as the maximum.

### Commands to practise

- `<field_name>_max(group)`
- `group.subsession`
- a Subsession model field

### Checkpoint

In each round, test exactly the endowment and exactly one unit above it. The
first must pass and the second must fail.

---

## Mission 16: Create Introduction and comprehension Pages

### Objective

Explain the rules and prevent misunderstanding before decisions begin.

### Your task

Create two Pages that appear only in round 1:

1. `Introduction`, with no form;
2. `Comprehension`, with the Player comprehension field.

Add a field-specific validation function for the comprehension field. Return a
helpful error when the stored answer is not the correct Recipient earning.

### Commands to practise

- `is_displayed(player)`
- `form_model = "player"`
- `form_fields`
- `<field_name>_error_message(player, value)`

### Checkpoint

An incorrect answer stays on the Page with guidance. A correct answer advances.
Neither Page reappears in later rounds.

---

## Mission 17: Display treatment-specific wording

### Objective

Use persistent Participant data in Python and HTML.

### Your task

Create a round-1-only `TreatmentInformation` Page. In its HTML:

1. inspect the current participant's stored treatment;
2. show neutral wording for the neutral condition;
3. show ownership wording for the ownership condition;
4. show the same mathematical allocation rule in both branches.

### Commands to practise

- `player.participant.<field_name>` in Python
- `participant.<field_name>` in HTML
- `{{ if ... }}`, `{{ else }}`, and `{{ endif }}`

### Research-design warning

Do not accidentally change the endowment, feasible choices, or payoff formula
between treatments. This mission changes wording only.

### Checkpoint

Partners see the same framing, participants in different treatments see
different framing, and all see identical mathematical rules.

---

# Part F: Build the decision and preview

## Mission 18: Create the AllocatorDecision Page

### Objective

Let only the Allocator submit the Group transfer.

### Your task

Create a Page that:

1. uses `Group` as the form owner, with the required lowercase form-model text;
2. includes only `transfer`;
3. appears only to the Allocator;
4. displays the current `subsession.round_endowment`;
5. renders the form field and Next button.

### Commands to practise

- `form_model = "group"`
- `form_fields`
- `player.role`
- `is_displayed(player)`
- `{{ formfield ... }}`
- `{{ next_button }}`

### Checkpoint

The Allocator sees and can submit the field. The Recipient skips the Page.
When roles change in the next round, the other participant must see the Page;
do not hard-code a participant code or original position into `is_displayed()`.

---

## Mission 19: Send the endowment to JavaScript

### Objective

Learn the boundary between Python data and browser-side interaction.

### Your task

On `AllocatorDecision`, add `js_vars(player)` that returns the current round's
endowment under a clear JavaScript-facing key.

Use this generic pattern:

```python
@staticmethod
def js_vars(player: Player):
    return dict(
        some_key=SOME_VALUE,
    )
```

In the browser, the matching value will be available as:

```javascript
js_vars.some_key
```

### Important distinction

`js_vars()` sends values from server-side Python to browser-side JavaScript. It
does not save a response and does not replace an oTree form field.

### Checkpoint

Temporarily log the value in the browser console and confirm that it changes
correctly across rounds.

---

## Mission 20: Add a live earnings preview in HTML

### Objective

Give immediate feedback without changing official calculations.

### Your task

In `AllocatorDecision.html`:

1. add two `<span>` elements, one for the Allocator's preview and one for the
   Recipient's preview;
2. retrieve the transfer input using `document.getElementById(...)`;
3. listen for its `input` event;
4. read the typed transfer;
5. calculate both preview amounts using the endowment from `js_vars`;
6. update each span's `textContent`.

### Commands to practise

- `{{ block scripts }}`
- `document.getElementById(...)`
- `addEventListener("input", ...)`
- `Number(...)`
- `.textContent`
- `js_vars.<key>`

### Guard against an empty input

When the input is blank, JavaScript should display a sensible placeholder or
treat the previewed transfer as zero. Decide explicitly which behavior you
want.

### Security and data rule

The preview is informational only. JavaScript can be changed by a participant,
so official validation and payoff calculations must still happen in Python.

### Checkpoint

Typing 3 with an endowment of 12 previews 9 for the Allocator and 3 for the
Recipient. Refreshing before submission does not create a stored transfer.

---

# Part G: Synchronization and round earnings

## Mission 21: Write the round-earnings helper

### Objective

Calculate two individual outcomes from one Group decision.

### Your task

Create an ordinary helper that receives Group. It should:

1. retrieve the Allocator by role;
2. retrieve the Recipient by role;
3. retrieve the current round endowment;
4. calculate and store the Allocator's `round_earnings`;
5. calculate and store the Recipient's `round_earnings`.

Do not assign `player.payoff` yet.

### Commands to practise

- `group.get_player_by_role(...)`
- `group.subsession.round_endowment`
- `group.transfer`
- assignment to two different Player fields

### Hand-calculation checks

Calculate these cases before running Python:

1. endowment 10, transfer 0;
2. endowment 12, transfer 5;
3. endowment 20, transfer 20.

In every case, the two earnings should add to the current endowment.

### Checkpoint

Your helper has no `return` requirement because it stores both results directly
on Player records.

---

## Mission 22: Add the decision WaitPage

### Objective

Ensure the transfer exists before calculating earnings.

### Your task

Place one WaitPage immediately after `AllocatorDecision`. It must:

- wait for both members of the current group;
- call the round-earnings helper after both arrive;
- use a clear waiting title and body;
- have no custom HTML file.

### Commands to practise

- `WaitPage`
- `after_all_players_arrive(group)`
- calling an ordinary helper

### Manual synchronization test

1. Advance the Recipient first.
2. Confirm the Recipient waits.
3. Leave the Allocator's decision unsubmitted.
4. Confirm no round earnings have been calculated yet.
5. Submit the Allocator's transfer.
6. Confirm both participants proceed with stored earnings.

### Checkpoint

The Recipient never sees a result based on an empty transfer.

---

## Mission 23: Create RoundResults

### Objective

Display the economic outcome without modifying it.

### Your task

Create a Page and HTML template displaying:

- round number;
- treatment;
- role;
- current endowment;
- transfer;
- current participant's round earnings.

Use a Bootstrap table or card. Add a Next button.

### Commands to practise

- automatically available template variables;
- Participant fields in HTML;
- Subsession fields in HTML;
- Group and Player fields in HTML;
- Bootstrap classes.

### Refresh test

Refresh this Page several times. The transfer and earnings must remain
unchanged. Do not calculate or assign outcomes in `vars_for_template()`.

---

# Part H: Cross-round history

## Mission 24: Create a cumulative History Page

### Objective

Retrieve this participant's records from multiple rounds.

### Your task

Create a `History` Page that appears from round 2 onward. In
`vars_for_template()`:

1. retrieve the participant's Player records from round 1 through the current
   round;
2. retrieve only the records before the current round as a second list;
3. calculate the sum of previous-round earnings;
4. return the records and sum to HTML.

### Commands to practise

- `player.in_rounds(1, player.round_number)`
- `player.in_previous_rounds()`
- `sum(...)`
- `vars_for_template()`

### HTML task

Create a table with one row per retrieved Player record and columns for:

- round;
- endowment;
- transfer;
- your role;
- your round earnings.

Remember that a historical Player record reaches its historical Group and
Subsession through that record, not through the current `player`.

### Reasoning question

Inside a loop called `record`, which object path gives you the endowment from
that record's own round?

### Checkpoint

Round 2 shows two rows, round 3 shows three, and round 4 shows four. The
previous-round sum excludes the current round. The role column should alternate
for the same participant.

---

# Part I: Random-round payment

## Mission 25: Write the final-payment helper

### Objective

Convert provisional round earnings into one official payoff.

### Your task

Create an ordinary helper receiving Player. It should:

1. read the paid-round number from the participant field;
2. retrieve all Player records for this participant;
3. set every round's official `payoff` to zero Currency;
4. retrieve the Player record from the selected round;
5. copy that record's `round_earnings` into that record's `payoff`.

### Commands to practise

- `player.participant.<paid_round_field>`
- `player.in_all_rounds()`
- `player.in_round(n)`
- looping over Player records
- `cu(0)`
- `player.payoff`

### Important distinction

Do not overwrite `round_earnings`. You need those four values for the history
table. Only one official payoff should be nonzero.

### Hand audit

If round earnings are 4, 7, 9, and 11 and the paid round is 3, the official
payoffs should be 0, 0, 9, and 0.

### Checkpoint

The sum of `player.payoff` across all rounds equals the selected round's
`round_earnings`, not the sum of all four earnings.

---

## Mission 26: Trigger payment at the correct time

### Objective

Make the helper run exactly when all required round data exists.

### Your task

Use `before_next_page(player, timeout_happened)` on `RoundResults`.

- In rounds 1–3, do nothing.
- In round 4, call the final-payment helper for the participant viewing the
  Page.

### Commands to practise

- `before_next_page(...)`
- `player.round_number`
- `C.NUM_ROUNDS`
- calling an ordinary Player helper

### Why not `vars_for_template()`?

`vars_for_template()` may run repeatedly when the Page is refreshed. It is for
preparing display values, not for payment assignment.

### Checkpoint

Before leaving round-4 Results, all round earnings exist. After leaving it,
exactly the selected Player record has the official payoff.

---

## Mission 27: Create PaymentSummary

### Objective

Explain random-round payment transparently.

### Your task

Create a Page displayed only in the final round. In `vars_for_template()`:

1. read the participant's paid round;

2. retrieve the Player record from that round;
3. retrieve all four Player records;
4. prepare the selected round's earnings;
5. calculate the participant's payoff including the participation fee, using
   the built-in Participant method.

### Commands to practise

- `player.in_round(...)`
- `player.in_all_rounds()`
- `participant.payoff_plus_participation_fee()` in Python
- `vars_for_template()`

### HTML task

Build a four-row table. Add a `Paid?` column using a template condition that
compares each record's round number with the selected round.

Use `<tfoot>` for the selected payment summary rather than presenting it as a
fifth experimental round.

### Checkpoint

- Exactly one table row says it was selected.
- The displayed selected earning matches that row.
- The displayed final amount uses the official payoff rule.

---

# Part J: Assemble and test

## Mission 28: Build `page_sequence`

### Objective

Put all Pages in economic and temporal order.

### Your task

Assemble the sequence from:

- Introduction;
- Comprehension;
- TreatmentInformation;
- AllocatorDecision;
- the decision WaitPage;
- RoundResults;
- History;
- PaymentSummary.

Do not copy the order of that bullet list blindly. Check when final-payment
assignment occurs and when PaymentSummary needs to read it.

### Two-role trace

Before running the app, create this table and fill every cell:

| Position | Allocator experience | Recipient experience |
|---|---|---|
| Round-1-only Pages | Decide | Decide |
| Decision Page | Decide | Decide |
| WaitPage | Decide | Decide |
| Results | Decide | Decide |
| History | Decide | Decide |
| Final-only summary | Decide | Decide |

### Checkpoint

Trace both participant links across round 1, round 2, and round 4. Remember that
the person described as Allocator in one round becomes Recipient in the next.
No Page should read data before it exists.

---

## Mission 29: Conduct a two-browser manual test

### Objective

Test timing, persistence, bounds, histories, and payment.

### Your task

Use one normal browser window and one private/incognito window. Test:

1. a zero transfer;
2. a transfer equal to the endowment;
3. a middle transfer;
4. one attempted transfer above the round maximum;
5. Recipient waiting before the Allocator submits;
6. fixed partners but alternating roles;
7. fixed treatment;
8. the correct endowment in every round;
9. history-row growth;
10. one and only one paid round.

### Per-round data audit

After every round, inspect:

- Subsession endowment;
- Group transfer;
- both Player `round_earnings`;
- both participants' treatment;
- both participants' paid round;
- official payoff.

### Checkpoint

Every stored value agrees with a hand calculation, and the official payoff is
not mistakenly the sum of all four provisional earnings.

---

# Part K: Automated testing and export practice

## Mission 30: Write role-conditional bots

### Objective

Reinforce testing of a sequential two-role game with persistent state.

### Your task

In `tests.py`:

1. yield round-1-only Pages only in round 1;
2. branch using the bot Player's **current-round** role;
3. let only the Allocator submit `AllocatorDecision`;
4. do not yield the WaitPage;
5. yield Results and History only when displayed;
6. yield PaymentSummary only in the final round;
7. assert that the transfer respects that round's endowment;
8. assert that the two round earnings sum to the endowment;
9. in round 4, inspect the participant's selected round and assert the official
   payment rule.

Do not assume that a bot which is Allocator in round 1 keeps that role. Read
`self.player.role` again in every `play_round()` call.

### Commands to practise

- `Bot`
- `play_round()`
- conditional `yield`
- `self.player.role`
- `self.round_number`
- `assert`
- cross-round retrieval inside a test

### Checkpoint

The bot test completes all four rounds, each Participant is Allocator twice,
and the test checks stored economic outcomes rather than merely checking that
Pages load.

---

## Mission 31: Create a payment-focused custom export

### Objective

Reinforce tidy export design while adding persistent fields.

### Your task

Create a custom export with one row per Player per round. Include:

- session code;
- participant code;
- round;
- role;
- treatment;
- paid round;
- round endowment;
- transfer;
- round earnings;
- official payoff;
- whether this row is the paid row.

The first yielded row must contain headings. Later rows contain data.

### Commands to practise

- `custom_export(players)`
- `yield`
- Player-to-Participant paths
- Player-to-Subsession paths
- Python comparison producing `True` or `False`

### Data question

Why will transfer and endowment appear twice per pair-round in a
one-row-per-Player export? Decide whether that duplication is useful for this
analysis.

### Checkpoint

For each participant, the export contains four rows and exactly one row marked
as paid.

---

# Final completion audit

Do not call the assignment complete until every answer is yes.

## Structure and timing

- Is the app separate from the two previous assignments?
- Does the session configuration use an even participant count?
- Do both participants reach the decision WaitPage?
- Does the Recipient wait while the Allocator decides?
- Is the calculation helper called only after the transfer exists?

## Storage ownership

- Is the endowment stored once per Subsession-round?
- Is the transfer stored once per Group-round?
- Are round earnings stored separately for each Player-round?
- Are treatment and paid round persistent Participant fields?
- Are treatment counts stored once for the Session?

## Treatments and matching

- Are groups randomized only in round 1?
- Do partners remain fixed across all rounds?
- Are the round-1 positions restored as the baseline before each even-round
  swap?
- Do positions and roles alternate in the intended pattern?
- Is every participant Allocator twice and Recipient twice?
- Do pair members share a treatment?
- Does the treatment remain constant?
- Does framing alter wording but not economic rules?

## Validation and calculations

- Does each round enforce its own transfer maximum?
- Do the two earnings add to the endowment?
- Does JavaScript provide only a preview?
- Does Python independently validate and calculate official outcomes?
- Does refreshing display Pages leave stored data unchanged?

## Cross-round payment

- Is the selected round between 1 and 4?
- Do partners share the selected round?
- Does `in_round(n)` retrieve the correct record?
- Are all non-selected official payoffs zero?
- Does the selected official payoff equal selected `round_earnings`?
- Does the PaymentSummary clearly identify the paid row?

## Testing and data

- Do both role bots complete?
- Do assertions check economic identities?
- Does the custom export contain persistent treatment and payment information?
- Does every participant have four export rows and one paid row?

---

# Optional extensions

Complete these only after the core version works.

## Extension 1: Session-controlled history

Add a `show_history` session-config parameter. Use it to decide whether the
History Page appears. Practise:

- `session.config.get("show_history", default_value)`;
- combining round and configuration conditions in `is_displayed()`.

## Extension 2: A previous-choice reminder

From round 2 onward, use `player.in_round(player.round_number - 1)` to show only
the immediately previous round's transfer and earnings above the current
decision.

## Extension 3: Whole-form validation

Add a second Allocator field asking for the amount the Allocator expects to
keep. Use Page-level `error_message(player, values)` to require consistency
between the transfer, expectation, and endowment.

Do not use this prediction in the payoff calculation.

## Extension 4: `wait_for_all_groups`

Create a final session-wide synchronization Page before payment summaries and
investigate:

```python
wait_for_all_groups = True
```

Explain why this makes every group wait for every other group, and why it is
usually unnecessary for calculations that depend only on one pair.

## Extension 5: Prepare for live pages

Without implementing a live page, write a short comparison of:

- a JavaScript preview;
- a normal oTree form submission;
- `liveSend()`/`liveRecv()`;
- an `ExtraModel` event log.

This reflection prepares the next difficulty level.

---

# Reflection questions

Answer these after the app works:

1. Why does `round_endowment` belong to Subsession?
2. Why does the transfer belong to Group?
3. Why are treatment and paid round Participant fields?
4. What would go wrong if the treatment were reassigned in every round?
5. Why does list access use `round_number - 1`?
6. What is the difference between `round_earnings` and `player.payoff`?
7. What does `player.in_round(n)` return?
8. How is `in_previous_rounds()` different from `in_all_rounds()`?
9. Why must JavaScript not be trusted for official payoff calculation?
10. When does the decision WaitPage call the round-earnings helper?
11. Why is final payment not assigned in `vars_for_template()`?
12. Why does each participant have exactly one nonzero official payoff record?
13. What is shared at the pair level and what is shared at the whole-session
    level?
14. Why might a researcher prefer one row per Player over one row per pair?
15. Why does reversing the list passed to `group.set_players(...)` change
    automatic roles?
16. What is the difference between Python list indexes 0/1 and oTree
    `id_in_group` positions 1/2?

If you can answer these without consulting the code, you understand the main
new concepts introduced by Command Gym 3.
