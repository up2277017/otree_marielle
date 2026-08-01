# oTree Command Gym

## Purpose

This is a deliberately small practice assignment. Its purpose is not to create
an original economics experiment. Its purpose is to make you use the principal
oTree commands correctly and understand when each command runs.

Do not complete the whole assignment at once. Work through one mission, run the
app, and check the stated result before continuing.

This guide does not contain the completed Python or HTML.

## The experiment you will build

Create a two-person, two-round "Shared Box" experiment.

In every round:

1. Each participant receives 10 tokens.
2. Each independently places between 0 and 5 whole tokens in a shared box.
3. After both participants submit, the program calculates the group total.
4. Each participant receives an equal share of the group total.
5. Each participant's round payoff combines the tokens kept privately and the
   participant's share from the shared box.

The assignment also asks the participant for a nickname and a prediction. These
extra fields exist only to practise different model fields and Page forms.

## Command coverage

By completing the core missions, you will practise:

- `SESSION_CONFIGS`
- `C`, `Subsession`, `Group`, and `Player`
- `StringField`, `IntegerField`, `BooleanField`, and a monetary field
- `initial`, `label`, `choices`, `min`, `max`, and a widget
- `creating_session`
- `group_randomly()` and `group_like_round()`
- `Page`, `WaitPage`, and `page_sequence`
- `form_model`, `form_fields`, and `get_form_fields`
- `is_displayed()`
- `vars_for_template()`
- `before_next_page()`
- `error_message()`
- `after_all_players_arrive()`
- `get_players()` and `get_others_in_group()`
- `round_number`, `id_in_group`, and `payoff`
- `in_all_rounds()`
- oTree template variables, forms, conditions, and loops
- basic HTML and Bootstrap
- basic bot structure and data verification

The bonus missions cover timeouts, dynamic validation, participant fields,
session configuration parameters, JavaScript, CSS, and live pages.

---

# Part A: Build the smallest working app

## Mission 1: Create the app

### Your task

Use the oTree `startapp` command to create a new app. Choose a name that clearly
identifies it as your command-practice app.

Do not modify any of the completed `learning_*` apps.

### Checkpoint

Confirm that:

- A new app folder exists.
- It contains `__init__.py`.
- It contains at least one generated HTML template.

### Hint if stuck

Look at the command you used to create `assignment_1_mpl`. The command begins
with the oTree executable and ends with `startapp` followed by the app name.

---

## Mission 2: Register a session configuration

### Your task

Add a new dictionary inside `SESSION_CONFIGS` in `settings.py`.

Decide:

- The unique internal configuration name
- The readable display name
- The app folder to place in `app_sequence`
- An appropriate demo participant count for groups of two

### Commands practised

- `SESSION_CONFIGS`
- `name`
- `display_name`
- `app_sequence`
- `num_demo_participants`

### Checkpoint

Run the server and confirm that your new configuration appears on the Demo page.

### Do not continue if

- The configuration does not appear.
- oTree reports that it cannot import the app.
- The demo count would create an incomplete two-person group.

---

## Mission 3: Create the model skeleton

### Your task

In the new app's `__init__.py`, import the oTree objects required for:

- Constants
- Subsession
- Group
- Player
- An ordinary Page
- A WaitPage
- Model fields
- Form widgets
- Monetary values, if you decide to use them

Then declare:

- `C`
- `Subsession`
- `Group`
- `Player`

At this point, leave the three models without custom fields.

### Checkpoint

The app imports without an error.

### Reflection

Explain aloud:

- One session can contain several apps.
- One Subsession represents one app round.
- One Group contains the interacting Players in one round.
- One Player represents one participant in one app round.

---

# Part B: Constants and fields

## Mission 4: Define the constants

### Your task

Place the fixed design parameters in `C`.

You need constants for:

- The URL name
- Two participants per group
- Two rounds
- The round endowment
- The maximum shared-box contribution

### Checkpoint

Answer these questions without opening the cheat sheet:

1. Which constant determines group size?
2. Which constant makes the Page sequence repeat?
3. Which values should be monetary and which should be ordinary integers?
4. Why are these parameters in `C` rather than Player?

---

## Mission 5: Add Player fields

### Your task

Add fields for:

- A nickname
- Confirmation that the participant read the instructions
- A prediction of the other participant's contribution
- The participant's own contribution
- A calculated amount representing privately retained tokens

Use this mission to practise several field types.

### Design decisions

For every field, write a small planning table before coding:

| Variable | Field type | Entered by participant? | Calculated by Python? |
|---|---|---:|---:|
| Nickname | Decide | Yes | No |
| Confirmation | Decide | Yes | No |
| Prediction | Decide | Yes | No |
| Contribution | Decide | Yes | No |
| Retained tokens | Decide | No | Yes |

### Field options to practise

Use the appropriate options where relevant:

- `label`
- `initial`
- `min`
- `max`
- `choices`
- A radio-button widget

### Checkpoint

For every Player field, be able to state:

- What is stored
- Who supplies it
- On which Page it will be collected or calculated
- Whether it should appear in the export

---

## Mission 6: Add Group fields

### Your task

Add Group fields for:

- The total contributed by both participants
- The equal share received by each participant

### Reflection

Explain why these belong to Group rather than Player.

### Checkpoint

You should now have:

- Individual decisions on Player
- Shared outcomes on Group
- Fixed parameters in `C`

---

# Part C: Session creation and grouping

## Mission 7: Implement `creating_session`

### Your task

Create the special `creating_session` function.

Its grouping rule is:

- Randomize pairs in round 1.
- Keep the same pairs in round 2.

### Commands to investigate

- `subsession.round_number`
- `subsession.group_randomly()`
- `subsession.group_like_round(...)`

### Questions

1. Why does `creating_session` receive Subsession rather than Player?
2. How many times is it called in a two-round app?
3. Which round should be copied when creating the later matching?
4. What would happen if you randomized independently in both rounds?

### Checkpoint

Run a four-participant demo and inspect the session data or debug information.
Confirm that each participant has the same partner in both rounds.

---

# Part D: The instruction and profile Pages

## Mission 8: Create Introduction

### Your task

Create an Introduction Page and matching HTML.

The page should:

- Appear only in round 1.
- Explain the endowment.
- Explain the permitted contribution range.
- Explain that there are two rounds.
- Display values from `C`, rather than manually repeating numbers in HTML.

### Command to practise

- `is_displayed(player)`

### Checkpoint

- Introduction appears in round 1.
- Introduction is skipped in round 2.
- Changing a constant changes the displayed instruction.

### Common mistake

Do not put a calculation needed in every round inside a Page that is displayed
only in round 1. If the Page is skipped, its `before_next_page` also does not run.

---

## Mission 9: Create a Profile Page

### Your task

Create a Page that collects:

- Nickname
- Instruction confirmation

Show it only in round 1.

### Commands to practise

- `form_model`
- `form_fields`
- `{{ formfields }}`
- `{{ next_button }}`

### Checkpoint

Submit the Page and inspect the Player data.

Confirm:

- Both values were stored in round 1.
- The Page is skipped in round 2.

### Reflection

Because Player records are round-specific, decide whether the nickname needs to
exist in round 2. Do not solve this yet; it becomes a bonus mission about
participant fields.

---

# Part E: The decision Page

## Mission 10: Create Decision

### Your task

Create a Decision Page that collects:

- Prediction
- Contribution

For this mission, use the standard fixed `form_fields` attribute.

### Checkpoint

The HTML displays exactly the fields listed on the Page, in the same order.

Confirm in the exported or admin data that both values were stored.

---

## Mission 11: Replace fixed fields with `get_form_fields`

### Your task

After the fixed form works, replace the fixed field list with the dynamic
`get_form_fields(player)` Page method.

The returned fields may remain the same in both rounds. The purpose is only to
practise the command.

### Questions

1. Does `get_form_fields` return values or field-name strings?
2. Why is it an alternative to the fixed `form_fields` attribute?
3. When would different rounds or roles need different fields?

### Checkpoint

The Page behaves exactly as it did before the change.

---

## Mission 12: Add validation

### Your task

Add Page-level validation using `error_message(player, values)`.

Create one simple rule involving the prediction and contribution. The rule
should be easy to explain and should not change the economic purpose of the
exercise.

Examples of rule categories, not answers:

- Require one submitted number to be no greater than another.
- Forbid one particular combination.
- Require both decisions to use whole tokens.

### Checkpoint

Test:

- One submission that must pass
- One submission that must fail

When validation fails:

- The participant remains on the Page.
- A helpful error appears.
- The participant does not reach the WaitPage.

### Reflection

Explain the difference between:

- Field `min`/`max`
- `<field>_error_message`
- Page-level `error_message`

---

## Mission 13: Use `before_next_page`

### Your task

After a valid contribution is saved, calculate and store the amount the
participant retained privately.

Use the Page hook that runs after form validation and before the next Page.

### Commands to practise

- `before_next_page(player, timeout_happened)`
- Assignment to a declared Player field

### Checkpoint

Inspect the data immediately after the decision.

Confirm:

- Contribution was entered by the participant.
- Retained tokens were calculated by Python.
- Both are stored.

### Common mistake

A local variable is not a database field. Make sure the calculated value is
assigned to the declared Player field.

---

# Part F: Synchronization and group calculation

## Mission 14: Write the group calculation

### Your task

Create an ordinary helper function that receives Group.

It should:

1. Retrieve the two Players in the group.
2. Add their contributions.
3. Store the group total.
4. Calculate and store an equal share.
5. Assign each Player's built-in payoff using retained tokens and the group share.

### Commands to practise

- `group.get_players()`
- A loop over Players
- `player.payoff`

### Questions

1. Which values are common to both participants?
2. Which part of the payoff differs between participants?
3. Why must the function receive Group?
4. Why should the official payment use `player.payoff`?

### Checkpoint

Calculate one example by hand before running the app.

After the app runs, compare:

- Hand-calculated group total
- Stored Group total
- Hand-calculated share
- Stored Group share
- Hand-calculated payoffs
- Stored Player payoffs

---

## Mission 15: Add ResultsWaitPage

### Your task

Create a WaitPage between Decision and Results.

Use `after_all_players_arrive(group)` to call your group calculation.

Add simple wait-page title and body text.

### Commands to practise

- `WaitPage`
- `title_text`
- `body_text`
- `after_all_players_arrive(group)`

### Checkpoint

Open two participant links.

1. Submit only participant 1.
2. Confirm participant 1 waits.
3. Submit participant 2.
4. Confirm both proceed.
5. Confirm the group calculation runs once after both decisions exist.

### Common mistake

Do not calculate the group result in one participant's
`before_next_page`. The partner may not have submitted yet.

---

# Part G: Results and repeated rounds

## Mission 16: Create Results

### Your task

Create a Results Page and matching HTML.

Display:

- Current round
- Participant's contribution
- Partner's contribution
- Group total
- Equal share
- Retained tokens
- Participant payoff

### Commands to practise

- `vars_for_template(player)`
- `player.get_others_in_group()`
- Automatically available `player`, `group`, and `C`

### Checkpoint

For every displayed value, state its source:

```text
C
Player field
Group field
vars_for_template
```

Refresh Results and confirm no stored outcome changes.

### Common mistake

Do not generate random values or change payoffs inside `vars_for_template`.
It runs again when the Page is refreshed.

---

## Mission 17: Create FinalSummary

### Your task

Create a final Page that:

- Appears only in the last round.
- Retrieves this participant's Player records from both rounds.
- Displays a row for each round.
- Displays total contribution and total payoff across the two rounds.

### Commands to practise

- `is_displayed(player)`
- `player.in_all_rounds()`
- `sum(...)`
- Template `for` loop

### Checkpoint

- The Page is skipped in round 1.
- It appears after round-2 Results.
- Both rounds appear in the table.
- Totals equal the two displayed rows.

---

## Mission 18: Assemble `page_sequence`

### Your task

Place all Page and WaitPage classes in the intended order.

Before coding, draw the flow:

```text
Round 1 flow
Round 2 flow
```

Remember that the same `page_sequence` repeats every round, and
`is_displayed()` controls which Pages are skipped.

### Checkpoint

Run the complete experiment with two participants from beginning to end.

---

# Part H: HTML practice

## Mission 19: Improve the templates

### Your task

Across your templates, deliberately use:

- One heading
- Paragraphs
- An ordered or unordered list
- Strong emphasis
- An informational Bootstrap alert
- A table
- An `if` condition
- A `for` loop
- `{{ formfields }}` on one Page
- `{{ formfield 'field_name' }}` on another Page
- `{{ next_button }}`

### Checkpoint

The HTML should be readable on a normal browser width and a narrow/mobile width.

### Rule

HTML changes presentation. It does not replace server-side model storage,
validation, or payoff calculations.

---

# Part I: Data and testing

## Mission 20: Audit the data

### Your task

Complete a known test session and download or inspect the data.

Create an audit table:

| Variable | Expected owner | Expected round | Expected value |
|---|---|---:|---|
| Nickname | Player | 1 | Your test input |
| Contribution | Player | 1 and 2 | Your test inputs |
| Retained tokens | Player | 1 and 2 | Hand-calculated |
| Group total | Group | 1 and 2 | Hand-calculated |
| Group share | Group | 1 and 2 | Hand-calculated |
| Payoff | Player | 1 and 2 | Hand-calculated |

### Checkpoint

Do not consider the assignment complete merely because the browser displays the
right values. Confirm the values in the data.

---

## Mission 21: Write a basic bot

### Your task

Create a bot that:

- Visits only Pages that are displayed.
- Submits known values.
- Ignores WaitPages in the bot sequence.
- Asserts stored decisions.
- Asserts the group total.
- Asserts the share.
- Asserts the payoff.
- Visits FinalSummary only in the final round.

### Checkpoint

Your assertions should compare actual data with values you calculated by hand.

---

# Bonus command missions

Complete these only after the core app works.

## Bonus 1: Dynamic field validation

Replace one fixed `max` with a `<field>_max(player)` method.

Use a harmless rule whose limit depends on round number or another stored field.

## Bonus 2: Timeout

Add a short test timeout to the Decision Page.

Use `timeout_happened` to:

- Record whether the participant timed out.
- Supply a documented default decision.

Test this in development only.

## Bonus 3: Participant field

Move the nickname from a round-specific Player field to a declared participant
field so it persists naturally across apps and rounds.

Compare its export location with the original Player field.

## Bonus 4: Custom session parameter

Move one non-structural parameter from `C` into a custom session config key.

Access it through `session.config`.

Do not move `NUM_ROUNDS` or `PLAYERS_PER_GROUP` for this beginner exercise.

## Bonus 5: CSS

Add a small `styles` block that changes:

- Maximum page width
- One result-table heading color

Use stable oTree selectors where relevant.

## Bonus 6: JavaScript

Add a participant-facing preview of privately retained tokens that updates when
the contribution input changes.

The preview must not determine the official payoff. Python remains authoritative.

## Bonus 7: Back button

On a safe, non-WaitPage screen, practise:

- `allow_back_button`
- `{{ back_button }}`

Remember that participants cannot go back through a WaitPage.

## Bonus 8: Live-method reading exercise

Do not add a live page to this simple app. Instead, open the completed learning
auction and identify:

- `live_method`
- `liveSend`
- `liveRecv`
- `ExtraModel.create`
- Broadcast recipient `0`

Explain what each does without modifying the auction.

---

# Hint policy

When asking for help, request one of these:

1. Concept reminder
2. Error interpretation
3. Small hint
4. Strong hint
5. Partial unrelated example
6. Full solution only if you explicitly decide to stop treating it as an assignment

# Official references

- https://otree.readthedocs.io/en/latest/models.html
- https://otree.readthedocs.io/en/latest/pages.html
- https://otree.readthedocs.io/en/latest/forms.html
- https://otree.readthedocs.io/en/latest/multiplayer/groups.html
- https://otree.readthedocs.io/en/latest/multiplayer/waitpages.html
- https://otree.readthedocs.io/en/latest/templates.html
- https://otree.readthedocs.io/en/latest/rounds.html
- https://otree.readthedocs.io/en/latest/bots.html
