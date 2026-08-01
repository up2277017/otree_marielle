# oTree Command Gym 2: Posted-Price Trading Game

This is a guided assignment, not a completed solution. It is designed in a
Codecademy-style sequence: make one small change, run it, and verify one
specific result before continuing.

Do not copy code from the completed learning apps. The purpose is to practise
recalling where each oTree command belongs.

---

# The experiment you will build

Create a two-person, three-round posted-price trading game.

Each group contains:

- one Seller;
- one Buyer.

In every round:

1. The Seller has a production cost of 2 tokens.
2. The Buyer values the item at 10 tokens.
3. The Seller posts one whole-token price.
4. The Buyer observes the price and accepts or rejects it.
5. If the Buyer accepts:
   - the Seller earns `price - production cost`;
   - the Buyer earns `buyer value - price`.
6. If the Buyer rejects, both participants earn 0 for that round.

The highest permitted price comes from the session configuration. This lets
you run the same app under different market rules without changing the app's
code.

---

# What is new in this assignment

The first Command Gym assignment focused on basic models, forms, grouping,
WaitPages, calculations, repeated rounds, and template loops.

This assignment reuses those skills and introduces these commands or patterns
as core requirements:

- role constants ending in `_ROLE`;
- `player.role`;
- `group.get_player_by_role(...)`;
- a participant-entered field stored on Group;
- two sequential role-specific decision Pages;
- two synchronization points in one round;
- custom session parameters read through `session.config`;
- dynamic field limits such as `<field_name>_max(...)`;
- `get_timeout_seconds(player)`;
- deliberate timeout handling with `timeout_happened`;
- `field_display(...)`;
- `preserve_unsubmitted_inputs`;
- `{{ include_sibling }}`;
- `custom_export(players)`;
- role-conditional bots;
- `SubmissionMustFail` and simulated timeout tests as extension work.

You will also keep practising:

- `C`, Subsession, Group, and Player;
- `creating_session`;
- `group_randomly()` and `group_like_round()`;
- `Page`, `WaitPage`, and `page_sequence`;
- `form_model`, `form_fields`, and `is_displayed()`;
- `vars_for_template()`;
- `before_next_page()`;
- `after_all_players_arrive()`;
- `player.payoff`;
- `in_all_rounds()`;
- oTree templates, conditions, loops, and tables.

---

# How to use this assignment

For each mission:

1. Read only the current mission.
2. Make the smallest required change.
3. Save the file.
4. Run the stated checkpoint.
5. Do not continue until the checkpoint works.

When you need help, use this hint order:

1. Explain what you think the command should do.
2. Read the relevant cheat-sheet section.
3. Read the error message from the first line down.
4. Ask for a small hint.
5. Ask for a stronger hint.
6. Request completed code only if you explicitly decide you want it.

---

# Part A: Plan before coding

## Mission 1: Make the data-ownership map

### Objective

Decide where every value belongs before declaring any fields.

### Your task

Create this planning table on paper or in a temporary note:

| Value | Fixed parameter, Session config, Group, or Player? | Entered or calculated? | Must appear in export? |
|---|---|---|---|
| Production cost | Decide | Fixed | No separate response |
| Buyer value | Decide | Fixed | No separate response |
| Maximum allowed price | Decide | Fixed for one session | Useful |
| Posted price | Decide | Entered by Seller | Yes |
| Accept/reject decision | Decide | Entered by Buyer | Yes |
| Whether trade occurred | Decide | Calculated | Yes |
| Buyer timeout indicator | Decide | Calculated | Yes |
| Round payoff | Decide | Calculated | Yes |

### Reasoning questions

1. Which outcomes are shared by both members of a group?
2. Which values differ between session configurations?
3. Why should you not create a separate `role` field?
4. Which value already has a built-in oTree field?

### Checkpoint

You can explain why the posted price and acceptance decision should have one
shared value per group per round.

---

## Mission 2: Draw the round flow

### Objective

Understand the sequential interaction before creating Pages.

### Your task

Draw this flow and fill in who moves or waits at each position:

```text
Instructions/role information
          ↓
Seller decision
          ↓
First synchronization point
          ↓
Buyer decision
          ↓
Second synchronization point and payoff calculation
          ↓
Round results
          ↓
Final summary only when appropriate
```

### Questions

1. Where is the Buyer while the Seller is choosing?
2. Where is the Seller while the Buyer is choosing?
3. Why would one WaitPage at the end be insufficient?
4. At which point is it safe to calculate payoffs?

### Checkpoint

You can explain why the Buyer must not reach the acceptance Page before the
Seller's price exists.

---

# Part B: Create and register the app

## Mission 3: Create a new app safely

### Objective

Create a separate app without modifying your completed examples or first
assignment.

### Your task

1. Use the oTree `startapp` terminal command.
2. Choose a new folder name that describes the posted-price exercise.
3. Confirm that the folder contains `__init__.py`, HTML templates, and
   `tests.py` as appropriate for your oTree version.
4. Do not reuse `basic_assignment`.

### Command to practise

```text
otree startapp
```

### Checkpoint

The new folder exists and no existing learning app has changed.

---

## Mission 4: Add two session configurations

### Objective

Run the same app with two different market rules.

### Your task

Add two new dictionaries to `SESSION_CONFIGS`.

Both configurations should:

- run only your new app;
- use two demo participants;
- have different internal `name` values;
- have clear `display_name` values.

Add these custom parameters to both:

- `price_cap`;
- `decision_seconds`.

Use:

- a price cap of 8 in one configuration;
- a price cap of 10 in the other configuration;
- a reasonable positive time limit in seconds.

### Commands to practise

- `SESSION_CONFIGS`
- custom dictionary keys
- `session.config["price_cap"]`
- `session.config.get("decision_seconds", fallback)`

### Questions

1. Why is the price cap a session parameter instead of a constant in `C`?
2. Why must the configuration still use an even number of participants?
3. When would `.get(...)` be safer than square brackets?

### Checkpoint

Both configurations appear separately on the oTree demo/admin screen.

---

# Part C: Constants, roles, and fields

## Mission 5: Declare the constants

### Objective

Define the app structure and fixed economic parameters.

### Your task

In `C`, define:

- the URL name;
- two players per group;
- three rounds;
- the Seller production cost;
- the Buyer value;
- the Seller role;
- the Buyer role.

### New role rule

Role constant names must end in:

```text
_ROLE
```

oTree uses those constants to assign `player.role` automatically.

### Design checks

- Use Currency values for quantities that enter payoffs.
- Do not create `Player.role = models.StringField()`.
- Make the role labels participant-friendly.

### Questions

1. Which role will correspond to one `id_in_group`?
2. Why should production cost and Buyer value stay in `C`?
3. Why is `price_cap` not included in `C`?

### Checkpoint

You can state the difference between `C.BUYER_VALUE`,
`session.config["price_cap"]`, and `player.role`.

---

## Mission 6: Declare the Group fields

### Objective

Create database fields for decisions and shared outcomes.

### Your task

Declare Group fields for:

- the Seller's posted price;
- the Buyer's acceptance decision;
- whether trade occurred;
- whether the Buyer timed out.

### Field-design questions

For each field, decide:

- the appropriate model-field type;
- whether it needs `choices`;
- whether it needs a radio-button widget;
- whether it needs `initial`;
- whether it can be left blank before its role-specific Page is reached.

### Important distinction

The Seller and Buyer both access the same Group record. Only the role-specific
Page determines which participant is allowed to edit each Group field.

### Checkpoint

You can explain why `form_model = "group"` will be appropriate on both decision
Pages.

---

## Mission 7: Decide whether a new Player field is needed

### Objective

Avoid creating unnecessary duplicate data.

### Your task

Review the planned outcomes and answer:

1. Is a custom Player earnings field necessary when `player.payoff` already
   exists?
2. Is a custom Player role field necessary when `player.role` already exists?
3. Is a Player timeout field necessary when the timeout concerns one shared
   Buyer decision?

Only add a Player field if you can identify a value that truly differs by
participant and is not already built into oTree.

### Checkpoint

Your models contain no duplicate versions of the same Group outcome under
Player.

---

# Part D: Dynamic price validation

## Mission 8: Add a dynamic minimum price

### Objective

Prevent the Seller from entering a price below production cost.

### Why this mission uses a function

Because production cost is fixed in this exercise, a fixed `min=` on the model
field could also enforce the rule. This mission deliberately uses the dynamic
`<field_name>_min(...)` pattern so you learn how oTree asks a model object for a
limit at form-rendering and validation time. Mission 9 then applies the same
idea to a limit that genuinely changes between session configurations.

### Your task

Create the special dynamic-minimum function associated with the posted-price
field.

The function should:

1. Be placed at module level, not inside the Page class.
2. Have a name beginning with the exact posted-price field name.
3. Receive the current Group object, because the posted-price field is
   declared in Group. It does not receive the field name or submitted price.
4. Return the Seller's production cost.

### Command pattern

```text
<field_name>_min(model_object)
```

Because the field belongs to Group, think carefully about the function's
argument type.

### Checkpoint

The browser rejects a price below production cost before proceeding.

---

## Mission 9: Add a dynamic maximum price

### Objective

Make the valid price range depend on the selected session configuration.

### Your task

Create the corresponding dynamic-maximum function.

It should:

1. Receive the current Group object as its argument, because Group owns the
   price field. It does not receive the field name or submitted price.
2. Reach the current Session from that object.
3. Read the `price_cap` configuration parameter.
4. Return a value of the correct type for the price field.

### Commands to practise

- `<field_name>_max(...)`
- `group.session`
- `session.config[...]`
- `cu(...)` where type conversion is needed

### Testing sequence

1. Run the lower-cap configuration.
2. Attempt a price one unit above its cap.
3. Confirm validation blocks it.
4. Run the higher-cap configuration.
5. Confirm the same price is now permitted.

### Checkpoint

The same app enforces different price limits without changing `C` or the model
declaration.

---

# Part E: Grouping and role stability

## Mission 10: Form random pairs in round 1

### Objective

Reuse grouping commands while preserving roles across rounds.

### Your task

Create `creating_session(subsession)`.

Its matching rule should be:

- round 1: randomly form groups;
- later rounds: copy round 1's grouping.

### Commands to practise

- `subsession.round_number`
- `subsession.group_randomly()`
- `subsession.group_like_round(...)`

### Role checkpoint

Because roles follow position in the group, verify that each participant keeps
the same role in all three rounds.

### Data checkpoint

In the admin data, compare each participant's:

- participant code;
- round number;
- `id_in_group`;
- role.

---

## Mission 11: Retrieve players by role

### Objective

Stop relying on unexplained numeric positions inside payoff logic.

### Your task

Create a small ordinary helper function for later payoff work.

Inside it:

1. Receive Group.
2. Retrieve the Seller using the Seller role constant.
3. Retrieve the Buyer using the Buyer role constant.
4. Temporarily inspect or print their roles while testing.

### Command to practise

```text
group.get_player_by_role(...)
```

### Checkpoint

The retrieved Seller reports the Seller role and the retrieved Buyer reports
the Buyer role.

### Common mistake

Pass the role value expected by oTree. Do not pass the name of the constant as
plain text unless that is deliberately the stored role label.

---

# Part F: Build the sequential Pages

## Mission 12: Create Instructions and RoleInformation

### Objective

Show shared instructions and personalized role information.

### Your task

Create:

- an Instructions Page;
- a RoleInformation Page.

Both should appear only in round 1.

The role Page's HTML should display:

- `player.role`;
- the production cost if the participant is the Seller;
- the Buyer value if the participant is the Buyer;
- the price cap selected for this session.

### Commands to practise

- `is_displayed(player)`
- `player.role`
- template `if` conditions
- `session.config`

### Checkpoint

The two participant links display different role-specific information, and
neither information Page appears again in rounds 2 or 3.

---

## Mission 13: Create the SellerOffer Page

### Objective

Let only the Seller edit the shared posted-price field.

### Your task

Create a Page that:

1. Uses Group as its form model.
2. Selects only the posted-price field.
3. Is displayed only to the Seller.
4. Displays the Seller's cost and current session price cap.
5. Renders the selected field and a Next button in HTML.

### Commands to practise

- `form_model = "group"`
- `form_fields`
- `is_displayed(player)`
- `player.role`
- `vars_for_template(player)`
- `{{ formfield ... }}`

### Dynamic-label extension within the mission

Make the form label mention the current cap.

Use:

1. `vars_for_template()` to create label text;
2. the `label=` argument of `{{ formfield ... }}`.

### Checkpoint

- The Seller sees the Page.
- The Buyer skips it.
- A valid submitted price appears in the Group data.

---

## Mission 14: Preserve an unfinished Seller input

### Objective

Practise oTree 6's browser-side preservation of unsubmitted form values.

### Your task

Add the Page attribute that preserves an unfinished input if the Seller reloads
the Page or temporarily navigates away.

### Command to investigate

```text
preserve_unsubmitted_inputs
```

Placement reminder:

```python
class ExampleFormPage(Page):
    preserve_unsubmitted_inputs = True
```

### Test

1. Type a valid price.
2. Do not submit.
3. Reload the Page.
4. Confirm whether the typed value remains.

### Important distinction

This temporary value is stored in the browser. It is not yet stored in the
oTree database because the Seller has not submitted the form.

---

## Mission 15: Add the first WaitPage

### Objective

Prevent the Buyer from proceeding until the posted price exists.

### Your task

Place a WaitPage immediately after the SellerOffer Page.

This WaitPage:

- waits for the current Group;
- does not calculate payoffs;
- uses clear `title_text` and `body_text`;
- needs no custom HTML template.

### Manual test

1. Open both participant links.
2. Let the Buyer advance first.
3. Confirm the Buyer waits.
4. Submit the Seller's price.
5. Confirm both participants leave the WaitPage.

### Checkpoint

The Buyer never sees an empty or `None` price.

---

## Mission 16: Create the BuyerDecision Page

### Objective

Let only the Buyer accept or reject the observed price.

### Your task

Create a Page that:

1. Uses Group as its form model.
2. Selects only the acceptance field.
3. Is displayed only to the Buyer.
4. Shows the submitted posted price.
5. Shows the Buyer's value.
6. Uses clearly labelled accept/reject choices.

### Commands to practise

- role-based `is_displayed(player)`
- `form_model = "group"`
- Group fields in HTML
- Boolean choices
- radio-button widget

### Checkpoint

- The Buyer sees the Page.
- The Seller skips it and waits later.
- The acceptance value is stored once on Group.

---

# Part G: Timeouts and payoff calculation

## Mission 17: Add a dynamic Buyer timeout

### Objective

Use the time limit defined in the session configuration.

### Your task

On the BuyerDecision Page:

1. Add `get_timeout_seconds(player)`.
2. Read `decision_seconds` from the session configuration.
3. Return that number.
4. Add `before_next_page(player, timeout_happened)`.
5. If a timeout occurred:
   - deliberately store rejection;
   - store that the Buyer timed out.
6. If submission was normal:
   - ensure the timeout indicator records the opposite value.

### Commands to practise

- `get_timeout_seconds(player)`
- `player.session.config`
- `before_next_page(player, timeout_happened)`
- `player.group`

### Questions

1. Why does the Page hook receive Player even though `form_model` is Group?
2. How do you reach the Group from that Player?
3. Why should you explicitly store the timeout outcome instead of trusting an
   empty auto-submitted form?

### Checkpoint

Let one Buyer Page time out. Confirm that:

- the group does not get stuck;
- rejection is stored;
- the timeout indicator is stored;
- payoff calculation can still run.

---

## Mission 18: Write the trade and payoff helper

### Objective

Calculate outcomes once both decisions are available.

### Your task

Create an ordinary helper function that receives Group.

Work in this order:

1. Retrieve the Seller by role.
2. Retrieve the Buyer by role.
3. Read the Group's posted price.
4. Read the Group's acceptance decision.
5. Store whether trade occurred.
6. If trade occurred, assign the two role-specific payoffs.
7. Otherwise, assign zero Currency payoff to both.

### Commands to practise

- `group.get_player_by_role(...)`
- Group fields
- `player.payoff`
- `cu(0)`
- Python `if/else`

### Hand-calculation checkpoint

Before running the app, calculate these cases on paper:

1. Accepted price of 6.
2. Rejected price of 6.
3. Accepted price equal to production cost.
4. Accepted price equal to Buyer value.

For every accepted trade, check that the two payoffs add to the available trade
surplus.

### Common mistakes

- assigning both payoffs to the same Player;
- using an undefined local `price` instead of the stored Group field;
- returning payoffs without assigning them;
- calculating before the Buyer decision exists;
- mixing ordinary numbers and Currency values.

---

## Mission 19: Add the second WaitPage

### Objective

Calculate results only after the Buyer decision exists.

### Your task

Place a Results WaitPage after BuyerDecision.

Use its arrival hook to call the trade/payoff helper.

### Commands to practise

- `WaitPage`
- `after_all_players_arrive`
- ordinary helper-function call

### Manual test

1. Submit the Seller's price.
2. Do not submit the Buyer decision.
3. Confirm the Seller waits.
4. Submit the Buyer decision.
5. Confirm both proceed.
6. Inspect the stored Group decision and both Player payoffs.

### Checkpoint

The payoff helper runs only when both group members reach the second WaitPage.

---

# Part H: Results and reusable HTML

## Mission 20: Create the round Results Page

### Objective

Display shared outcomes and role-specific payoffs clearly.

### Your task

Display:

- round number;
- participant role;
- production cost;
- Buyer value;
- posted price;
- human-readable accept/reject label;
- timeout status;
- whether trade occurred;
- current participant payoff.

### New command

Use:

```text
field_display(...)
```

to retrieve the displayed label corresponding to a field's stored choice.

Generic syntax reminder:

```python
readable_label = group.field_display("some_choice_field")
```

Return the readable label through `vars_for_template()` if you want a short,
convenient variable name in HTML.

### Questions

1. Which values are automatically available in HTML?
2. Which displayed label needs preparation in Python?
3. Should `vars_for_template()` alter payoffs or decisions?

### Checkpoint

Refresh the Results Page. No stored decision, timeout indicator, or payoff
changes.

---

## Mission 21: Create a reusable rules fragment

### Objective

Avoid copying the same explanatory HTML into multiple templates.

### Your task

1. Create a small sibling HTML file containing the trading rules.
2. Do not put `block title` or `block content` around the fragment.
3. Insert it into both Instructions and Results.

### New command

```text
{{ include_sibling "filename.html" }}
```

### Checkpoint

Change one sentence in the fragment and confirm that both Pages display the
updated sentence.

---

## Mission 22: Create the final three-round summary

### Objective

Reuse across-round methods in a role-based experiment.

### Your task

Create a FinalSummary Page that:

- appears only in the final round;
- retrieves this participant's Player record from every round;
- displays one table row per round;
- displays round number and payoff;
- displays total payoff across all three rounds;
- displays the participant's role.

### Commands to practise

- `is_displayed(player)`
- `player.in_all_rounds()`
- `sum(...)`
- `vars_for_template()`
- template `for` loop
- `<thead>`, `<tbody>`, and `<tfoot>`

### Checkpoint

- The Page is skipped in rounds 1 and 2.
- It appears after round-3 Results.
- The table has three body rows.
- The footer total equals the sum of those rows.

---

# Part I: Assemble and test the app

## Mission 23: Build `page_sequence`

### Objective

Make the sequential game work in every round.

### Your task

Add all Page and WaitPage classes in the correct economic order.

Before typing the list, write a two-column trace:

| Seller experience | Buyer experience |
|---|---|
| Which Page appears first? | Which Page appears first? |
| Where does Seller wait? | Where does Buyer wait? |
| When does Seller see results? | When does Buyer see results? |

### Checkpoint

Trace both participants through one complete round without running the app.
Every role-specific Page should be paired with an appropriate waiting point.

---

## Mission 24: Conduct a two-browser manual test

### Objective

Test timing and synchronization, not only individual screens.

### Your task

Run one complete three-round session using:

- one normal browser window;
- one private/incognito browser window.

Test at least:

1. One accepted trade.
2. One rejected trade.
3. One Buyer timeout.
4. One price at the lower bound.
5. One price at the session cap.

### Data audit after each round

Check:

- posted price;
- acceptance;
- trade indicator;
- timeout indicator;
- Seller payoff;
- Buyer payoff;
- role;
- round number.

### Checkpoint

The stored data matches your hand calculations in every tested case.

---

# Part J: Data export

## Mission 25: Add a custom export

### Objective

Create a researcher-friendly dataset rather than relying only on the default
wide export.

### Your task

Define `custom_export(players)` at module level.

The first yielded row should contain column headings for:

- session code;
- participant code;
- round number;
- role;
- posted price;
- accepted/rejected value;
- timeout indicator;
- trade indicator;
- payoff.

Then loop over the supplied Player records and yield one data row per Player
record.

### Commands to practise

- `custom_export(players)`
- `yield`
- `player.session.code`
- `player.participant.code`
- `player.group`
- `player.round_number`
- `player.role`

### Questions

1. Why will each Group decision appear once for the Seller row and once for the
   Buyer row?
2. Is that duplication useful or undesirable for your planned analysis?
3. How would a one-row-per-group export differ?

### Checkpoint

Download the custom export from the admin data page and verify:

- expected column names;
- three rows per participant;
- no missing role;
- payoffs agree with the default export.

---

# Part K: Bots

## Mission 26: Write role-conditional bots

### Objective

Test a sequential multiplayer game automatically.

### Your task

In `play_round()`:

1. Yield round-1-only Pages only when appropriate.
2. Branch according to the bot's role.
3. Let the Seller bot submit SellerOffer.
4. Let the Buyer bot submit BuyerDecision.
5. Do not yield either WaitPage.
6. Yield Results.
7. Yield FinalSummary only in the final round.

### Commands to practise

- `self.player.role`
- `self.round_number`
- conditional `yield`
- assertions or `expect(...)`

### Checkpoint

The bot runner completes all three rounds without attempting to submit a Page
that is hidden from the bot's role.

---

## Mission 27: Add economic assertions

### Objective

Make bots verify stored data rather than only navigation.

### Your task

Add checks for:

- the stored posted price;
- the stored acceptance decision;
- the trade indicator;
- Seller payoff;
- Buyer payoff;
- total payoff across rounds.

### New commands to investigate

- `expect(...)`
- `SubmissionMustFail(...)`

Use `SubmissionMustFail` to verify that a Seller price outside the current
session cap is rejected.

Generic pattern:

```python
yield SubmissionMustFail(SomePage, dict(some_field=invalid_value))
```

### Checkpoint

Deliberately introduce one incorrect expected payoff. Confirm that the bot test
fails for the intended reason, then restore the correct expectation.

---

## Mission 28: Simulate a timeout in a bot

### Objective

Test the timeout branch without waiting for the real countdown.

### Your task

Use a bot submission object that marks:

```text
timeout_happened=True
```

Verify that the timeout produces:

- rejection;
- a true timeout indicator;
- zero payoffs;
- no blocked WaitPage.

### Checkpoint

The bot explicitly exercises both the normal Buyer submission path and the
timeout path.

---

# Final completion audit

Do not call the assignment complete until every answer is “yes.”

## Structure

- Is the new app separate from every completed learning app?
- Do both session configurations run the same app?
- Do all ordinary Pages have matching HTML?
- Are both WaitPages present in `page_sequence`?

## Roles and timing

- Does each group contain one Seller and one Buyer?
- Do roles remain stable across rounds?
- Can only the Seller edit the price?
- Can only the Buyer edit acceptance?
- Does the Buyer wait for the Seller's price?
- Does the Seller wait for the Buyer's response?

## Types and storage

- Is the price stored on Group?
- Is acceptance stored on Group?
- Can every payoff calculation use compatible Currency types?
- Are calculated outcomes assigned to declared fields?
- Are there no unnecessary duplicate Player fields?

## Session configuration

- Does each configuration enforce its own price cap?
- Does the Buyer timer read its value from the configuration?
- Does changing configuration parameters require no app-code edits?

## Results and data

- Does `field_display(...)` show a readable response label?
- Does the final summary contain all three rounds?
- Does the custom export contain the planned columns?
- Do manual calculations match stored payoffs?
- Does refreshing Results leave stored outcomes unchanged?

## Tests

- Do role-conditional bots follow the correct Pages?
- Is invalid-price validation tested?
- Is the timeout branch tested?
- Do assertions inspect stored economic outcomes?

---

# Optional extensions

Complete these only after the core assignment works.

## Extension 1: Reverse roles in a separate copy

Investigate:

- `group.get_players()`;
- `group.set_players(...)`.

Create a separate experimental copy in which partners stay together but swap
roles after a specified round. Do not alter the working core version first.

## Extension 2: Add a static market diagram

Place a small image in the app's static folder and display it with:

```text
{{ static "folder_name/image_name.png" }}
```

Verify that the image has useful alternative text.

## Extension 3: Record offer-edit events

Use JavaScript and an ExtraModel to explore recording every time the Seller
changes the proposed price before submitting.

Investigate:

- `ExtraModel`;
- `models.Link(...)`;
- `liveSend(...)`;
- `ExtraModel.create(...)`;
- the difference between an event log and the final Group price.

## Extension 4: Compare one-row-per-Player and one-row-per-Group exports

Create a second custom export function whose name also begins with
`custom_export`.

Design one row per Group per round and explain which export is easier for:

- participant-level payoff analysis;
- trade-level price analysis.

---

# Reflection questions

Write short answers after completing the assignment:

1. Why are posted price and acceptance Group fields even though different
   participants enter them?
2. Why does a role-specific Page still receive Player in `is_displayed()`?
3. Why does a dynamic validator for a Group field receive Group?
4. What does the first WaitPage guarantee?
5. What does the second WaitPage guarantee?
6. Why is `group.get_player_by_role(...)` clearer than relying on unexplained
   numeric positions?
7. Why is a session-config price cap more flexible than a constant?
8. What exactly is stored when `preserve_unsubmitted_inputs` preserves an
   unfinished value?
9. Why must a timeout outcome be assigned deliberately?
10. What is the analytical difference between Player rows and Group rows in an
    export?

If you can answer all ten without opening the cheat sheet, the central learning
goal of Command Gym 2 has been achieved.
