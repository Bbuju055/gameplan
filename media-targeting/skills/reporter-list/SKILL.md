---
name: reporter-list
description: The one place the agency's reporter list (the media log) is read and written to. Finds where it lives (a Microsoft 365 workbook, a Google Sheet, a file in the gameplan root, or the suite's own list), reads it live and normalized with the parse-coverage line and its age, and writes approved new names and health-check findings to pending review (or, for the suite's own list, into the list), never into the agency's log. Called by build-target-list (read), curate-and-archive (write), and /media-list (both); not a user-facing entry point. Cross-plugin requests route through core's suite-router.
---

# Reporter List

Every message, the notes while it works included, is in plain words, with nothing internal named and nothing said about what was read or checked (the core plugin's `rules/voice.md`). A note while it works is one plain line, or nothing: what is being done or what comes next, in plain words, is fine; it never names anything internal and never gives a count or a result.

Every skill that needs the agency's reporter list goes through here, so the list is read one way
and written one way. The agency's own log is its source of record: this skill reads it and never
writes it. Writes go to pending review, for the log owner to promote on their own schedule. Only
the suite's own list, kept for an agency with none, is written directly, and only on approval.

## Config preflight

Nothing about this step is said to the operator; every message follows the core plugin's
`rules/voice.md`. Load the suite's org config (the core plugin's `org-config` skill). This skill needs
`media_log.*` (source, location, column map, log owner),
`pending_review.file_name`, and the core `next_actions.list_stale_days` threshold.

**Find the source.** `media_log.source` when set. Unset: `m365` if `media_log.sharepoint_site`
is filled; else `suite` if `<memory>/media/reporter-list.md` exists; else there is no list
yet.

- The source's own location values still TODO(org) → the list's location is not known: read
  nothing. The caller decides what that means for its run; the sentence it says is: "I don't
  know where your media list is yet. Say 'set us up' and tell me where it is."
- No list yet (the agency keeps none of its own, and the suite's list has not been started) →
  nothing is missing from setup: read nothing, and the sentence is: "You don't have a media list
  yet: your first media list starts one." It may add, once: "If you already keep one somewhere, say 'set us up' and tell me where it is." In neither case improvise a candidate pool from the web.
- **Unattended runs** (per the core contract) read only `file` and `suite` sources. A list behind
  a connector is skipped and said once in the run's output.

## Read

1. **Read the media log live**, once per run, from its source. No mirror, no cached copy; the
   source is the record. **The main log is read-only to this plugin, permanently.**
   - **m365** — the workbook through the Microsoft 365 connector, which needs the organization's
     admin to approve it once. If it returns a summary rather than the rows, or a tab other than
     the log's, say so and stop: a target list is never built from a summary (the list is the pitch list's
     input, not a source: the core plugin's `rules/sources.md`).
   - **google** (not yet verified against a live Drive connector) — the Sheet through the Drive
     connector's `download_file_content`, which returns exact rows as CSV. Never
     `read_file_content`, whose natural-language form can be incomplete. The export is believed
     to cover only the first tab, so the log rows must be there; if the rows look like another
     tab's, say so and stop.
   - **file** — the file at `media_log.file_path` under the gameplan root: a `.csv` read
     directly; an `.xlsx` through the core plugin's `gameplan-render read-xlsx <path>` (its path
     is in core's `office-files` skill), which
     returns one sheet's rows as text (dates as YYYY-MM-DD), lists every sheet's name under
     `sheets`, and never writes the file. It reads the first sheet unless told another: when
     `media_log.main_sheet` is filled, add `--sheet "<that name>"`. If the rows read look like
     another tab's, say so, name the workbook's other tabs, ask which one holds the log, and read
     that one; then write `media_log.main_sheet` to the agency's `org-config.yaml` (in the memory folder), changing
     only that value, and read it back (with nowhere to write, use it for this run and say it
     won't be remembered). Never
     install anything to read it; if the command is missing or fails, say so and stop.
   - **suite** — `<memory>/media/reporter-list.md`, the `## Reporters` table. Its columns
     are fixed (`templates/reporter-list.md`); the column map does not apply.
2. **Confirm the columns on the first read.** If the column map is still TODO(org) for an m365,
   google or file source, match the real header row and the first rows to the fields, and ask once
   in plain words: "Your list has these columns. I'd read 'Journalist' as the reporter's name,
   'Publication' as the outlet, 'Covers' as the beat, and I didn't find a region column. Is that
   right?" Use no rows and give no row counts until they confirm or correct it. Then write the map to the agency's `org-config.yaml` (in the memory folder), changing only those values, and read it back; a column with no match is `""`.
   With nowhere to write, use the map for this run and say it won't be remembered. An unattended
   run doesn't ask: it skips the list and says so once.
3. **Normalize rows** using the column map and the agency's rules in
   `<memory>/media/parsing-rules.md` (beat synonyms, delimiter tolerance, skip rules). No
   such file yet → use the shape of the plugin's `config/parsing-rules.md`, parse conservatively
   and say so once. **Always report parse coverage in one line:** "Read 412 rows, used 407, skipped
   5, mostly blank beat fields." A row with no reporter name is always skipped, whatever else it holds. Rows skipped for naming an outlet and no reporter are said once, by outlet ("2 rows named an outlet and no reporter, so they were left out: Medwire, Credit Signal"). A row skipped as a repeat is named ("a second row for
   <reporter>"). When more than one row in twenty is skipped for a reason other than being blank or a
   repeat, ask what those rows mean; when the operator
   explains, save the rule to that file, starting from the plugin's copy the first time.
4. **State the list's age once it is old.** For a `file` source, the file's last-modified date;
   for the suite's own list, the oldest `Last verified` among the rows the caller uses. Older than
   `list_stale_days` → one plain line with the date ("This list was last updated in June, so some
   names may have moved."). A connector list's age is not stated.

Hand the caller the normalized rows, the parse-coverage line, and the age line if any. The rows
carry the suite's field names (reporter, outlet, beat, email, geography, tier, notes), not the
log's own headings; the column map is what translates one to the other. A cell holding several
beats or regions comes back as separate values, written with commas (fintech, lending, payments),
never as the log's own joined string.

## Write

Only rows the operator approved, by name, in conversation or on a review page. Most runs never
write at all. Columns per `templates/pending-review-columns.md`, for every source.

- **m365** — the pending-review file, `pending_review.file_name`, a separate small CSV in
  the same folder as the media log. The M365 connector writes whole files only, so: read the
  small file, append the rows, replace the file. **This is the plugin's only SharePoint write.**
- **file** — the same CSV beside the log file in the gameplan root, appended the same way.
- **No review file yet** (m365 or file) is not a failure: create it in that folder with the fixed
  header row and this run's rows. Nobody has to make it first.
- **google** (not yet verified against a live Drive connector) — a new Sheet named "<file_name without extension>
  <YYYY-MM-DD>" through the Drive connector's `create_file`, holding the header row and this run's
  rows. A second write on the same day adds "-2". Never edit or delete a Sheet in the agency's
  Drive.
- **suite** — straight into `<memory>/media/reporter-list.md`, created from
  `templates/reporter-list.md` the first time. New names are added under `## Reporters` with
  today as `Added` and `Last verified`. An approved health-check finding updates the reporter's
  row (a move) or moves it under `## Left` (left the beat, left journalism); nothing is deleted.
  Every write adds a `## Change log` line: date, what changed, who approved.
- **Health-check findings** on an agency's own list (m365, file, google) are pending-review rows
  with `Source` set to "Health check: moved", "Health check: left beat", or "Health check: left
  journalism", the new outlet or beat in the existing columns, and the bylines in `Evidence`. They
  suggest a correction; they never change the log.
- If a write fails (file locked, write scopes not enabled, the file could not be created), say so
  plainly and hand the rows back to the caller, which saves them as a for-review CSV in the client's folder (export-list in a pitch-list run, media-list-run's step 7 in a
  media-list run) — the chain never stalls on this.
- Tell the caller where the rows went, so it can say so: the review file, a new review Sheet by
  its name, the suite's own list, or handed back.

## Prohibitions

- Never write to the media log. Not a cell, not a tab, not ever. Only the suite's own list is
  written directly.
- Never edit or remove a pending-review row; append only.
- Never write a row the operator did not approve.
- Never guess contact info for a row being written.
