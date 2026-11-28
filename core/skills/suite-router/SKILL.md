---
name: suite-router
description: The Gameplan suite's front door for the agency's client work, and its sense of what comes next. Use when a request about the agency's clients could go to more than one plugin, when the user names a client of the agency without a task, when they ask what is due or next for their clients ("what's due for our clients", "where are we with" a named client), when someone asks what Gameplan can do, how to start, or which commands there are, and at the close of any suite run to name the one next step. Also sets a client up across every plugin with two stops ("set up [client]", "onboard [client]", /gameplan [client], "continue setting up [client]") and keeps each client's status page. Not for personal plans or someone's own to-do list. Routes plain language to the right plugin (core's ROUTING.md), works out each client's next actions from its calendar, activity log, and runs record (core's rules/next-actions.md), offers at most three with one recommended default each, and remembers every no. Also invoked by /today.
---

# Suite router

Every message, the notes while it works included, is in plain words, with nothing internal named and nothing said about what was read or checked (the core plugin's `rules/voice.md`). A note while it works is one plain line, or nothing: what is being done or what comes next, in plain words, is fine; it never names anything internal and never gives a count or a result.

The user should never have to remember a command or work out what is due. This skill does both:
it sends a plain-language request to the plugin that answers it, and it works out, from the
client folder alone, what each client needs next. It suggests; it never runs anything costly or
sends anything without a yes.

## First — Gameplan work or not

Take part only when at least one is true: the user typed a Gameplan command (such as `/today`);
they named a client of the agency; the request is about the agency's clients or work; they asked
about Gameplan itself (what it can do, how to start, its commands); or the gameplan root holds the agency's files (the memory folder, or what an earlier version left at its top). Otherwise
the request is not Gameplan work (their own day, a personal plan, a to-do list): answer it as
Claude normally would, say nothing about Gameplan, its folder, setup, or clients, and follow nothing else in this skill.

A gameplan root left by an earlier version is moved before anything else is done: the contract's A folder from an earlier version (one question, asked once; on a no, stop). It is the only stop this skill adds to any request.

## Step 0 — Load

Silently load the core plugin's client-folder contract, the org config (for the `next_actions`
thresholds), `${CLAUDE_PLUGIN_ROOT}/ROUTING.md`, and `${CLAUDE_PLUGIN_ROOT}/rules/next-actions.md`.
Missing contract → stop and say the core plugin is not installed, in plain words.

Then, unless this is the morning check, when the memory folder (the core plugin's client-folder contract) has no `org-config.yaml`, or has one with neither the agency's name nor an approver's name filled in, the answer opens with: "Your agency's details aren't set up yet. Say 'set us up' any time; it takes about two minutes." Nothing in the answer comes before it; a one-line working note shown earlier does not count. Say it once per conversation, then carry on. Find this out by looking at the root, silently and before the answer, never by assuming, and never say how: nothing about a file, a folder or having checked. With no gameplan root at all, say the contract's no-folder line instead, never both.

## Job 0 — Explain Gameplan

When the user asks about Gameplan itself, answer from the plugins that are installed, in plain
words, with no file, skill, folder or plugin-internal names, then stop: no queue. The reply opens
with the answer itself (after the not-set-up line, when that applies), never with what was checked
to give it.

- **What it can do:** one short sentence per step of the loop whose plugin is installed, no
  longer than the words here, and no command list: take on the client
  (a client folder from public sources, completed by the account team), know the field
  (competitors, upcoming news, messages for each outcome), watch the news (the daily brief), pitch
  (reporter lists from a press release), measure (what a campaign landed, and what AI engines say
  about the client and how to fix it). Then "You approve what goes out, once." Then one offer of
  the first step that fits where the agency is: not set up, "say 'set us up'"; no client yet, set
  one up; otherwise, what's due.
- **How to start:** the first-day steps still left, from where the agency is: say "set us up";
  set up the first client ("set up" and its name, or a made-up practice client), which runs every
  step for that client, with two stops; then each morning ask what's due. Then offer the first of
  them.
- **Which commands:** one short line per installed command, `/today`, `/gameplan` (set a client
  up across everything), `/landscape`, `/triggers`,
  `/wargame`, `/brief`, `/clips`, `/target`, `/media-list`, `/outcomes`, `/pulse`, each with what it
  does in a few words, then: "Pick one from the / list, or just say what you want."

## Job 1 — Route

Follow `ROUTING.md` in order: explicit command, then the name, then what the user wants back.
Hand the request to the skill or command it names and let that skill own the conversation. A
task that names a client is routed without a queue line in front of it: the next step comes at the
close of whatever run the task starts.

An answer to a suggestion (yes, no, not now, stop suggesting) is not a new task. Job 4 handles it,
and the reply is that answer's confirmation only: no queue, no report of a lapse applied on the way.
The queue is shown again only when the user asks for it.

## Job 2 — Work out the queue

For one client (only that client's folder is read; no other client's files are opened or named):

1. Resolve the folder per the contract. None → the queue is "build the client folder", and stop.
   A project folder that cannot be read right now (the desktop app is closed, or this is the phone)
   → say only: "I can't reach your project's folder from here. Open the Claude desktop app on the
   computer that holds it, then ask again." Never say nothing is due when the files were not read.
2. Read `calendar.md`, `activity-log.md`, `runs.md`, the README review status, `constraints.md`, and
   `monitoring/cadence.md` when there is one.
   Apply the contract's lapse rule first and write it: a GUIDED window that has passed without news
   becomes LAPSED-GUIDED in `calendar.md` with its change-log line, in a conversation as in the
   morning check. It is the one change the contract lets any run make directly; never report
   "nothing changed" over a window that has passed.
3. Test every rule in `next-actions.md` against what was read. A rule whose plugin is not
   installed, or whose input is missing, does not fire.
4. Drop what the `## Declined` table silences, rank, and keep `max_shown` items plus a count of
   the rest, all per `next-actions.md`. When `max_shown` or more are due, show exactly
   `max_shown`; the count covers only the items after them.

For "what should I do today" or `/today` with no client: do the same for every client folder in memory, rank all items together, tag each with its client, and show `max_shown` plus a
count. A client with nothing due is not mentioned.

Nothing about the queue is stored. It is worked out fresh every time from the files.

## Job 3 — Say it

Plain business English throughout: no file, folder, or column names, no rule or row ids, no
narration of what was read, and that holds for any note shown while you work: never the contract,
the root, a skill or a file. An event whose expected window passed with no news is late, never
"lapsed" or "overdue": "Orvane's CORAL results are late: expected in the third quarter, no news
yet." A client's state is two or three short sentences, about 50 words, in one paragraph: how
far setting it up has got, and the one thing that matters most now. Dates, deadlines and late
events go in the lines after the items, never in the state, and a window marked late on the way
is said only as its late line, never as "I've marked". Whether the folder was approved is for the
status page only: the chat never says a folder is unapproved, unreviewed or not signed off. The
reply to an answer (a no, a not-now, a mute) stays one or two sentences, or one short line per
answer when several come at once: the confirmation, and how to undo it where that applies. A yes
that writes rows is confirmed one line per answer in this shape, and nothing comes after the last
line: "<client>: <what> logged as sent on <date>." The line holds those three things and no more: who sent it and who received it are in the record, not in the line. No undo, no fields left blank, no rows shown back (the client-folder contract's Writing, and what a reply may say).

Each item is short: what is due and the recommended action, with exactly one yes/no question. No
follow-up branches ("if it did… if it didn't…"), no menu:
"Obesity Week starts in 6 days and the Pulse hasn't run since July. Run it now? It takes about
20 minutes." Never a menu of options, never a rule id, a file name, or a row id: the user hears
"the CORAL readout", not `EV-002`. Name the cost when it is notable (the landscape refresh is the
long one). Say each item once per conversation; if it was already said and not answered, leave
it.

Where the queue shows up:

- When the user asks what's next, or names a client with no task: for a client, its state in two or
  three short sentences and the queue (ROUTING.md); with no client, the queue across clients. After
  the items, the lines a person would otherwise only get from the morning check, worked out the same
  way (step 1 and the block, below) and tagged with the client when across clients: passed with no
  outcome recorded, then late with no news yet, then coming up soonest first. Coming up means only what falls
  within `watch_days`, agency deadlines and events alike: a deadline this week comes before an event
  next week, and anything further off is neither named nor counted. One event per line. These lines
  have their own cap, apart from the items': at most `max_shown` of them, passed, late and coming up
  counted together, then their own "and <n> more" for the rest. They are statements with no question, and are left out when there are none. A line never
  replaces a queue item: a lapsed event with no wargame still has that item, ranked and counted as
  usual.
- Whenever the queue is shown in a conversation and the memory folder's `today.md` exists but is
  more than 3 days old, one line after the items: "The morning check last ran on <date>; the
  computer it runs on may be off or asleep." Once per conversation.
- Nothing follows the items but the count of the rest, those lines and the morning-check line: no
  instructions on how to answer, no extra notes.
- At the close of a suite run during the set-up job (Job 5): no queue. What it returns is the
  line between steps (Job 5, step 2), which also names what the step saved, in place of the
  step's own "Saved:" line; then the job goes on to its next step.
- At the close of any other suite run: the calling skill has written its own `runs.md` row; work out
  the queue again and say only the top item, or every item the run itself just made due (new
  calendar rows from a landscape run, say), within `max_shown`. R15 stays out of this, except at
  the close of a brief, where it offers the next client's.
- At the top of each brief draft and in the memory folder's `today.md`: see the morning check
  below.

## Job 4 — Act on the answer

- **Yes** → hand off to the skill or command the item names, as if the user had asked for it.
  The skill runs its own gates; the router's yes approves the start, nothing more.
- **R15** → asked as one line: "Today's briefs for Veltrix and Calderon aren't started. Start with
  Veltrix?" A yes starts `/brief` for the first client named, with a person present (never
  `--draft-only`). A no or a not-now writes one row per client named, with today's date as the key,
  so it comes back on the next publication day. The confirmation follows the rule for any answer: one or two sentences.
- **No** → append a `no` row to `## Declined` (rule, trigger key, today). The item returns only
  when its trigger key changes.
- **Not now** → a `not-now` row; it returns after `not_now_days`.
- **"Stop suggesting that for <client>"** → a `mute` row for the rule. Say once how to undo it:
  "Just tell me if you want these again." An un-mute request appends `unmute`.
- **R5** → asked as "Did it go out?", and the item stops at the question: what a yes would record
  is not said. **Yes it went out** → append the activity-log row per the contract: the deadline's
  what, a type chosen from it, `serves` its calendar id, today's date unless the user gives one,
  recorded by `entered-by: <name>`, the person in this conversation (the client-folder contract's Writing, and what a reply may say).
  When the user names a sender other than
  themselves, the row's `what` says so ("…, sent by Sam Ortiz"). `audience` and `claims` take what the user
  said, else `not given`; the confirmation does not mention them (a later correction row can fill
  them).
- **"It went to the client"**, said for an approved output (whenever the person says it; nothing asks
  for it or prompts it) → append the activity-log `deliverable` row per the
  contract (the output, its version, who received it, the date it went), and a `sent` row for it
  in `runs.md` under the capability of that output's `approved` row. Never asked
  by this skill.
- Those rows, the R5 rows, the Declined rows, and the set-up job's `skipped` rows are the only
  writes this skill makes to a client folder, besides the contract's lapse rule; in the memory folder it writes the morning check's `today.md`, and in each client's own folder its status page.

## What's coming for a client (a read of the calendar)

"What's coming for Pellamune?", "what dates matter for Pellamune?": answered from the client's
`calendar.md` alone, after the lapse rule. Nothing is researched, and nothing is written but the
lapse. In date order, one plain line each: what, when, and how firm in plain words (confirmed,
the company's own guidance, an estimate, speculative); then what is late, as late; then the
agency's own deadlines with what must be ready, by when and whose it is; then, in one line, what
is being watched with no date yet. No ids and no file names. A timeline is built only when the
person asks for a refresh, or for a space with no client folder (competitive-intel's routing).

## Job 5 — Set up a client (two stops, every step)

"set up Pellamune", "onboard Pellamune", `/gameplan Pellamune`, a yes to "set up your first
client", and a yes to R16 all land here. The user should never have to know which plugin comes
next: this job takes the client through every step, in order, and says where it is at each one.

**The steps**, each run by its own plugin, each only when that plugin is installed:

| # | Step (as the user hears it) | Run by | Its rows in `runs.md` |
|---|---|---|---|
| 1 | Client folder | competitive-intel's client-onboard | `onboard` |
| 2 | Competitive landscape | competitive-intel's landscape-report | `landscape` |
| 3 | What Claude says about <client> (or "What AI engines say", when more than Claude is measured) | narrative-pulse's pulse-run, first run | `pulse` |
| 4 | Daily brief | daily-brief's monitoring-config: the watch terms are saved, and no brief is made | `brief` |
| 5 | Media list | media-targeting's media-list-run | `media-list` |

Whether a step is done, settled (skipped) or only started is the client-folder contract's test
(its `runs.md` section, What counts as done): a step with `draft` rows alone is not done, the client folder excepted: it is done once it is built, whatever its row says, and is never named as a step left. Steps
already done are not run again, and a started step is picked up at the approval it waits on. A practice
client (client-onboard's practice mode, a made-up company) runs step 1 only: there is nothing
public to research, so steps 2 to 5 get `skipped` rows and one line says so ("Acme Bio is a
practice client, so I've built its folder and skipped the research steps.").

**1. Start at once.** "Set up <client>" is the go-ahead, and nothing asks to start: the work begins
in that same turn. Nothing is said first but a one-line working note (the plan is said at the first
stop, below: a message before the work is a working note, and a plan does not fit in one). Nothing
is asked (not the therapeutic area, public or private, or anything a step works out when it runs).

**2. The first stop: one message, one answer.** Run step 1 (client-onboard builds the folder and asks
nothing in this job) and the landscape's competitor discovery, then stop once. The message holds,
in this order and nothing else:

- one opening line, "<Client>'s folder is built. This is the first of two stops.", then the plan
  for what comes after, in two or three lines: what is still to run once this is answered (the
  steps still left, in the user's words), that it can take up to 30 minutes, give or take, and
  uses a good share of the plan's usage, that it will not stop again until the end, when it asks
  once for approval, and that any step can be skipped by saying so;
- the claims, grouped and worded as client-onboard's Step 5 shows them, with what "all" covers;
- the competitor set as the landscape's Stop 1 presents it, without its conflict question, which is asked last;
- one line that is never a question: "Tell me any time what <Client> can't say, its quiet
  periods or its spokespeople, and I'll keep them.";
- last, the one question, both parts in one line so one reply answers both: "Approve the claims and this competitor list as <approver name>? And is any of these companies a client of the agency, or one we have a relationship with?" (the approver per the
  contract's Who approves). The line before it gives the landscape's reason for asking, once: the
  suite cannot check the agency's client list, and a company the agency represents is left out
  until someone decides.

The answer is read for all of it: the claims approved, or the ones named as not approved; companies
moved, added or removed; the conflict answer. An answer that leaves one of the three unsettled gets
one follow-up for that part alone, once. An approval that says nothing about the conflict question has
not answered it: ask that one question again, alone, with no thanks or acknowledgement before it. If it is still not answered, record it as not
answered, never as "no conflict", and go on. An answer to one part is recorded as said: "none is a client of ours" is written as not a client, with the relationship part not answered, never a "no relationship" nobody said; that part is not asked again in this conversation. Then write, before anything else runs: the approvals in
the claims ledger; the folder as approved (approving the claims approves the folder: `README.md`
and an `approved` `onboard` row, in the same act); the confirmed set and the space searched in
`competitors.md`, as confirmed by that person on that date; and the conflict answer in
`relationships.md`, dated, so no later landscape asks it again about these companies.

**3. Run to the end without stopping.** Steps 2 to 5 run in order, each by its own skill, and
none of them stops for its own approval inside this job. No step is cut short to save time or usage: each does all it would do run by itself (the check of what Claude says is the full first run, every question asked twice and the baseline saved). A choice the job makes for itself is never recorded as a person's decision: no line it writes carries a person's name for something that person did not say. Each saves what it made for approval
(its copy for approval in the client's `Drafts/`, a `draft` row in `runs.md`) and the job goes on to the
next. What the research finds on the way (a dated event, a new public claim, a changed status) is
written to the folder when it is found, sourced as always and marked `not yet reviewed`, because
the steps after it read the folder (the contract's Proposed updates, In the set-up job). The daily
brief step saves the watch terms as built and makes no brief: the first brief is run and approved
like any other, the first morning it is asked for. The media list's new names are added to no list
before the closing review. Between steps nothing is said but a one-line working note. One thing
still stops the run midway: the landscape's failure stop, when the clinical trials registry cannot
be reached. "Skip <step>" (or "not now" for one) writes a `skipped` row for it first, before the
next step starts, and moves on. After each step, rebuild the status page (Job 6). The status page is
rebuilt only after that row is written, the `draft` row included, so the page never calls a step "not
run" whose work is saved. When a later step finds something that changes what an earlier step made
(a newer date, a company not on the list), it writes the fact to the folder, marked as above, and
rewrites that step's copy for approval under the same name: never a second copy or a version number,
because nobody has seen the first one yet. A company found after the first stop is written to `competitors.md` with the note `conflict not yet checked`, since nobody has answered for it. The closing review's block for that step says in a few words what was corrected.

**4. The closing review: one message, one answer.** When the last step has saved its work,
rebuild the status page. With nothing waiting on an approval (every step left was skipped, or it is a
practice client), there is no closing review: go straight to the ending. Otherwise one message:

> **Everything for <Client> is ready for your approval.**

Then one short block for each step that made something, in step order, three lines at most, because
the files carry the rest:

- the file's name, said as the contract says it, with "in <Client>, Drafts" (the daily brief has no file: its block is headed "Daily brief: the news watch is set up", never the
  words "no file", and gives the watch terms in one line and
  what yesterday would have brought, as a count and the top story);
- one sentence: the most important thing in it;
- what approving it does, in the person's terms: the claims it relies on that are not approved, each
  in its own words, followed by "This claim stays unapproved unless you say 'accept it'." (Approving a block never accepts a claim that is not approved); companies found after the first stop, by name, with "Approving confirms none of them is a client of the agency; tell me if one is."; for the AI-engines page, "Approving it confirms these findings: ...", naming what
  the engines got wrong, never that the approval "accepts" a wrong fact; for the media list, how many
  names it would add and how many findings.

Then the one question, the message's last line: "Approve all of it as <name>, or tell me what to
hold or change." (who is approving, per the contract's Who approves, is inside this question).
The answer is read for each block:

- **Approved**: that step's own skill finishes as it does after its approval (the approved copy,
  the `approved` row, the names added to the list), and the `not yet reviewed` mark comes off every
  line that step brought. A claim that is not approved is written `accepted by <name>, <date>` only when the answer names it
  ("accept it", or the claim in the person's words); otherwise its row stays as it was and the
  approved copy keeps its mark. For each company found after the first stop, the answer given by
  the approval is written to `relationships.md`, dated, and the note comes off its line in `competitors.md`; the approved copy's method line says they were confirmed with the approval, with its date, never that they have no conflict answer; a company named as a client is left out as the landscape's conflict rule says.
- **Held**: it stays as saved, at `draft`; what's due shows it, and nothing warns about it.
- **A change asked for**: that step's own revision rule runs; the changed copy is shown alone and
  approved on its own.

What was approved and what was held is said in one line, then the ending below, in the same reply.

**5. If it stops partway** (the conversation ends, usage runs out, the user stops it): nothing is
lost, because each step wrote its own rows. "Continue setting up <client>", or a yes to R16,
picks up from the first step with nothing saved: that request is the go-ahead, so nothing is asked
before the work goes on. When the person stops it themselves ("stop there for today"), finish what their
answer settled, start nothing else, and say in one line where it stands and that "continue setting
up <client>" picks it up. Say which step it is resuming at, and which steps are left. When every
step has saved its work, it goes straight to the closing review. A step the user skips gets the
line "Skipped: <step>. Starting: <next step>.", on a line of its own. When the request itself
skips the step it would resume at, that line is the resume line and opens the reply: it already
names the step resumed at and the step that is left, so nothing is added to it about the steps
done before or the steps left.

**6. The ending.** After the closing review's answer, rebuild the status page (Job 6) so it
shows every step, then:

> **<Client> is fully set up.** Everything is in <Client>'s folder.
>
> **From here:**
> - **Each morning:** open this project and ask *what's due today?* and I'll start <Client>'s news brief.
> - **When you have a press release:** say *pitch this for <Client>* and paste it.
> - **When news breaks about a competitor:** say *what do we say if…*
> - **The rest shows up when you ask what's due:** when to check the AI engines again, when the landscape needs a refresh, and when a coverage report is due.

The morning line says what is true for this root. With the morning check running (the memory folder's `today.md` is dated within the last 3 days), it ends instead: "<Client>'s draft news brief is
already there to review." Nothing in this ending says Gameplan acts unasked.

Name only what was set up: a skipped brief drops its mention from the first line; a skipped media
list drops the pitch line's "media list" wording but keeps the line. The first line stands in
for the contract's "Saved:" line for the status page, so no file is named, and nothing else
goes in the ending: a skipped step's sentence is on the status page. Then, once per gameplan root,
only if the session has a scheduler and only if this client's daily brief was set up (not
skipped): "Want the brief drafted before you open the app each
morning? It runs while the computer is on and the Claude app is open." A yes sets up the morning
check (below); a no is recorded like any declined suggestion.

## Job 6 — The status page

A line shown while the page is rebuilt says "Updating <client>'s page of where things stand.",
never "the status page".

`<Client name>/<Client name> - Where things stand.html` at the top of the gameplan root, made from
`${CLAUDE_PLUGIN_ROOT}/templates/status-page.html`. What the page shows, and where each part comes
from, is in `${CLAUDE_PLUGIN_ROOT}/templates/status-page.md` and nowhere else: read it first and
fill the page from it. Rebuilt after each
set-up step, at the close of any run a person started that writes a `runs.md` row for the client
(never by the unattended morning check, and not for an answer that writes only a Declined row: the page shows steps and outputs, not what was declined), and when the user
asks "where are we with <client>?" (then also given in chat: the client's state in two or three
sentences, then one line naming the page and its folder, before any queue).

It is a page for people: plain words, no ids, no storage file names. Like `today.md`, it is a
printout worked out from the files, never read back as state. After each rebuild, run
`gameplan-render check <the page> --root <gameplan root> --client <slug>` (the office-files
skill) and fix anything it reports: another client's name never appears on the page.

## The morning check (unattended)

Optional. The daily routine needs no schedule: someone opens the project and asks what's due, and
the conversation gives them the queue, the same lines and the day's briefs. For someone who wants
it, one scheduled job per gameplan root runs `/today --scheduled` every day, in the morning: each client's own
publication days decide whether its brief is started. Nobody is in
the conversation, so it asks nothing, and the contract's unattended rule holds: local files,
API keys and web search, never a connector. For each client folder in the root:

1. Work out the queue (Job 2), without R15: this check starts the drafts itself. A rule that needs
   a connector (a reporter list behind one, say) is skipped, and its not-checked line says where the list lives and why: "the media list health check: the list is in <where it lives, such as Microsoft 365 or a Google Sheet>, and a connector is only used when someone is in the conversation." Add the coming-up lines: FIRM and GUIDED events under `## Upcoming` whose date, or the
   start of whose window, falls within `watch_days`, and agency deadlines due within it, leaving
   out anything already shown as a queue item (one counted in "and n more" keeps its line). A
   deadline is its own line even when its event has an item (a wargame suggestion for that event,
   say); only a deadline that is itself a shown item is left out. Add a passed line for each FIRM
   event that has passed with no outcome recorded (next-actions defines passed).
2. If daily-brief is installed and the client has `monitoring/`, run its
   `/brief <client> --draft-only` (daily-brief's brief-run skill in draft-only mode), every
   morning, even when its sources may be out of reach: the brief checks its own cadence, degrades
   on its own, and saves a draft that names its gaps, which is what the reviewer opens. Never skip
   it on a guess. The draft opens with this client's block. A brief that fails is named in that
   client's block, and the job moves on.
3. Write the client's block into `today.md`.

The block:

```
### NEXT: <client> | <date>
- <item, in the words of Job 3, as a statement> | up to max_shown item lines
- <item>
- <item>
- and <n> more
- coming up: <event or deadline, and its window or date, in plain words> | one line each, omitted when none
- late, no news yet: <event, and when it was expected, in plain words> | omitted when none
- passed, outcome not recorded: <event and its date, in plain words> | one line each, omitted when none
- not checked today: <what was skipped and why, in plain words> | omitted when nothing was
```

Every line of the block is a statement: no question, and no instruction to anyone ("ask whether
it went out", "wargame it"). The question is asked later, in a conversation. The item cap is
per block: each client's block shows up to `max_shown` of that client's own items, whatever
another client's block shows, and its "and <n> more" counts only that client's rest. The block
has no cap on its coming-up, late and passed lines: each is written. The cap on them in Job 3
is for the conversation only.

`today.md`, in the memory folder, is rewritten every morning: the date, one block per client with
something in it, then, when there are any, "Nothing due for <n> other clients." It names every client, so it is
internal: never copied into a client folder or a client's own folder, never quoted to a client. Its
date is how anyone can tell the check is still running.

Unattended, the router writes nothing except the contract's lapse rule and `today.md`. Answers
come later, in a conversation, and are recorded then.

**Setting it up.** Offered once, at the end of the set-up job (Job 5), and set up whenever
someone asks for it. Create the job with the session's
scheduler, if it has one: named "gameplan morning check", every day (or on the days the person names), running `/today --scheduled`
from the gameplan root, with the agency's time zone in its instructions ("Work in America/New_York:
read today's date and the time with gameplan-render clock --zone America/New_York"), because a task
isn't told one. The zone is `org.time_zone`; when it is not saved yet, use the one the person has
given, or ask once before creating the job, "Which time zone should the morning check use?". The
zone is saved when the job is created, in that same step and never before: as its full name
("Eastern" is `America/New_York`) in the agency's `org-config.yaml` (in the memory folder), changing only that value and reading it back. When no job is created (the session has no scheduler, or the person
only asked what the job would be), nothing is saved. Keep the time the person names, exactly. With
none named, set it 30 minutes before the earliest "draft ready by" time in the clients'
`monitoring/cadence.md` files (7:00 AM local when there are none). Then say in plain words where it
stands. A task reaches this project's files only if the folder is on the task itself; the project
having it isn't enough. If the folder shows on the task, say so. Otherwise say it isn't finished
until the folder is added on the task in the app. Either way, each run reaches the folder only
while the desktop app is open on this computer and the computer is awake. Without a scheduler, say
in plain words that it can't be set up from here and that asking what's due each morning does the
same job, with brief drafts starting on a yes. Only someone who asks how to run it themselves gets
this line, to schedule on a machine that sees the gameplan root as local or synced files:
`claude -p "/core:today --scheduled" --permission-mode acceptEdits --allowedTools 'WebSearch WebFetch Bash(python3 *scripts/gameplan-feeds*) Bash(python3 *scripts/gameplan-render*)'`.
Nobody is present to approve a tool, so the line lets the job write its files, search the web, and
run the suite's two commands: `gameplan-feeds`, daily-brief's command for its keyed news feeds
(without it those sources become gaps), and `gameplan-render`, which gives the job the date and
time in the agency's zone. The job runs no other command. Later clients need nothing; the job reads every folder.

**When it stops.** A stale `today.md` is said in conversation (Job 3, where the queue shows up).

## Never

- Run a capability, start research, or draft anything without a yes.
- Send, publish, or contact anyone.
- Store the queue, or keep a suggestion list anywhere but the files it is worked out from;
  `today.md` is a dated printout of it, rewritten each morning, never read back as state.
- Show more than `max_shown` items unprompted, or repeat one the user has answered.
