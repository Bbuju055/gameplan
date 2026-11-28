# Template spec: the client status page

`<Client name> - Where things stand.html`, in the client's own folder, `<Client name>/`, at the top of the gameplan root. One self-contained
page per client, made from `status-page.html` by the suite router (its Job 6), which says when it
is rebuilt. This file is the one place that says what the page shows and where each part comes
from. It answers three questions for someone who has never opened the client folder: what
has been done, what is left, and where each file is.

## Filling it

Copy `status-page.html` and replace each `{{slot}}`. Blocks between `<!-- repeat:name -->` and
`<!-- /repeat:name -->` are repeated once per item and removed when there are none. The
`<p class="empty">` line right after a block stays only when that block has no items; otherwise
it is removed. A link element is removed when it has no file. Everything comes from the client folder (`runs.md`,
`README.md`, `pipeline.md`, `constraints.md`, `voice-and-style.md`, `own-terms.md`), the org config, and, for links, the files in this client's `<Client name>/` folder; nothing is invented, and a part with no recorded
source is not on the page (who approved a step, which connected services a run used).

**Dates** are the date of the latest `runs.md` row for that step or output. **Links** are relative, to the newest file for that step or output in `<Client name>/` or its subfolders (an approved copy in the folder itself before a copy for approval in `Drafts/`), found by the
name the client-folder contract gives it; no such file there → no link, never a path from `runs.md`.

| Slot | From |
|---|---|
| `{{client}}` | the client's name, as the title of its folder's `README.md` gives it |
| `{{org_name}}` | `org.name`; unset → left empty, never `TODO(org)` |
| `{{updated}}` | today, `D Mon YYYY` |
| `{{summary}}` | one sentence: "Fully set up." or "3 of 5 steps done; the daily brief and media list are left." |
| repeat `step` | the five set-up steps in order (the router's Job 5 table): `{{step_name}}`, `{{step_state}}` (`done`, `skipped`, `todo`), `{{step_detail}}` ("Done 12 Nov", "Skipped 12 Nov", "Started 12 Nov, waiting for your approval", "Not run yet"; done, skipped or started by the client-folder contract's test, its What counts as done; a started step is `todo`), `{{step_link}}` (the link to its file, or empty), `{{step_action}}` (the sentence that runs it, for skipped and not-run steps; empty when done) |
| repeat `latest` | the latest brief, pitch list, coverage report, and Pulse page (the latest `brief`, `target`, `outcomes` and `pulse` row in `runs.md`; one with no row is left out), each `{{latest_name}}`, `{{latest_date}}`, `{{latest_link}}` |
| repeat `finding` | each line under `## Exposures` in `pipeline.md`, what the research found that the team should know before speaking for the client: `{{finding}}`, in plain words, with no source line or id |
| repeat `fact` | cannot-say, quiet periods, spokespeople: `{{fact_name}}`, `{{fact_state}}` ("Given" or "Not given yet"; spokespeople are given when `constraints.md` or `voice-and-style.md` names them, and a quiet period of "none" is given), `{{fact_action}}` (the sentence that adds it, e.g. "Say: Pellamune can't talk about …") |
| repeat `term` | each live row of `own-terms.md`: `{{term}}`, `{{term_use}}` |
| `{{folder_status}}` | the review status in `README.md`: "Approved 12 Nov by J. Alvarez", or "Not approved yet: say 'approve Pellamune's folder'" (competitive-intel's client-onboard takes that sentence) |

## Rules

- Plain words only: no ids, no storage file names, no grades without their meaning.
- Links stay inside `<Client name>/`, so the page works wherever the folder is synced.
- It never names another client.
- No em dashes.
