# Add these two dictionaries to SESSION_CONFIGS in your project's settings.py.
# Keep the rest of your existing settings.py unchanged.

SESSION_CONFIGS = [
    dict(
        name='manager_performance_only',
        display_name='Manager Study – Performance Only',
        app_sequence=['manager'],
        num_demo_participants=1,
        show_help=False,
    ),
    dict(
        name='manager_performance_and_help',
        display_name='Manager Study – Performance and Helping',
        app_sequence=['manager'],
        num_demo_participants=1,
        show_help=True,
    ),
]

# No PARTICIPANT_FIELDS or SESSION_FIELDS are required for this app.
