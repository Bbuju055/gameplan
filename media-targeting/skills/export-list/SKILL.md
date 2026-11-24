---
name: export-list
description: Generate the pitch-list spreadsheet (a CSV of every segment's ranked reporters, each with the angle to lead with, plus a summary CSV) in the client's Deliverables folder and name the files to the operator. Fires automatically after a successful save, or standalone when the operator asks to re-export any previously saved list. Cross-plugin requests route through core's suite-router.
---

# Export List

Every message, the notes while it works included, is in plain words, with nothing internal named and nothing said about what was read or checked (the core plugin's `rules/voice.md`). A note while it works is one plain line, or nothing: what is being done or what comes next, in plain words, is fine; it never names anything internal and never gives a count or a result.

Turn the finalized list into the spreadsheet the team actually pitches from.

## Config preflight

Load the suite's org config (the core plugin's `org-config` skill) and read: `org.confidential_footer` (TODO(org) → omit the footer, don't invent one). Standalone mode fetches the list from the archive (campaign-history's "Reading the archive"); no root, the script failing, or no such list → say so and stop. Chain mode with no gameplan root: there is nowhere to write a file, so write none and name none; curate-and-archive shows the final list in the conversation instead.

## The file — spec in `templates/target-list-template.md`

- **One CSV for the whole list**, segment by segment, each ranked by score: segment, rank, reporter, outlet, beat, score, match reasons, angle to lead with, contact info, pitch-history flag, added-by. Excel opens it directly. An accepted discovery is on the list: in its segment, after that segment's log reporters, marked as discovered in added-by, and never ranked among them. A discovery that was not accepted is not on the list.
- **Reactive hits carry their deadline** (Deadline column: "closes Sep 3") and sort to the top of their segment.
- **A flag from another client's list names no client in the file.** The file gets forwarded, so the flag stays and only the name goes: "on Bluewater Capital's list saved 13 days ago" is written "on another client's list saved 13 days ago". This client's own flags read as saved. A possible match (the same name saved under a different outlet) keeps its flag and names that outlet. The reply to the operator may still name the other client.
- **Discovered reporters** whose email wasn't publicly sourced carry "verify contact before sending" in the contact column, and one with no email found at all reads "not found: verify manually" — the export must preserve the discovery trust boundary, not launder it.
- If the finalize-time pending-review write failed, discoveries also get their own **"for your review"** CSV, in pending-review column order, and one line in the hand-over telling the operator to paste its rows into the pending-review file.
- **Summary CSV** (`<Client> - <Release title> - <D Mon YYYY> - summary.csv`, beside the list): client, release title, date, operator, segment counts, list id and version — plus the parse-coverage line from the build, so the files record what the log looked like that day.
- Saved in `Deliverables/<Client>/Pitch lists/` (the core plugin's client-folder contract; a list with no client: `Deliverables/<Release title>/`), named `<Client> - <Release title> - <D Mon YYYY>.csv`, with ` - summary.csv` and, when needed, ` - for review.csv` beside it. The reply names the file and its folder ("Saved: Pellamune - Series A - 12 Nov 2026, in Deliverables, Pellamune, Pitch lists.").
- Write the CSVs directly (UTF-8, a header row) and run the core plugin's `gameplan-render check` on each before handing them over. Never install anything to make a spreadsheet. Load the core plugin's `office-files` skill first, without announcing it: it gives the command's path and the full rule.

## Modes

- **Chain mode** (after curate-and-archive): generate and deliver. No offer: the angles are already on the list.
- **Standalone mode** ("re-export the Lumen list"): fetch the named list with `lists` and `show-list` — current version by default, earlier versions on request — regenerate, deliver. No offer here either, even for a list saved without angles: a blank column is said once as what the saved list holds ("The saved list has no angles, so that column is blank."), with no offer to fill it or run /target again.

## Prohibitions

- Never alter list content at export time — formatting only; the archive holds the truth. The one wording change is another client's name in a flag (above).
- Never strip pitch-history flags or "verify contact" notes to make the file look cleaner.
