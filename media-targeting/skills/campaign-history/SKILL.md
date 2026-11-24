---
name: campaign-history
description: Answer archive questions in plain English at any time, such as who we've pitched, when, for whom, hit rates by reporter/outlet/segment/client, how discovered reporters perform vs. log reporters. Fires whenever the operator asks an archive-shaped question. Prose and tables, never file names or commands. Cross-plugin requests route through core's suite-router.
---

# Campaign History

Every message, the notes while it works included, is in plain words, with nothing internal named and nothing said about what was read or checked (the core plugin's `rules/voice.md`). A note while it works is one plain line, or nothing: what is being done or what comes next, in plain words, is fine; it never names anything internal and never gives a count or a result.

The archive's front door. Every number comes from `scripts/archive.py`; nothing is counted by hand, and the archive's files are never read directly.

## Reading the archive

The archive is plain files under `<gameplan root>/media/archive/`, which this script reads for every skill:

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/archive.py" <command> --root <gameplan root> ...`

| Command | Gives |
|---|---|
| `lists [--client NAME] [--release TEXT]` | each saved list: version, date, whether it is current, `conflict_with` |
| `show-list --list-id ID` | one list in full, with its outcomes |
| `history [--client NAME] [--reporter TEXT] [--all-versions]` | one row per reporter on a saved list, newest first; `--all-versions` adds what later versions replaced |
| `performance --by reporter\|segment\|discovery [--client NAME]` | counts and hit rates |
| `pitch-history --today D --client NAME --reporters FILE [--max-days 90]` | the saved lists these reporters are on (a JSON list of `name` and `outlet`), for this client and others, with `saved_on`, `days_ago`, `outlet_match` and any recorded `outcome`; lists outside the window come under `older` |

- **No root, or the script is missing or fails** → say in plain words that the history couldn't be read, and why. Never answer from memory or count by hand.
- **`problems`** in a result are files the archive couldn't use. Say each once, in plain words ("One saved list couldn't be read, it may not be downloaded to this computer, so it isn't counted here."). Never drop one silently.
- **`conflict_with`** means two people saved the same version from folders that hadn't synced. Say so once; both count until a new version replaces them.
- **`--client`** takes the client's name as saved, its leading words ("Lumen") or the name with no spaces. `client_matched` says which saved client it was read as: name it when it differs from what was asked. `ambiguous_client` means the name fits two saved clients: ask which, never pick.
- **A reporter is matched by name.** `outlet_match: different` is a possible match: say the outlet it was saved under and let the operator judge. A list under `older` is on record: say when it was saved.
- **Nothing on record is not "never pitched".** The archive holds lists saved in this folder from when it started: say "no pitch on record", and when the answer rests on what isn't there, add: "This checks lists saved in this project's folder. Pitches made elsewhere won't show." Earlier history kept elsewhere isn't imported.

If the operator asks about the archive without a question, offer the common ones (recent
campaigns, a reporter's pitch count, hit rates by client or segment) and wait.

## Typical questions, and where the answer lives

- "Who have we pitched for Client X, and when?" → `history --client`
- "How many times has Reporter Y been pitched across all clients this quarter?" → `history --reporter`
- "Show me the list from Client X's last raise." → `lists`, then `show-list`: the current version by default; earlier versions on request
- "Do we have any broadcast targets for this client, ever?" → `history --client`, each row's `snapshot` tier
- "**Who actually covers us?**" → `performance --by reporter`, `--by segment` — hit rates by reporter, outlet, segment, client
- "How have discovered reporters performed vs. log reporters?" → `performance --by discovery`

## Presentation rules

- Prose first, a small table when the answer is a list. Column counts stay readable; explanations live in the surrounding prose.
- **A saved list is not a pitch.** The archive counts reporters on saved lists (`times_listed`, `last_listed`); it knows a pitch went out only from a recorded outcome of covered or no coverage. Asked who was pitched, say who was on which saved list and what is recorded for each, and say "pitched" only where an outcome or the client's activity record shows it. This holds for every sentence of the answer, the one that sums up a table included: three saved lists are "on three saved lists", never "pitched three times".
- **Distinguish "not covered", "not pitched" and "not yet tracked":** entries with no recorded outcome are unresolved, not failures, and a reporter recorded as not pitched is never a miss — say "12 on the list, 4 covered, 5 didn't, 1 not pitched, 2 not yet tracked (run /outcomes on that campaign)".
- Hit rates are covered over covered plus no coverage; never compute a rate over unresolved or not-pitched entries.
- Cross-client questions are fair game — the archive covers every client in this folder.

## Prohibitions

- Never show commands, file names, or ids to the operator.
- Never editorialize a reporter's worth beyond what the numbers say — "hasn't covered the last three pitches" is data; "waste of time" is not this skill's call.
