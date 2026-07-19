# Manager study: complete 1,400-worker simulation guide

This guide runs the manager experiment from the included pseudo worker data all
the way through manager sessions, testing, export, and later worker-bonus
calculation. Run every command from the project root: the folder containing
`settings.py` and `manager`.

The commands are for Windows PowerShell and this project's virtual environment.

## Simulation design

- 1,400 workers complete the worker task before the manager study.
- Workers are randomly matched into 700 fixed pairs.
- Every pair is evaluated exactly once overall.
- 350 pairs go to `performance_only`.
- 350 pairs go to `performance_and_help`.
- There are 14 managers per treatment (28 total).
- Every manager evaluates 25 pairs in this simulation.
- Worker A/B position is randomized for every assigned pair.
- Allocations to A and B must add to 100 pence.
- The stages are not live. Worker bonuses are calculated and paid after the
  manager data are exported.

```text
1,400 workers / 2 = 700 pairs
700 pairs / 25 pairs per manager = 28 managers
28 managers / 2 treatments = 14 managers per treatment
```

## Important files

```text
manager/
|-- __init__.py
|-- Allocation.html
|-- matching/
|   |-- create_random_pairs.py
|   `-- create_manager_assignments.py
`-- data/
    |-- pseudo_raw_workers_1400.xlsx
    |-- raw_workers_1400.csv
    |-- worker_pairs.csv
    `-- manager_assignments.csv
```

- `pseudo_raw_workers_1400.xlsx` is the readable pseudo source workbook.
- `raw_workers_1400.csv` is the unmatched input to the matching script.
- `worker_pairs.csv` fixes the 700 randomly created pairs.
- `manager_assignments.csv` fixes treatment, manager slot, decision order, and
  A/B orientation for every pair.
- `manager/__init__.py` loads the generated CSVs when oTree starts.

## Before starting

### 1. Open the project root

In PyCharm, open:

```text
C:\Users\up227\PycharmProjects\otree_marielle
```

Open PyCharm's Terminal. The prompt should end with:

```text
PS C:\Users\up227\PycharmProjects\otree_marielle>
```

### 2. Stop oTree

If `otree devserver` is running, press `Ctrl+C` and wait for the normal
PowerShell prompt. Keep the server stopped while regenerating CSVs and creating
sessions. Otherwise, the old Python module and CSV data can remain in memory.

### 3. Optional clean rehearsal

To delete all old local oTree sessions and test responses, run this while the
server is stopped:

```powershell
.\.venv\Scripts\otree.exe resetdb
```

This is optional and destructive. Skip it to preserve existing data. Never run
it after creating sessions you want to use, or after real data collection starts.

## Full 1,400-worker simulation

Keep the server stopped through Steps 1-4.

### Step 1: Confirm the raw input

Use the included file:

```text
manager\data\raw_workers_1400.csv
```

It has 1,400 rows and exactly these headings:

```text
worker_id,correct_letters,letters_revealed
```

Worker IDs must be unique. Both measures must be whole numbers from 0 through
22. The worker count must be even. For real Qualtrics data, create a CSV with
the same rules. The script accepts comma, semicolon, or tab separators and
UTF-8 files with or without a byte-order mark.

### Step 2: Create the 700 fixed random pairs

Run:

```powershell
.\.venv\Scripts\python.exe manager\matching\create_random_pairs.py --input manager\data\raw_workers_1400.csv --output manager\data\worker_pairs.csv --seed 20260713
```

Expected message:

```text
Created 700 random pairs from 1400 workers using seed 20260713.
```

The script validates the raw file and overwrites `worker_pairs.csv`. The same
input and seed always produce the same pairs. Change the integer seed only when
you deliberately want new pairs, and record the real experiment's seed.

### Step 3: Schedule all pairs across managers and treatments

Run:

```powershell
.\.venv\Scripts\python.exe manager\matching\create_manager_assignments.py --input manager\data\worker_pairs.csv --output manager\data\manager_assignments.csv --performance-managers 14 --help-managers 14 --max-pairs-per-manager 25 --seed 20260714
```

Expected output includes:

```text
Assigned 700 pairs exactly once across 28 managers using seed 20260714.
Performance-only decisions: 350; performance-plus-helping decisions: 350.
Manager workloads range from 25 to 25 pairs.
```

The script overwrites `manager_assignments.csv` and guarantees:

- every pair is assigned exactly once;
- each pair belongs to one treatment only;
- each manager gets at least one and no more than 25 pairs;
- slots start at 1 within each treatment;
- A/B orientation is randomized; and
- the seed is recorded in every assignment row.

Do not manually sort only part of either generated CSV. The files are joined by
`pair_id`, and `decision_number` controls each manager's round order.

### Step 4: Create both oTree sessions while the server is stopped

Performance only:

```powershell
.\.venv\Scripts\otree.exe create_session manager_performance_only 14
```

Performance and helping:

```powershell
.\.venv\Scripts\otree.exe create_session manager_performance_and_help 14
```

Each command prints a new random eight-character session code. Record each code
and its treatment. Codes differ every time; never look for an old example code.

Session creation copies all predetermined assignments into the database. The
app checks the participant count against the scheduled slots, so this simulation
must use exactly 14 participants in each session.

If a session was created before the latest CSV/code was loaded, do not reuse its
links. Stop the server and create a replacement session.

### Step 5: Start oTree

Only after the CSVs and sessions are final, run:

```powershell
.\.venv\Scripts\otree.exe devserver
```

Keep the terminal running and open:

```text
http://localhost:8000/admin
```

The two new sessions should be at the top. Press `Ctrl+F5` if the browser was
already open. Do not run `resetdb` now; it would delete the sessions.

### Step 6: Test performance only

1. Open the `manager_performance_only` session.
2. Open Participant 1's link.
3. Confirm performance information is displayed.
4. Confirm helping/letters-revealed information is hidden.
5. Try A=40 and B=40. Submission must be rejected.
6. Change to A=40 and B=60. It must continue.
7. Complete at least five decisions and check the `of 25` counter.

### Step 7: Test performance and helping

1. Open the `manager_performance_and_help` session.
2. Open Participant 1's link.
3. Confirm both performance and helping information are displayed.
4. Repeat the invalid-total and valid-total tests.
5. Complete at least five decisions.

Use an incognito/private window when testing another participant simultaneously,
so browser cookies do not mix participant links.

### Step 8: Complete the simulated collection

Each treatment has 14 one-use participant links. A complete simulation requires
all 28 links to finish all 25 decisions. Managers do not need to be online at
the same time because assignments were fixed before the sessions were created.

## Export and quality checks

In oTree admin, open Data and download the `manager` app CSV. This is long-format
data: one row is one manager-round. A complete simulation has 700 relevant rows.

If the database contains old tests, filter `session.code` to the two codes
recorded in Step 4. After filtering, verify:

```text
Rows                                  700
Unique player.pair_id                 700
Unique worker IDs across A and B      1,400
Rows in performance_only              350
Rows in performance_and_help          350
Rows per manager                      25
Completed allocations per manager    25
allocation_a + allocation_b           100 on every completed row
```

Important fields:

```text
session.code
participant.code
subsession.round_number
player.manager_slot
player.manager_treatment
player.assigned_pair_count
player.assignment_seed
player.pair_id
player.worker_a_id
player.worker_b_id
player.worker_a_correct
player.worker_b_correct
player.worker_a_help
player.worker_b_help
player.allocation_a
player.allocation_b
```

Helping values are stored for analysis in both treatments. They are hidden from
performance-only managers by `show_help=False` in `settings.py`.

oTree creates all round rows when the session is created. Unused participant
links and unfinished future rounds therefore have blank allocations. This is
normal; a decision is complete only when both allocation fields are present.

## Calculate worker bonuses later

This is not live matching. Qualtrics workers finish first; managers can complete
oTree later. After manager collection:

1. Filter the export to the two real session codes.
2. Pair `player.worker_a_id` with `player.allocation_a`.
3. Pair `player.worker_b_id` with `player.allocation_b`.
4. Stack those records into one worker-level payment table.
5. Join to Qualtrics/Prolific using the unique worker ID.
6. Confirm every expected worker ID appears once, then pay bonuses.

With a completed 1,400-worker run, every worker receives one manager-determined
allocation because every pair is scheduled exactly once.

## Different worker or manager counts

The first script accepts any even worker count and creates half as many pairs.
Choose manager counts with `--performance-managers` and `--help-managers`.

```text
total capacity =
    (performance managers + helping managers) * max pairs per manager
```

- Capacity must cover all pairs.
- At least one manager is required in each treatment.
- Scheduled managers cannot outnumber pairs because everyone gets at least one.
- `--max-pairs-per-manager` must be from 1 through 25.

The scheduler gives managers 25 pairs wherever possible. It uses a smaller
workload only when the pair and manager totals require it. Create each treatment
session with exactly the manager count used to generate the schedule.

## Troubleshooting

### `player.assigned_pair_count is None`

The session was created using an older running code state. Do not use its links.
Stop the server, confirm the CSVs, create two replacement sessions with Step 4,
restart with Step 5, and use only the new codes.

### New sessions do not appear

Run the server from the project root with the exact Step 5 command, then reopen
the admin URL or press `Ctrl+F5`. Remember that each creation generates new codes.

### Participant count is rejected

It must equal the scheduled slot count. It is 14 per treatment in this supplied
simulation. If manager counts change, regenerate `manager_assignments.csv` and
use those new counts during session creation.

### Raw CSV heading error

The headings must be exactly:

```text
worker_id,correct_letters,letters_revealed
```

Remove title rows, extra blank columns, or renamed headings, then save as CSV
UTF-8.

### Port already in use

Another dev server is running. Find its terminal, press `Ctrl+C`, and start only
one server.

### Export contains old rows

Filter by the intended `session.code` values. For a future clean rehearsal, use
the optional `resetdb` step before creating any new sessions, but only if all old
local data can be deleted.

## Final real-study checklist

- Back up the untouched Qualtrics worker export.
- Confirm exact headings, even worker count, and unique worker IDs.
- Record both random seeds.
- Archive final `worker_pairs.csv` and `manager_assignments.csv`.
- Record both session codes and treatments.
- Test one link in each treatment.
- Confirm helping information is hidden/shown correctly.
- Confirm invalid allocations cannot be submitted.
- Do not regenerate CSVs after real sessions are created.
- Do not run `resetdb` after real data collection begins.
- Retain the app code, input, generated files, seeds, session codes, and export
  together for reproducibility.
