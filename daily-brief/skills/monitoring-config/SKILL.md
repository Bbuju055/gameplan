---
name: monitoring-config
description: Create or edit a client's daily-brief monitoring files (queries.md, sources.md, cadence.md) in their client folder. A new setup is built from the client folder and saved with defaults and no question, and what is watched is said in one line; changes are made by typing ("stop showing me X", "also watch Y", "no brief on Fridays"), and an existing query spreadsheet imports losslessly. Use when /brief finds no monitoring set up, as the fourth step when the core plugin's suite router sets a client up, or for "add a query", "downgrade that source", "change the schedule". Configuration only; it never runs a brief. Cross-plugin requests route through core's suite-router.
---

# Monitoring Config

Every message, the notes while it works included, is in plain words, with nothing internal named and nothing said about what was read or checked (the core plugin's `rules/voice.md`). A note while it works is one plain line, or nothing: what is being done or what comes next, in plain words, is fine; it never names anything internal and never gives a count or a result.

Monitoring is client knowledge, so it lives in the client folder and is owned by the account
team — the plugin ships zero client logic. This skill writes and maintains the three files
brief-run consumes, from the shipped templates in `templates/`.

## Prerequisites

The client folder must exist with `positioning.md` and `approved-claims.md` in place: the
queries are built from it. No folder → offer to set the client up first (the core plugin's suite
router).

## New setup: the watch terms, and no question

Nobody is interviewed row by row and nothing is asked. Build the three files from the client folder and the shipped
templates, save them, and say what is being watched in one line.

1. **queries.md**, built, not asked: the categories in the house order (competitive, regulatory,
   program, capital markets) with the catch-all designated (always a category that has rows: the first in the house order when the person names none, moved to the next one that has rows if an answer empties it); rows for the client (company names
   and tickers from positioning), its programs, asset codes and trial names (pipeline), every competitor in
   `competitors.md` (the landscape's set once one exists), the field (the landscape's space), and
   the client's own terms (`own-terms.md`, per the core plugin's `rules/sources.md`). Priority
   follows from the row: the client and its programs 5, direct competitors 4, the field 3,
   adjacent competitors 2. A program name that is nothing but an ordinary word (CORAL, HARBOR) is never a
   term on its own: use the company name or the asset code. A name with a number or a code
   attached (VISTA-3) is distinctive, and stands as a term by itself.
2. **sources.md**: the house default tier list from the template, unchanged.
3. **cadence.md**, defaults: weekdays; the year's US federal holidays off, each written out by
   date in the holiday list (the template's rule: a list, not a label); draft ready by 8:00 AM local
   time (the time zone is never asked here: times are in the zone saved for the morning check, and the
   person's own clock where none is saved), reviewer and approver the name saved at setup (the client-folder contract's
   Who approves). Recipients are not asked: the agency sends the brief itself.
4. **The sample, inside the suite router's set-up-a-client job only.** Run signal-gather on the built rows over the default window (brief-run's, its step 4),
   with its normal preflight and degradation rules, and story-curate on what comes back, and keep
   the result for the job's closing review: one line of counts ("43 stories from 19 publications; the competitive rows bring the most") and the top story. Anywhere else (asked for directly, or from `/brief` for a client with no watch terms yet) no sample is made: the
   first brief is the first look. Asked to set the brief up, the first brief is drafted in that same turn, with the watch line above it,
   and its approval is the one stop. If no source is reachable, say so where the counts would go.
5. **Say what is watched, once, and ask nothing.** One line, in the message that comes next (the
   brief's review, or the set-up job's closing review): "I'm watching for news on <client> (<ticker>), <each program by asset code, name and trial>, <each competitor by name> and
   <the field, with any second name for it: "X, also written Y">. Tell me any time to add or stop watching something." With it, once, in
   plain words, what the brief is built from here: web search only in the Claude app ("The brief
   comes from web search here, so it can miss stories a news feed would catch"), plus any news
   or monitoring connector the session has (named once, per `rules/sources.md`).
6. **Changes in plain words, at any time.** ("stop showing me Fierce", "add
   Brantley Bio", "no brief on Fridays", "draft by 7") are made to the files, the change log with them, and said
   once, with the result they belong to (the client-folder contract's Writing, and what a reply may say). Extra terms go to
   `own-terms.md` and into the queries. Inside the set-up job, write a `brief` row at `finalized`,
   "watch terms saved": that is the step done (the client-folder contract's What counts as done).

With the three files, when a sample ran, save its results to `monitoring/calibration-<date>.md` (what ran, what came back, what
was changed and why), so the first real briefs can be compared against it. Every file carries a
change log section (date, who, what changed); append on every edit.

## Importing an existing query spreadsheet

An agency's existing query workbook maps losslessly, whatever its column names:

| Spreadsheet column (typical names) | queries.md field |
|---|---|
| Category / Coverage bucket | category |
| Query / Search terms (Boolean) | boolean terms, verbatim |
| Priority (1–5) | priority |
| Channel / Source | targeted sources (news rows → feed; owned-social rows → a note in queries.md as owned-social, phase 2, not run yet and not silently dropped) |

Any per-client strategy or positioning text in the workbook belongs in `positioning.md`, not in monitoring —
offer to file it there as a proposed update if the folder lacks it. Anything ambiguous in the
sheet is asked about, never guessed, and nothing is written until those questions are answered:
an import then goes through the same sample and one yes as a new setup, and that yes writes the
files. Until it does, the reply says what was read from the sheet, never that it was imported.
Rows imported unmodified are marked `imported <date>` in the change log. A row that already
exists, or comes from the agency's sheet, is kept exactly as the agency wrote it: a bare
ordinary-word term in one (`("Halden Bio" OR "HARBOR")`) is never changed or dropped. It is
raised once, in the closing question, with what it will also catch ("HARBOR on its own will also
match stories about harbours. Keep it, or search it with Halden Bio?").

## Edits

Apply the change the user typed, say it back in one line ("No brief on Fridays from next
week."), and append to the change log. Tier changes take effect next run — say so, and note that past briefs are never
retroactively rewritten: every shipped brief is immutable.

## Guardrails

- No client names, queries, or tiers in the plugin itself — everything in the client folder.
- Every query traces to the client folder, the user's own terms, or something the user said;
  never one invented from general knowledge. Two things are not invention: the words that make a
  row regulatory or capital markets are the template's, used as written with none added; and a
  second name the press uses for the field goes in only when the setup question named it
  ("fibrotic lung disease, also written pulmonary fibrosis"), so the yes confirms it.
- Deleting a query archives it (moved to the file's `## Archived` section with date and
  reason), preserving why past briefs covered what they covered. Archive it when asked, then
  raise anything the archive leaves open (a category with no rows left, the catch-all
  included); never hold the archive on that question.
