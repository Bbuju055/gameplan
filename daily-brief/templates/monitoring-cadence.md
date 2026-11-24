# Cadence — {CLIENT NAME}

The schedule contract. A scheduled run reads this file first and skips (with a one-line record
in `briefs/skipped.md`) on non-publication days. A human asking for a brief overrides the
calendar — the run says so and proceeds.

## Schedule

- Publication days: {Monday–Friday}
- Draft ready by: {8:00 AM} (the suite's morning check runs before the earliest of these across clients)
- Send-by target: {9:00 AM}
- Times are in the zone saved for the morning check; with none saved, the reader's own clock.
- Coverage window: since the previous brief, else since the previous publication day (brief-run's default window)

## Holidays observed ({YEAR})

| Date | Holiday |
|---|---|
| {YYYY-MM-DD} | {name} |

<!-- List the client's observed holidays explicitly; "US federal" is not a list. Refresh
     annually — brief-tune reminds when the year turns with no new list. -->

## People

- Reviewer and approver: {the name saved at setup, unless the user names someone else}
- Recipients: {optional; the agency sends the brief itself, so this is left empty unless the user gives names}

## Alert path

- Off-cycle alert briefs: {enabled / disabled}
- Alert reviewer if different from daily: {name}

## Change log

| Date | Who | Change |
|---|---|---|
| {DATE} | {NAME} | Initial setup |
