MANAGER OTREE APP (oTree 6.0.15)

OPEN THIS FILE FOR THE COMPLETE STEP-BY-STEP RUNBOOK:

    manager/README.md

It covers the complete 1,400-worker simulation:

- safely stopping and restarting the server;
- creating 700 random worker pairs;
- assigning all pairs once across 28 managers and two treatments;
- creating both 14-participant sessions while the server is stopped;
- testing both treatments and the allocation validator;
- checking the long-format export; and
- calculating worker bonuses later.

Do not run resetdb unless you intentionally want to delete every local session
and all local test responses.
