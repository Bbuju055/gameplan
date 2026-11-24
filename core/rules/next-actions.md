# Next actions — the rule table

The one place that says what a client needs next. The suite router (`skills/suite-router`) reads
it; no other skill carries its own "come back in a couple of weeks" line. A skill that finishes a
run asks the router for the top item instead. Every rule only suggests: nothing here runs a
capability, and nothing here starts research on its own.

Thresholds are named, not written in. Their values come from the org config's `next_actions`
section (shipped defaults: max_shown 3, not_now_days 3, thin_list_min 8, pulse_lead_days 7,
pulse_standing_days 30, deadline_lead_days 5, outcomes_after_days 10, outcomes_until_days 21,
landscape_refresh_days 91, snapshot_lead_days 10, clips_window_days 14,
list_stale_days 90, brief_tune_days 30). An agency changes them there, never here.

## What the rules read

Per client, all from the client folder per the client-folder contract: `calendar.md`,
`activity-log.md`, `runs.md` (both tables), the README review status, the placeholders in
`constraints.md`, and whether the client is in scope for a service: a `monitoring/` folder (the
brief) or a question set in `narrative/` (Pulse). R12 also reads the reporter list's
date when the list is a file, and R15 the client's `monitoring/cadence.md`. A rule whose plugin is not installed never fires. Each rule's plugin:
R2, R6, R12 media-targeting; R3 narrative-pulse; R7, R8, R9 competitive-intel; R10, R13, R15
daily-brief; R4, R5, R16 core (R4 suggests drafting in conversation when competitive-intel,
which owns the wargame, is not installed). R1, R11 and R14 were retired in 1.1.0 (setting a client
up now covers the first media list, the folder is approved at onboarding, and whether an output
went to the client is never asked: its approval says once that the person can tell the suite); their ids are never reused.

"Today" is as the client-folder contract says. "Matching log row" for an agency deadline means an activity-log row
that serves the deadline's event and delivers what the deadline names. A FIRM event has passed
when its date, or the last day of its window, is before today and its `outcome` is still empty;
no rule fires on a passed event (the what's-due answer and the morning check name it until its
outcome is recorded).

## The rules

| id | Fires when | Suggest | Trigger key | Unattended |
|---|---|---|---|---|
| R2 | `/target` scores fewer than `thin_list_min` reporters in a segment | A media list for that segment's beat | list name and segment | no: asked only at the end of that `/target` run |
| R3 | The client is in Pulse scope, and either a FIRM or GUIDED event under `## Upcoming` starts within `pulse_lead_days` with no `pulse` row dated after the previous event (or none at all), or no FIRM or GUIDED event is ahead and the latest `pulse` row is older than `pulse_standing_days` | A Pulse run before the event, or the monthly standing run | the calendar id, or the latest pulse date | yes |
| R4 | An agency deadline falls within `deadline_lead_days` with no matching log row | Holding language or messaging → wargame that event, or, when a wargame already serves it, draft what the deadline needs from that wargame's holding language; anything else → draft it in conversation from the client folder (voice, approved claims) for the lead to approve | calendar id and the deadline's "what" | yes |
| R5 | An agency deadline has passed with no matching log row | Ask whether it went out. Yes → the router appends the activity-log row as `entered-by`. No → it stays a missed deadline and a `no` row stops the question | calendar id and the deadline's "what" | yes |
| R6 | The latest `target` row for a list is `finalized`, dated between `outcomes_after_days` and `outcomes_until_days` ago, and no later `outcomes` row names that list | `/outcomes` for that list | list name | yes |
| R7 | A high-relevance row under `## Upcoming` has no `wargame` row whose output serves or names it | Wargame that event | calendar id | yes |
| R8 | The latest `landscape` row is older than `landscape_refresh_days` | Refresh the landscape (said plainly to be the long, costly run) | that row's date | yes |
| R9 | The quarter ends within `snapshot_lead_days`, the activity log has rows this quarter, and no `deliverable` row names this quarter's snapshot | The quarterly activities snapshot | the quarter | yes |
| R10 | A month or quarter closed within `clips_window_days`, the activity log has rows in it, and no `clips` row covers it | `/clips` for that period (the quarter only, when both closed together) | the period | yes |
| R12 | A `media-list` row exists and either the reporter list is a file older than `list_stale_days` or the latest `media-list` row is older than `list_stale_days` | A health check of the client's beat on the reporter list | the file date, or that row's date | yes for a file list; a list behind a connector is checked only in a conversation |
| R13 | The client has `monitoring/`, a brief has run since the last `brief-tune` row, and that row (or the first brief, if never tuned) is older than `brief_tune_days` | Tune the brief | the last tune's date | yes |
| R16 | A client folder exists and one or more of the five setup steps (the folder, the landscape, Pulse, the daily brief, the media list) is neither done nor skipped by the client-folder contract's test (its `runs.md` section, What counts as done: a step with `draft` rows alone is still left, except the client folder, which is done once it is built), for a plugin that is installed | Finish setting the client up, naming what is left ("Pellamune isn't fully set up: the daily brief and the media list are left. Finish now?"). Yes → the suite router's set-up-a-client job, from the first step left | the steps left | yes |
| R15 | The client has `monitoring/` (that is what says the brief is on: a `skipped` brief row from setting the client up does not turn it off), today is a publication day in `cadence.md` and not a holiday there, and `runs.md` has no `brief` row dated today (not started) or has one still at `draft` (waiting for review) | Start today's brief, or review the draft that is waiting | today's date | no: the morning check starts the drafts itself |

Not a rule, on purpose: anything that would start research by itself. A new competitor seen in
the news is a story in the brief, not a trigger for discovery.

## Silencing

Before ranking, drop every item the `## Declined` table silences. The latest row for the item's
rule and trigger key decides: `no` silences it until the key changes; `not-now` silences it for
`not_now_days` from that row's date; `mute` silences the rule for this client under any key until
an `unmute` row for that rule.

## Ranking and the cap

1. R5 items first: something already missed. When R15 is due, at most `max_shown` minus one of them
   are shown, so today's brief always keeps a place; the others count in the rest.
2. Then R15: the day's routine. However many clients it covers, it is one item: one line naming
   them, one place in the cap, waiting drafts named first.
3. Then items tied to a date still ahead (an event, a deadline), soonest first. An item for a
   period that has ended (R10's quarter) comes after every one of them, so a deadline two days
   away is never pushed below it, and above every undated item. An event whose window has lapsed
   has no date left: its item ranks after the ended period's and before the undated ones.
4. Then R16: a client not yet fully set up. It comes after every dated item, so a real deadline
   is never pushed below it, and before the other undated items.
5. Then undated items (R12, R13) in that order.
6. R8 last, unless it is the only item.

Show at most `max_shown`. The rest are counted ("and 2 more"), and listed only if asked.
