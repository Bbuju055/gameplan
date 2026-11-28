---
name: client-folder-contract
description: The shared client-folder contract for the whole suite. It covers how a client folder is found, the fixed file set, the provenance line every fact carries, the review-status and placeholder rules, the proposed-updates flow, the runs record, and the PROFILE block a loader emits. Loaded by other skills (client-profile, client-onboard, brief-run, pulse-run) before they read or write a client folder; not a user-facing entry point. Part one is structure and holds for any industry; part two is the field semantics the suite ships with today (life sciences).
---

# Client-folder contract

Every message, the notes while it works included, is in plain words, with nothing internal named and nothing said about what was read or checked (the core plugin's `rules/voice.md`). A note while it works is one plain line, or nothing: what is being done or what comes next, in plain words, is fine; it never names anything internal and never gives a count or a result.

One client folder per client is the canonical, approved record of what the agency
knows about its own client. Every plugin in the suite reads it the same way and writes to it the
same way. This file is the one place that says how. A skill that cannot load this contract must
stop and tell the user the core plugin is not installed, in plain words, rather than carry on
from memory.

---

## Part one — structure (holds for any industry)

### The gameplan root

The gameplan root is the agency's Gameplan folder. At its top it holds one folder per client and
per topic, each under its own name, with what a person opens (Where people find things, below), and
one folder the suite keeps for itself, `Gameplan memory - DO NOT DELETE/` (the memory folder, next
section). **Nothing else is left in the root.** A record
is changed by editing the file itself, never a temporary copy beside it, and a run makes no folder
or file there that this contract does not name: never a folder of things to delete, a `.tmp` or
`.new` file, or a note to itself. A file made by mistake that cannot be removed is named to the
person once, in plain words, so they can remove it. It is, in order:

1. the root the project declares, when it declares one ("gameplan root is: `<path>`" in its
   CLAUDE.md), an optional override for a team that keeps its files elsewhere;
2. the folder added to this project in the Claude app, or the folder Claude Code was started in.

An empty folder is a new agency, not an error: the memory folder and a client's own folder are
made there the first time something is saved to them. With no folder at all (a project with nothing added),
say once, in plain words, that Gameplan keeps each client's files in a folder on their computer
and that they add one in the project under Context, "Add a local folder"; never mention config
files, paths or settings. Then offer what can be done for this run only. With no folder, a run
saves nothing and never offers to build a client folder or a file: there is nowhere to keep one.
What it makes is shown in the conversation.

### The memory folder

`<gameplan root>/Gameplan memory - DO NOT DELETE/`, written `<memory>/` in the suite's skills. It
holds everything the suite remembers between runs and nothing a person needs to open:

| In `<memory>/` | What it is |
|---|---|
| `clients/<slug>/` | each client's folder: the fixed file set below, and what each plugin keeps for the client |
| `org-config.yaml` | the agency's settings, only the values it set (the core plugin's `org-config` skill) |
| `media/` | the reporter list the suite keeps, the saved pitch lists and their results, the agency's parsing rules |
| `build/` | the content file each Word or PowerPoint file is built from (the `office-files` skill) |
| `templates/` | an agency's own Word or PowerPoint templates, once it has registered one |
| `today.md` | the morning check's printout, when the check is scheduled |

The folder is made the first time something is saved, and is never renamed and never hidden: it
is the suite's whole memory of every client, and a folder a person can see is one they back up
and carry with the rest. To a person it is "memory", never the folder's full name or a path
("saved to memory"), and its files are never named (Storage stays out of sight).

### A folder from an earlier version

Gameplan 1.0.0 and 1.1.0 kept these at the top of the gameplan root (`clients/`, `Deliverables/`,
`org-config.yaml`, `media/`, `build/`). A root that has any of them and no memory folder is from
an earlier version, and nothing is read or written in that folder until it is moved: the suite's
commands refuse it. So the first request in such a folder, whatever it is, starts here:

1. Run `gameplan-render migrate --root <gameplan root>` (the office-files skill gives its path).
   It changes nothing and lists what would move.
2. Say it in one message and ask, asked once: "Your Gameplan folder is from an earlier version.
   I'll move your clients' records and your settings into one folder called Gameplan memory, and
   give each client a folder of its own with its files. Nothing is deleted. Move it now?" Name
   anything the list leaves where it is.
3. On yes, run it again with `--apply`, read the result, say in one line that it is done, and go
   on with what was asked. If the result is an error, nothing was changed: say so in plain words
   and give the result's list, which names each thing to drag and where it goes.
   If the result has `empty`, the move worked and a folder it emptied could not be deleted here:
   say in that same line that the old Deliverables folder is now empty and can be deleted. It is not a question.
4. On no, say that Gameplan cannot work in this folder until it is moved, and stop. It is asked
   again the next time something is asked in that folder, never twice in one conversation.

An unattended run never moves a folder: it stops, and says that the folder needs moving the
next time someone opens Gameplan.

### Resolving the folder

A client is its folder. Its name is the title of the folder's `README.md` (the first line,
without "client folder"), and its slug is the folder's own name, set when the folder is built
and never worked out again.

1. Find the client by reading the folders, not by working out a slug: list
   `<memory>/clients/`, read each folder's `README.md` title, and match what the person
   typed against the names and the folder names, ignoring case, on whole words ("Veltrix" finds
   "Veltrix Bio"; "Calderon" finds "Calderon Diagnostics" in `clients/calderon/`). One match is
   the client, called by its full name from then on. Several: ask which. A name that only
   resembles one (a different spelling) is asked about, never assumed.
2. With no gameplan root, look via the SharePoint/OneDrive connector if one is connected, or
   files the user has attached to the session. If none holds the client, take what the person can
   give for this run only (the client's positioning, the release, the names).
3. **Not found** → say so in plain terms (no config-file names, no "filesystem" talk) and offer
   to build the folder now (recommended) or take intake for this run only; with no gameplan root,
   only the second. Never fabricate a
   profile for an un-onboarded client. The only setup guidance is the no-folder line above,
   said once.
4. **A new folder's slug** is the client's name without its legal suffix (Inc., Corp., Ltd, LLC,
   plc, GmbH, AG, SA), in lowercase, letters and digits only ("Veltrix Bio, Inc." →
   `veltrixbio`). If a folder with that slug already holds another client, ask.

### Today's date

"Today", in every run and every file a run writes, is the date where the person works. A
conversation uses the date it was given. A scheduled task's clock may be on UTC and it isn't told a
time zone, so it reads the date and time in the zone its own instructions name (the saved
`org.time_zone`), with the core plugin's `gameplan-render clock --zone <zone>` (its path is in the
office-files skill), never a bare `date` and never a shell command with a zone set in front of
it, which a task's allowed list does not cover; with no zone named, it uses the date it was given.
A date the person states wins.

### Unattended runs

A run nobody started by hand (the morning check and the brief drafts it starts) uses only the gameplan
root's own files, sources reached with API keys from the environment, and web search. It never uses a
connector, because a connector may need a person to approve it in the session. The only scripts it
runs are the suite's own, which its allowed list names: `gameplan-feeds` and `gameplan-render`. The gameplan root
should therefore be a folder the scheduling machine sees as local files; a synced OneDrive,
SharePoint, or Google Drive folder serves the team and the scheduler alike. If an unattended run
cannot find the client folder that way, it stops, and saying why is its whole output. The morning
check's one file outside the client folders is `today.md` in the memory folder, which the suite
router rewrites each morning.

### The fixed file set

Eleven files, identical for every client, built by onboarding and loaded by the profile loader:

| File | Role | Trust rule |
|---|---|---|
| `README.md` | Index, build date, provenance rules, **review status**: who approved the folder and when | Approved at the end of onboarding by whoever ran it (see Who approves) |
| `positioning.md` | The client's identity, its own framing, third-party framing, hard context | Facts usable per their source tiers |
| `pipeline.md` | What the client is developing or delivering: programs, status, exposures. Its dates live in `calendar.md` | Program facts usable per their source tiers |
| `calendar.md` | Every forward date that matters to the client, each graded, with the agency deadlines it carries | Re-verify dates older than one quarter before planning on them; a LAPSED row is a finding |
| `activity-log.md` | What the agency did that the client could see or that committed the client publicly | Append-only: never edited, corrected only by a new row |
| `runs.md` | What the suite itself ran for the client, and which suggestions the user declined. Internal: never shown to the client, never quoted in a deliverable | Append-only; the suite router reads it to work out what comes next |
| `approved-claims.md` | The claims ledger: each recurring claim with a substantiation verdict and an approval column | Only claims marked approved may be used unqualified in drafts; everything else keeps its ⚠; approving or accepting it once stops the question about it, never the mark |
| `voice-and-style.md` | Register, spokesperson roles, naming conventions | Match when drafting |
| `competitors.md` | The client's competitive field: a starter set at onboarding, a tiered set once a landscape run has written one | A starter set is not a discovery output |
| `constraints.md` | Cannot-say, NDAs, quiet periods, spokespeople | **Optional.** Never asked: the person is told once that they can give it at any time, and "not given yet" is a full state. Never a blocker, never a per-run warning, never a banner (see Optional facts) |
| `relationships.md` | The agency's relationships around the client; conflict-screen inputs | Feeds the conflict re-screen; an empty file means the screen falls back to asking the user |

Plugins add their own subfolders beside these files and own them: `monitoring/` and `briefs/`
(daily-brief), `narrative/` (narrative-pulse). One optional file sits beside the eleven:
`own-terms.md`, the client's own search terms, written the first time the user gives some (the
core plugin's `rules/sources.md` says how every search uses it). Plugins never write to the
folder's files except as the rules below allow: the proposed-updates flow, the calendar's lapse
rule, the activity log's append, the runs record's append, the claims write-back, and
`own-terms.md`.

### Provenance: every fact carries a line

Every factual line carries `| source | date | tier`, where tier is one of three authority
levels: **primary** (the record itself), **analysis** (editorial or peer-reviewed assessment),
**company-only** (the client's own releases or website, which proves they said it and nothing
more). Part two says what each level means in the industry the suite ships with. In a table
cell, the three parts are separated by commas, never by "|", which splits the row.

### Words

Two words the suite uses in more than one sense, each given one meaning here. Skills keep their
own labels where a table below maps them; none adds a new one.

**Tier is three things, each with its own name.** A bare "tier" is used only inside a file
that deals with one of them.

- **authority tier**: how far a fact's source can be relied on (primary, analysis,
  company-only), the last part of every provenance line.
- **source tier**: how much an outlet counts in a client's brief (5 highest to 1, 0 suppressed),
  kept in the client's monitoring sources.
- **competitor tier**: how close a competitor is (1, 2, 3). To a person it is said as direct,
  adjacent or horizon, never as a number.

**A claim has one of four verdicts**, the ledger's. The other labels in the suite are these four
under another name:

| The ledger (`approved-claims.md`) | The sweep's verdict on a sentence | A wargame message's tag | Said to a person |
|---|---|---|---|
| ✓ supported | Supported | ✓substantiated | can use as is |
| ⚠ qualified | Supported with qualification | ✓substantiated when the message carries the caveat, else ⚠needs-support | use with this caveat |
| ⚠ needs-support | Not supported | ⚠needs-support | needs support |
| ✗ do-not-use | Contradicted | never used in a message | do not use |

**Approval is separate from the verdict.** A row reads `approved by <name>, <date>` when it was
approved at onboarding and `accepted by <name>, <date>` when someone accepted it later while
approving an output; both are approvals, and neither changes the verdict. An accepted ⚠ claim
keeps its mark wherever it appears: what stops is the question. Where a skill says
"unapproved" (Narrative Pulse does), it means any ⚠ or ✗ row, accepted or not.

**Two kinds of fact whose authority tier is not obvious.** A finding that nothing was found
(no publication, no registry record) is `primary`: its source is the searches that came back
empty, with the date they were run. What the agency itself states (what a client cannot say, a
relationship, a quiet period) is `primary`, with the person's name as its source: the agency is
the record of what it knows, and of nothing outside it.

A claim with no source line is a placeholder, written `[TBD — account team]`. There are no
unmarked guesses in a client folder, ever. What only the agency can know (constraints, retired
claims, spokespeople (who may speak for the client: how each has spoken in public is derived,
into `voice-and-style.md`), quiet periods, relationships, the positioning actually being run) is never
derived; it is asked for, and if it cannot be answered in the session the file records *who was
asked and when* so the gap has an owner and a date.

### Who approves

The person running a step approves it, and the approval is recorded under that person's own name.

- **One approver saved** (the org config's `org.approver_name`, and no `org.team_approvers`): the
  name is attached to every approval automatically, and no run ever asks "approved by whom?".
- **Several saved** (`org.team_approvers` holds other names): the first approval question of a
  conversation asks which of them is approving, inside that same question ("Approve as Priya
  Nair, J. Alvarez or Sam Ortiz, accepting the 4% claim? Say which of you."). The name given is
  used for the rest of that conversation and is not asked again. It is still one question and
  one stop. A name that is not on the list is used as given, with one line that saying "set us
  up" adds it. An unattended run approves nothing, so it never asks.
- **None saved**: the approval question asks who is approving, in that same question. A name
  read from a client's files is never offered as the approver.
  The name given is used for the rest of that conversation, with one line that saying "set us
  up" saves it. It is never a question or a stop of its own.

- **One approval per version.** Each version of an output is approved once, by saying so
  ("approved", "looks good", "use this list"). That one approval covers the output, the ⚠
  claims it accepts, and the folder updates it brings (below). A revised version is a new copy
  and is approved again; nothing already approved is asked about a second time. Inside the suite
  router's set-up-a-client job, one answer at its closing review approves each output that answer
  covers: it is still one approval for each, recorded for each.
- **The question carries what it asks about.** What is short enough to read in a message (a
  brief's draft, a list, findings) is in the same message as the approval question, written out
  in full. For a document or page too long to read in a message (a landscape, a media list's
  review page), that message shows its page one or summary, the claims the approval would
  accept and the folder updates it brings, and names the file: the person approves that file.
  Nothing said or worked out earlier in the run stands in for either.
- **The folder** is approved with its claims: the one answer that approves the claims at the end of
  onboarding approves the folder, in that same conversation, by whoever ran
  it, or later by anyone saying "approve <client>'s folder". `README.md` records the name and date. A folder that was never approved still loads and is
  used; the status page says so in one line, and no run warns about it.
- **What only a person can add stays a stop.** Choosing the competitor set, and approving
  anything that leaves the agency. Everything else is a default the user can change by typing.

### Optional facts

What only the agency knows (cannot-say, quiet periods, spokespeople, NDAs) is never asked. At
onboarding the person is told once that they can give it at any time, and "not given yet" is a full state. It is never a blocker: no run stops
for it, no run's opening message mentions it, and no output carries an "unvetted" banner. The
client's status page shows each one as "not given yet", with the sentence that adds it ("Pellamune
can't talk about the co-development partnership"). A run whose own output depends on one says so in one line, with its result, and never stops for
it: a pitch list says it does not know whether the client is in a quiet period, and records the
answer when one is given.

### Proposed updates

Facts a run produces that belong in the folder (a newly found competitor, a new public claim, a
changed status, a calendar event) are shown with the output they came from, one plain line
each, in the message that asks for its approval. The approval of that output writes them into
the relevant file in the same act, dated and sourced; there is no separate approval, and
nothing is written before it. A run whose output is not approved writes none of them. The landscape's approval gives them as one line of counts by kind, since each is in the document being approved (its competitors table, its timeline), and lists them when the person asks.
**In the set-up job** (the suite router's Job 5) the steps run on without stopping and each reads
what the one before it found, so a fact is written when it is found, sourced as always, with
`not yet reviewed` at the end of its line. In a table row the mark goes inside the row's source cell,
after the tier ("..., primary, not yet reviewed"), never as a cell of its own: a row keeps the
number of cells its header has. Taking the mark off removes those three words and nothing else.
A change-log line is history and is never edited: the approval adds one new line. Nothing is shown for it until the job's closing review,
whose approval of the output that brought it takes the mark off. A line still marked is used like
any other; the client's status page says how many there are, in one line; and an output held at
the closing review leaves its lines marked. A file's
`## Proposed updates` heading holds only what waits for an answer in a later conversation (the
monthly tuning's proposals, changes found when an existing folder is built again). Each
update is one plain line where it is shown, in this shape: "Orvane's earnings call on
5 November goes on the calendar." After the approval they are not listed again: one line says
they were made ("Those 4 updates are in Pellamune's records."). Events and deadlines go by name and date, never an id or a file
name.

### Where people find things: `<Client name>/`

The client folder is storage, and nobody needs to open it. It is kept in memory. Everything a person opens,
approves, or sends is in one folder per client at the top of the gameplan root, `<Client name>/`
(the client's name as the title of its client folder's `README.md` gives it, never a shorter form
the user typed: `Veltrix Bio/` when they say "Veltrix"), with plain file names:

`<Client name> - <What it is> - <D Mon YYYY>.<ext>`, e.g. `Pellamune - Competitive landscape - 12 Nov 2026.docx`

| What it is | File name | In `<Client name>/` |
|---|---|---|
| The competitive landscape | `<Client> - Competitive landscape - <D Mon YYYY>.docx` | `Drafts/` for approval, the folder itself once approved |
| The quarterly activities snapshot | `<Client> - Activities snapshot - <quarter>.docx` | `Drafts/` for approval, the folder itself once approved |
| The daily brief | `<Client> - Daily brief - <D Mon YYYY>.docx` | `Daily briefs/` |
| An alert brief | `<Client> - Alert brief - <D Mon YYYY> <HHMM>.docx` | `Daily briefs/` |
| A pitch list | `<Client> - <Release title> - <D Mon YYYY>.csv`, with `<Client> - <Release title> - <D Mon YYYY> - summary.csv` beside it | `Pitch lists/` |
| Coverage of one campaign (outcomes) | `<Client> - Coverage report - <Release title> - <D Mon YYYY>.docx` | `Coverage reports/` |
| Coverage over a period (clips) | `<Client> - Coverage report - <period>.docx`, with `<Client> - Coverage report - <period>.csv` beside it | `Coverage reports/` |
| A media list's review page | `<Client> - Media list - <D Mon YYYY>.html`; names that could not be written go in `<Client> - Media list - <D Mon YYYY> - for review.csv` | `Drafts/` for approval, the folder itself once approved |
| The Pulse report | `<Client> - <What Claude says \| What AI engines say> - <D Mon YYYY>.html` | `Drafts/` for approval, the folder itself once approved |
| A wargame run by itself | `<Client> - Wargame - <D Mon YYYY>.docx` | `Drafts/`, the folder itself once approved |
| A catalyst timeline run by itself | `<Client> - Catalyst timeline - <D Mon YYYY>.docx` | `Drafts/`, the folder itself once approved |
| The status page | `<Client> - Where things stand.html` | the folder itself |

`<Client>` is the client's name as above. A skill names its file as this table does and adds no name of its own. An output not in the table saves no file for a person.

- **The top of a client's folder holds only what was approved.** A file there is safe to send.
  Anything first saved for approval (the landscape, the snapshot, a page's copy for approval) is
  saved in `Drafts/`, under the name in the table, and stays there. On approval the approved copy is made in the folder itself, under the same name with nothing added. Nothing is moved, deleted or written over: the draft is the
  record of what was put to the person; a file made only after its approval (a brief, a coverage
  report, a pitch list) goes straight where the table says.
- A second version on the same day adds ` - v2` to the name (then ` - v3`), for a page as well as a file, and the earlier one stays. A new date is a new file.
- A folder moved from an earlier version may hold names ending ` - approved` or ` - 2`. They are
  read as what they are and never renamed.
- Repeated outputs get a subfolder: `Daily briefs/`, `Pitch lists/`, `Coverage reports/`.
- The status page is `<Client name> - Where things stand.html`, rebuilt by the core plugin's
  suite router (its status page section).
- Nothing a person opens or approves is a Markdown file: it is a Word file, a page (`.html`), or a
  spreadsheet (`.csv`).
- Work with no client (a topic media list, a keyword coverage report) goes in `<Topic>/` at the top of the gameplan root, under the same naming, with its own `Drafts/`.
- Nothing else goes in a client's or a topic's folder. The working file a Word or PowerPoint file
  is built from (its content, as JSON) is kept in the memory folder's `build/`, which nobody
  needs to open.

**Every run that saves something for a person names it**, by folder and file name, in the message
that presents it or in its last message: "Saved: Pellamune - Competitive landscape - 12 Nov 2026, in Pellamune, Drafts." (an approved copy: "in Pellamune.")
Storage files are never named, and nor is the client's status page when the close of a run rebuilds it.
The one exception: inside the suite router's set-up-a-client job,
the router's line between steps names what the step saved and takes the place of the step's
own close, so the step says no "Saved:" line of its own.

### Storage stays out of sight

Every human action on the client folder's files (approving, logging an action, correcting a
row, adding a term) happens in conversation or on a page, and the plugin writes the file. Ids,
storage file names, and column names stay in storage: the user hears "the CORAL readout in the
third quarter", never a row id. The same holds for every message a run shows, the notes while it
works included: the core plugin's `rules/voice.md`. The files stay readable markdown so an administrator can audit
them.

### `calendar.md`

One table row per event, under `## Upcoming`:

`id | window | entity | event | grade | relevance | source | date added | agency deadlines | outcome`

- `id` is assigned when the row is approved and never reused.
- `window` is written in one of these forms: a day (`2026-11-05`), a range of days
  (`2026-11-02–06`), a month (`Nov 2026`), a span of months (`Jun–Oct 2026`), a quarter
  (`Q3 2026`), a half (`2H 2026`), or a year (`2027`). Each has a first day and a last day: the
  window is open from its first day through its last, and ends the day after its last day. Every
  rule that asks whether a window has started, is open, has ended or overlaps another uses those
  two days.
- `agency deadlines` holds zero or more `what must be ready · by when · owner` entries, separated
  by `;`; owner is `[TBD — account team]` until named. A deadline belongs to the event it serves
  and moves with it. What must be ready is something an activity-log row can record (a draft sent
  to the client, a statement issued), never an internal step such as a draft approved.
- `outcome` stays empty until the event happens, then reads `what happened, date, source` (commas, as in any table cell), and
  the row moves to `## Past`. Past rows are never deleted.
- In: every client event, every field event of high or medium relevance, every inherited-risk
  event, and any outside date an agency deadline is tied to, within 18 months. Low-relevance
  events stay in the report that found them.
- Events that cannot be dated yet, and every SPECULATIVE event whatever its relevance, go under
  `## Watch` with their trigger condition: a speculative event is watched, never planned around,
  so it is never among the upcoming rows.
- Collisions are computed from overlapping windows when read, never stored.
- The change log records changes to rows already there (a lapse, a new grade, a move). A row a run adds
  gets one line too: the date, who approved the output it came from, and what was added ("landscape run, approved by Priya Nair | Obesity Week added"). Its `date added` gives the same day.
- Changes go through proposed updates, with one exception: when a GUIDED window ends without
  news, the row becomes LAPSED-GUIDED directly and the change log records the date. An ESTIMATED
  or SPECULATIVE row whose window has ended with no outcome moves to `## Watch` the same way, with
  what would date it again as its trigger; it is said as "expected by <date>, no news yet".

### `activity-log.md`

One table row per action:

`id | date | type | what | audience | serves | claims | outcome | recorded by`

- `type`: pitch, placement, statement, owned, spokesperson, or deliverable. Only actions the
  client could see or that committed the client publicly; internal work is never logged. What the agency sent the client is a `deliverable`, whatever it holds (a draft statement sent for sign-off is a deliverable); a `statement` is what the client said in public.
- `serves` is a calendar id or `none`; `claims` lists the approved-claims ids the action used
  publicly.
- Append-only. A plugin writes its row when what it records has happened: pitches confirmed
  sent, coverage confirmed, a deliverable sent. A saved list or an approved draft is not an
  action. A later outcome or a correction is a new row that
  points to the earlier one. Actions taken outside the suite are entered in conversation and
  recorded as `entered-by: <name>`.
- An agency deadline in the calendar with no matching row by its date is a missed deadline.

### `runs.md`

The suite's record of its own work for the client, kept so what comes next is worked out from the
folder and not from anyone's memory. Two tables, both append-only.

`## Runs`, one row each time a run makes something, and again each time what it made changes
status:

`date | capability | output | status | detail`

- `capability`: `onboard`, `landscape`, `triggers`, `wargame`, `deliverable`, `brief`,
  `brief-tune`, `pulse`, `target`, `outcomes`, `media-list`, or `clips`.
- `output`: what was made, in the words a person would use ("Q3 landscape report", "Lumen Credit
  Series B list"), followed by `serves <calendar ids>` when it was made for particular events.
- `status`: `draft` (made, not yet approved), `approved` (passed its human gate), `finalized` (a
  list saved), `sent` (left the agency), or `skipped` (the user skipped this step while setting
  the client up; the status page shows it as skipped, with the sentence that runs it). A later status is a new row naming the same output;
  the latest row for an output is its state.
- `detail`: what was added, by name, and who approved it, where the run keeps no record of its own (a media list: the reporters added, the findings
  accepted, the approver); otherwise where the plugin keeps the run's own record (a decisions log, a report path, an
  archive list name), or `none`.
- The plugin that ran writes its row at the end of the run, and again when a gate it owns passes.
  Unattended runs write theirs too. A run that stops before making anything writes no row.

**What counts as done.** A capability is done for the client once one of its rows is `approved`,
`finalized` or `sent`: something it made passed its approval. Rows at `draft` alone mean it was
started and is waiting for that approval, and a `skipped` row settles it without its being done.
Every reader of this record uses this test and none counts a bare row: the suite router's
set-up job, its rule for an unfinished setup, and the status page. Two particulars for the
set-up steps: the client folder is done once it is built (any `onboard` row), because approving
the folder is optional; the landscape is also done by an approved `deliverable` row for the
landscape document; and the daily brief is done for the set-up job once its watch terms are saved
(a `brief` row at `finalized`, "watch terms saved"), because each day's brief is approved on its day.

`## Declined`, one row each time the user answers a suggestion with anything but yes:

`date | rule | trigger key | answer`

- `rule` is a rule id from the core plugin's `rules/next-actions.md`; `trigger key` is what the
  rule fired on (a calendar id, a list name, a report date, a period, or a file date).
- `answer`: `no` (silent until the trigger key changes), `not-now` (silent for `not_now_days`, 3 as shipped),
  `mute` (the rule stays silent for this client whatever the key), or `unmute` (ends a mute).
  The latest row for a rule and key decides.
- Only the suite router writes this table.

The runs record and the activity log never share a row. A finalized pitch list is a `target` run
here and nothing in the activity log until the pitches go out.

### Writing, and what a reply may say

- **Nothing a pending question could change is written before its answer.** A run that asks
  something (what an unclear row means, whether to make a change, an approval) writes what
  depends on the answer after it, never before. The exceptions are a `draft` row in `runs.md`,
  which records only that work started, and the set-up job's `not yet reviewed` lines (Proposed
  updates, In the set-up job).
- **A reply says something was saved, added, logged or changed only when it was**: the write
  was made in that same turn and read back, silently. It says so once, with the result it belongs to and never in a message of its own: a line for a
  few things, a count for many ("Added 4 dates to the calendar"), never a line each. It is
  in the person's words, and what it says matches what the file now holds, not what was meant.
  Rows, ids and field names are never shown back.
- **A failed save records nothing.** When a save fails, no row that says it happened is written:
  no `runs.md` row and no activity-log row. The reply says it was not saved, and why.
- **`entered-by: <name>` names the person in the conversation** who reported the action (the
  approver name per Who approves). When someone else sent it, the row's `what` says so ("…, sent
  by Sam Ortiz"); nobody is asked who sent it.
- **A logged action's `type`** is one of the six the activity log allows, chosen by what was
  done. For an agency deadline that went out, it is chosen by what the deadline says must be
  ready (a statement, a pitch, a document); when that does not tell, ask one short question
  after the yes.

### Appending a row (`activity-log.md`, and both tables in `runs.md`)

- A new row goes after the table's last row: never between rows, and an existing row is never
  edited or removed. To place it, anchor on the whole last row (unique in the file), or rewrite the
  file with every old row unchanged and the new ones at the end.
- Each action is one row, written once; an id continues the file's highest (AC-007 → AC-008).
- An `approved` row's detail says who approved it ("approved by <name>"), whichever skill writes it: a row that says approved and not by whom leaves the question open for whoever reads the record.
- After writing, read the table back, with no note saying so, and check it holds the new rows
  and every old row unchanged; what the reply then says was recorded is what the file holds
  (Writing, and what a reply may say).
  If the file holds anything else (a duplicate, a row out of place, an old row changed), undo your
  own write in the same run and write it again; if that cannot be done, say so plainly.
- **What this step is called in front of a person.** A line shown while a record is being
  written says "Updating <client>'s records." and no more: never "row", "table", "draft", "read
  back" or "the contract", and never how many things are being written.

### On load, and at the close

- **On load.** Every run that loads a client folder applies the calendar's lapse rule (the
  calendar section) before it reads a date, and writes it. A line shown while that is done says
  "Bringing <client>'s calendar up to date." and no more, never "the lapse" or "the lapse
  update": what changed is said in the answer, not in that line. Reading the suite's own rules, skills or templates is never announced: a
  line shown at that point speaks of the person's own material ("Reading <client>'s files.").
- **At the close.** A run a person started that wrote a `runs.md` row ends by asking the suite
  router for the next step (its close-of-run surface) and saying only what it returns; inside
  the router's set-up-a-client job that is its line between steps. A run that wrote no row (a
  sweep or a discovery run by itself, a timeline for a space with no client) ends without it. An
  unattended run never asks.

### Staleness

A folder is a snapshot. On load, compare its build or last-updated date with today: forward-
looking entries older than one quarter are re-verified by the run's own retrieval rather than
trusted, and are listed under `staleness` so the run knows to check. Static facts (identity,
voice, history) do not expire this way.

### The PROFILE block

A loader called by another skill emits this block; downstream stages read only this plus the
folder files it points to:

The rules every block follows (empty fields, when it is written, who reads it) are the core plugin's `rules/hand-offs.md`.

```
### PROFILE: <client>
- client folder: <path> | built <date> | review_status: approved (<name>, <date>) / not approved
- positioning: 2-3 line summary of the client's core narrative and differentiation
- lead_assets: the client's lead programs from pipeline.md (name, stage), or none
- class: the `Class definition searched:` line of competitors.md, or none (no landscape has run)
- constraints_state: given / not given (optional facts: never a flag or banner; see Optional facts)
- approved_claims: count approved / count ⚠-tagged | path
- known_competitors: names from competitors.md, each with its tier | tiered set (a landscape wrote it) / starter set
- calendar: upcoming count / LAPSED count / agency deadlines due within `watch_days` (14 as shipped) | path
- own_terms: the client's own search terms from `own-terms.md`, or none
- activity: last entry date / entries this calendar quarter (the quarter today falls in, not the last three months) | path
- runs: last run per capability (date, status) / muted rules | path
- conflict_inputs: names from relationships.md the conflict re-screen must check
- staleness: folder facts older than one quarter that the run should re-verify, by file
```

---

## Part two — field semantics (what the suite ships with today: life sciences)

This part is what a domain pack replaces. Nothing in part one changes with it.

### Evidence tiers

- **primary** — trial registry records, securities filings, regulator decisions.
- **analysis** — editorial reporting and peer-reviewed literature.
- **company-only** — the client's own releases, website, and decks.

### `pipeline.md` and `calendar.md`

`pipeline.md` holds programs and their trials with the registry fields. Under `## Exposures` it
lists what the research found that the team should know before speaking for the client
(going-concern language, a delisting process, a registry record that contradicts the client's
messaging, results announced and never published), one sourced line each; the client's status
page shows them. Every forward event
lives in `calendar.md` and carries exactly one grade, assigned from the *source type*, never from
how confident the language sounds:

- **FIRM** — externally fixed date: regulatory decision dates, scheduled advisory committees,
  conference dates (not what gets presented), patent expiries, announced earnings dates.
- **GUIDED** — the company has publicly committed to a window. Real but slippable; note when
  the guidance was given and whether the company has slipped before.
- **ESTIMATED** — inferred, not stated: enrollment status plus typical readout lag, abstract
  cycles, historical cadence. Always show the basis, and never render as a bare date; windows
  only.
- **SPECULATIVE** — plausible but unanchored; include only when the possibility itself is worth
  planning for.

One status composes with the grades: **LAPSED** — a GUIDED window that has passed without news,
written `LAPSED-GUIDED`. It is a finding, not a dropped event. The tag **INHERITED-RISK** also
composes with a grade: a competitor-owned event whose outcome changes how the client's own next
data will be read.

Company guidance stays GUIDED and is never blended with registry-derived dates.

### `approved-claims.md`

One table row per claim: `# | Claim | Substantiation | Verdict | Approved`, with the
substantiation's source, date and tier in its one cell. A row always has exactly five cells: an
approval is written into the fifth, in place of the empty one, never after it.

Each recurring claim gets a verdict from the claim-substantiation standard, clause by clause for
compound claims: **✓ supported / ⚠ qualified (with the caveat supplied) / ⚠ needs-support /
✗ do-not-use**. Numbers in boilerplate are checked against filed numbers; mismatches become
qualifications. Every row has an approval column, headed "Approved" (an older folder may carry the
agency's earlier header, such as "Agency approval"; it is read the same way): verdicts are
analysis, approval is a person's. Repetition in releases or news is not evidence; a claim is never
upgraded on its strength. A claim whose only source is the company itself is never ✓ supported: it
is at best ⚠ qualified, with the caveat that it is attributed to the company ("the company says
it received ...").

**Approved once, never asked again.** At onboarding the claims are shown in chat as a short
readable list, grouped by verdict, and approved in one answer; each approved row's column reads `approved by <name>, <date>`. Later, when
someone accepts a ⚠ claim while approving any output (a brief, a landscape, a coverage report),
that acceptance is written back to this column the same way, `accepted by <name>, <date>`, so no
later output asks about that claim again. When someone refuses a ⚠ claim at an approval instead, the column reads `declined by <name>, <date>`: the claim keeps its ⚠, later outputs cut or qualify it the same way, and no later output asks about it again. Nothing else is written in the column. A ⚠ stays visible in the claims ledger and in the
agency's own records of a run (a decisions log, a landscape's method section); the daily brief a
client receives never lists which claims were accepted. What goes away is the repeated question.
A ✗ do-not-use claim is never approved or accepted, at onboarding or with any output: a line
that needs it is cut.

### `competitors.md`

At onboarding, a starter set from the client's own filings and opportunistic registry findings.
Once a landscape run has written one, a tiered set: each competitor at tier 1, 2 or 3, as the
competitive-intel plugin's `competitor-discovery` skill defines them under "Tiering", its rule
for a big-pharma program included. The definitions live there and are not restated here.

A landscape run also writes two lines other plugins read, since nothing else of the run is kept
in the folder: `Class definition searched:` (the space the run searched, in its own words) and
`Incumbent named by the landscape:` (the approved comparator, or none). A file without the first
line is a starter set.

Removed or demoted entries are kept with the reason. A registered trial that has not dosed in
years is a zombie program, not a live competitor.

### `positioning.md`, `voice-and-style.md`

Industry-neutral in shape. The hard context the positioning file carries today includes
going-concern language, listing status, disclosed setbacks, and registry records that contradict
company messaging: the uncomfortable findings the folder exists to surface.
