---
name: curate-and-archive
description: Own the conversation from results-on-screen until "finalize", from plain-English list editing to one save to the campaign archive in the project's folder with approved discoveries saved where the agency's list keeps new names (through reporter-list). Fourth stage of the /target chain. Cross-plugin requests route through core's suite-router.
---

# Curate and Archive

Every message, the notes while it works included, is in plain words, with nothing internal named and nothing said about what was read or checked (the core plugin's `rules/voice.md`). A note while it works is one plain line, or nothing: what is being done or what comes next, in plain words, is fine; it never names anything internal and never gives a count or a result.

The results are on screen; this skill owns the conversation until the operator finalizes. Editing is plain English; the save writes one new file; the pending-review write is the only write beside the media log in the entire plugin.

## Config preflight

Load the suite's org config (the core plugin's `org-config` skill) and read: `pending_review.file_name`, `media_log.*` (folder location for the sibling file), `media_log.log_owner`.

**No gameplan root (a project with no folder) → warn BEFORE curation begins, not at save time:** say the core plugin's client-folder contract's no-folder line (Gameplan keeps each client's files in a folder on their computer, added in the project under Context, "Add a local folder") unless this conversation has already said it, then what it means here: "Without one I can build this list and show it here, but I can't save a spreadsheet or check it against future campaigns. Add a folder first, or carry on and I'll give you the final list here." Both come with the results, above the invitation to edit; the choice is the operator's, and nothing more is asked about it. With no folder, finalize saves nothing and writes no review rows: the final list is shown in the conversation as a table, group by group, with every column the spreadsheet would have, and the reply says once that nothing was saved.

## The curation loop

Apply and re-present each turn: drop, add, reorder, accept discoveries, manual adds, change a group or an angle. Manual adds who are in the log come with their log row; unknowns are treated like discoveries — snapshot captured, **no guessed contact info**. Pitch-history flags persist visibly through every edit; warn once per flagged reporter, never nag. Recognize natural finalize phrasing ("use this list", "finalize", "lock it in", "that's the list", "we're done"). That is the run's one stop, and its approval: the operator is recorded as the approver (the client-folder contract's Who approves).

## On finalize, in order

1. **Assemble one payload** (internal, never shown) as a temporary JSON file outside `media/archive/`: `client` (`display_name`), `press_release` (`title`, `news_type`, `summary`), `operator`, `segments` (`name`, `rationale`, `priority`), `entries`. Every entry carries a `reporter_snapshot` frozen at save time (`name`, `outlet`, `beat`, `email`, `geography`, `tier`, `notes`), `segment`, `score`, `match_reason` (the one sentence the scoring carried, with the citation links in it for discoveries and reactive hits), `angle` (the angle to lead with), `pitch_flags`, `added_by` (`agent`, `agent-discovery`, `agent-reactive`, or `operator`).
2. **Save it:** `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/archive.py" save-list --root <gameplan root> --today <today> --payload <file>` — the single permitted archive write path. It validates, writes one new file that is never changed afterwards, numbers the version and marks what it supersedes when a list already exists for the same release. Before saving, run its `lists` command, and if the client name is ambiguous against existing clients (near-match, different spelling), confirm with the operator. Skills never write archive files directly. A line shown while the list is being saved says "Saving the list." and no more. A refused payload is a bug to fix, not something to force. If the script is missing or the save fails, say plainly that the list was not saved and why, hand over the export anyway, and never say "saved".
3. **Stage approved discoveries** through this plugin's `reporter-list` skill (loaded by name; its Write section), which puts them where this agency's list keeps new names: the review file (created the first time), a new review Sheet, or the suite's own list. **This is the plugin's only write beside the media log.** It runs only here, and only when the operator approved at least one discovery — most runs never write there at all. **Never touch the main log.** If reporter-list hands the rows back (the write failed), put them on their own sheet in the export instead — the chain never stalls on this.
4. **Confirm in operator language:** "That's the list: 37 reporters across 3 groups." (export-list's "Saved:" line names the file; this line never says "Saved"). Then, when discoveries were approved, one sentence on where they went, as reporter-list reported it: the review file → "M. Torres added to the review file for [log_owner] to approve." (no list owner saved: "for whoever looks after your media list to approve"); a new review Sheet → "M. Torres is in a new review sheet, <its name>."; the suite's own list → "M. Torres added to your media list."; handed back → "The review file couldn't be written, so M. Torres is in <the for-review file's name>, beside the pitch list." Never name a file that was not written. Nothing is said here about checking coverage later: the suite router lists that check when it is due (its rule R6), and it is seen when someone asks what's due or the morning check runs. Never say you will check back. Then hand off to export-list, which saves the spreadsheet and names it.

## Recording the run

For a client-linked list whose save succeeded, append a `target` row to the client's `runs.md` at finalize (a failed save records nothing: the client-folder contract's Writing rule): the list's
name as the operator knows it, `finalized`, the version. A list with no
client records nothing.

## Logging pitches to the client's activity record

Finalizing saves a list; it does not mean anyone was pitched, so nothing is logged at finalize. Nothing is said about it at finalize, and nobody is asked to come back and report it: the outcomes run counts the list as pitched and asks who was not. When the operator says the pitches went out (now or in a later session), that is the confirmation: in the same turn, without asking again, append one `pitch` row per reporter actually pitched to the client's activity log, per the core contract (reading it is not announced: the one line shown at this step is the one below): the angle as `what`, reporter and outlet as `audience`, the calendar event the angle hangs on as `serves` (or none), the approved claims the angle uses as `claims`, and `media-targeting, pitches confirmed sent <date>` as who recorded it. A row looks like this, whatever the log already holds: `| AC-001 | 2026-09-02 | pitch | Cash-flow underwriting for community lenders | Dana Okafor, The Ledger Daily | EV-001 | C2 | | media-targeting, pitches confirmed sent 2026-09-02 |`. A line shown while the rows are written says "Adding the pitches to <client>'s activity record.", with no count. Then confirm in one or two plain lines: how many pitches went on the client's activity record and who was left out. No row, event, or claim ids and no file names.

## Prohibitions

- Never write the main media log — not a cell, not a tab, not ever.
- Never write archive files directly; `scripts/archive.py` is the only door.
- Never guess contact info for manual adds or discoveries.
- Never finalize without explicit operator phrasing that means "done".
- Never show the payload, the archive's files, or file paths to the operator.
