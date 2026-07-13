MANAGER OTREE APP (oTree 6.0.15)

1. Copy the folder named "manager" into the root of your oTree project,
   beside settings.py.

2. Open your existing settings.py and add the two session configurations
   from settings_snippet.py to SESSION_CONFIGS.

3. Reset the database after adding/changing model fields:
      otree resetdb

4. Start the development server:
      otree devserver

5. Test either session config from the oTree admin/demo page:
      manager_performance_only
      manager_performance_and_help

DESIGN IMPLEMENTED
- One manager per participant; no groups or wait pages.
- 25 rounds and 25 worker pairs.
- Instructions appear only before round 1.
- Pair order is randomized separately for each manager.
- Worker A/B position is randomized within each pair.
- Performance-only session hides helping information.
- Performance-and-help session shows helping information.
- Managers type separate allocations for A and B.
- JavaScript gives live feedback.
- Python performs final server-side validation that allocations equal 100p.
- Pseudo worker IDs and characteristics are stored in the exported data.

IMPORTANT
The worker data in __init__.py are temporary pseudo data. Replace PSEUDO_PAIRS
with the final paired Qualtrics data before running the actual experiment.
