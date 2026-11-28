---
name: landscape-report
description: Orchestrate the full competitive-intelligence chain (client profile, competitor discovery, per-competitor source sweeps, catalyst timeline, scenario planning) into one landscape, a Word document with a bullet page one and the evidence after it, with two stops (the competitor check, then one approval). Use for /landscape, "competitive landscape", "landscape report", "full competitive picture", "the works on [client]", and as the second step when the core plugin's suite router sets a client up (/gameplan), or any request spanning more than one stage ("map the field and tell us what's coming and what we should prep"). Single-stage requests go to the stage skill instead; see ROUTING.md. Cross-plugin requests route through core's suite-router.
---

# Landscape Report (Orchestrator)

Every message, the notes while it works included, is in plain words, with nothing internal named and nothing said about what was read or checked (the core plugin's `rules/voice.md`). A note while it works is one plain line, or nothing: what is being done or what comes next, in plain words, is fine; it never names anything internal and never gives a count or a result.

Run the full chain and assemble the landscape. Before starting, confirm the request actually spans more than one stage — the routing table is `ROUTING.md` at the plugin root; single-stage requests go to the stage skill. This skill contains no analysis of its own — its job is sequencing, the two stops, and assembly. The intelligence lives in the four skills it calls; the reliability lives here.

## Talking to the user (this chain's part of the suite's voice rule)

The voice rule is the core plugin's `rules/voice.md`, and it alone says what a message may name
or say. The points below are how it applies in this chain; where they differ, it wins.

The people running this are communications professionals, not technical staff. Every message to
the user — intake questions, the two stops, problem reports — is plain business
English:

- **Never mention internal machinery.** No file or config names (CLAUDE.md, SKILL.md,
  plugin.json), no "PROFILE block" or "hand-off", no "seven-file" or "source-tagged"/"tier-tagged" (say "client folder", "with sources"), no "filesystem", "working directory",
  "mounted", "session state", no stage numbers, and not "the chain" — say "the run" or "the
  landscape". The user-facing vocabulary is: client folder, the competitor check, sources, the
  landscape document — the words in GUIDE.md.
- **Say what a problem means and what you need, not what broke.** Not "no gameplan root
  declared in CLAUDE.md; no filesystem mounted" but "I don't have a client folder for
  Veltrix Bio in this session. Want me to set Veltrix Bio up first (every later run reuses
  it), or just answer a few questions for this run?"
- **Choices are short, plainly framed options with their trade-off, then stop and wait.**
- Grades and tiers (FIRM/GUIDED, Tier 1, ⚠) stay — the guide's glossary covers them. Anything
  else technical gets defined in-line or left out of chat; full detail belongs in the report's
  method section, not the conversation.
- **No em dashes, anywhere user-facing.** House convention, covering chat messages,
  briefs, and deliverables alike. Use commas, colons, semicolons, a middot for label pairs
  ("Orvane · CORAL topline"), or two sentences. En dashes stay in date ranges (Nov 2–6).
- No setup notes in a client run's conversation beyond the core plugin's two plain lines: the
  client-folder contract's no-folder line and the org config's not-set-up line.

## The chain

```
Stage 0  client-profile + Intake → PROFILE block (defaults; asks only what is missing)
Stage 1  competitor-discovery → HAND-OFF: competitor set
         ── STOP 1: the competitor check (incl. the conflict check) ──
Stage 2  source-sweep (per entity) → HAND-OFF per competitor + client
Stage 3  catalyst-timeline  → HAND-OFF: catalysts
Stage 4  scenario-planning  → wargame section
Stage 5  Assembly → client-deliverable renders the Word landscape
         ── STOP 2: approve the landscape (one approval) ──
Stage 6  approved copy + folder updates applied
```

Two stops, no more. Everything between them runs without asking.

Load each stage's skill by name (the Skill tool, never its file) before running it — do not run a stage from memory of what it probably says. Each stage consumes only the hand-off blocks of prior stages plus intake; if a stage needs something not in a hand-off, that is a bug in the chain — go back and regenerate the hand-off rather than improvising the missing data.

## Progress, without a separate page

The run has no progress page of its own. Inside the core plugin's set-up-a-client job, the
client's status page shows where setup stands; on its own, the run says one line when it starts
the research ("Researching the 9 companies now; this is the long part. I'll come back with the
landscape.") and nothing until the next stop.

## Stage 0 — Intake

**Load the client profile first** (client-profile skill): its PROFILE block supplies the client,
its lead assets, known competitors, positioning, and the conflict inputs. No client folder →
offer to set the client up first (the core plugin's suite router), or collect what is needed for
this run only. That is the client's positioning and nothing else: a space the user already gave is
not asked for or confirmed again, and claims, known competitors and relationships are not asked
for here (the conflict question comes once, after the companies are found).

Defaults, never asked, offered or recited: **horizon** 18 months; **depth** full (competitors, research, timeline,
scenarios). A user who says otherwise ("12 months", "skip the scenarios") gets that. The client's
own terms (the PROFILE block's `own_terms`, per the core plugin's `rules/sources.md`) join the
run: companies go into the competitor search, phrases into the searches.

Ask only for what the folder cannot give, as one short numbered list: the **space** (indication ×
mechanism) when the folder does not make it clear, and the client's **core positioning** when the
folder has none (the scenarios need it). With a complete folder, ask nothing and start: the first message is the competitor check, after
one line for each finding the folder load made (a date that lapsed). The folder's approval, its
claims, its deadlines and its optional facts are not recited; they are in the document and on the
status page.

## The two stops

**Inside the suite router's set-up-a-client job** the two stops are the job's own. Stop 1 is shown
inside the job's first stop, with the claims: discovery runs before it, and the confirmed set and
the conflict answer are written to the folder there. Stop 2 is not asked when the research ends:
save the copy for approval, write a `draft` `landscape` row, write what the research found to the
folder marked `not yet reviewed` (the client-folder contract's Proposed updates, In the set-up
job), say nothing, and let the job go on. The job's closing review approves it, and then this
skill's steps for an approved landscape run; in the job, approving accepts no unapproved claim unless the answer names it. Run by itself, this skill stops twice, as below.

**Stop 1: the competitor check (after discovery).** Present the competitor set in its three
groups, with the space it was searched in and the companies new to the client's list
highlighted, and in the same message the conflict check:

> "Is any of these a client of the agency, or a company we have a relationship with? I can't check
> your client list myself. If we represent one, researching and planning against them is a
> conflict, so I'd leave that name out until someone decides."

Check every name against the client folder's `relationships.md` first and name any match. This is
the one conflict question of the run: it covers the names the user expected and the ones
discovery found. **Stop here: the research never begins in the same turn.** The user confirms
("looks right"), moves, adds or removes companies, and answers the conflict question. A match
leaves that company out of the research and scenarios until someone decides; record the answer
and any decision in the method section and, dated, in the client folder's `relationships.md` (a company already answered for there is named as answered and is not asked about again; a part recorded as not answered is named in that question's line and adds no stop), and say so in the stop message ("Your answer and the
decision on <company> go in the document's method section."). This is the highest-leverage correction point: a
two-minute check here saves the whole run.

**Between the stops, no questions.** Every high-relevance event and every inherited-risk event is
wargamed by default, per scenario-planning's effort rule; the user can trim scenarios at Stop 2.

**Stop 2: approve the landscape (before anything is final).** Run the assembly verification
below, have client-deliverable render the Word landscape, and present it (the assembly section
says how). One approval covers the document, any flagged claims it accepts, and the folder
updates it brings.

If the user asked for a run with no stops, honor it, but the document says on its first page that
the competitor check was skipped, and it is never approved without someone reading it: Stop 2 is
the one stop that cannot be skipped.

## Stage rules

**Preflight, before Stage 1:** the run opens with source-sweep's preflight (its Step 2), once, and
discovery and every later stage reuse its ledger (the core plugin's `rules/sources.md`, When a source is missing) — the probe, the source ledger, and the degradation protocols all live there. It also follows the core plugin's `rules/sources.md`: any connected research or company database that fits is used and named once. The ledger goes in the method section, and any pass that ran degraded is visible in the sources and gaps section. Only the trial registry stops the run (Failure handling below); every other gap is written down.

**Stage 2 scope:** sweep every tier-1 entity and the client (company-sweep archetype). Tier-2 entities get swept only for forward-looking material (feeding stage 3) unless the user asked for full depth. Tier-3 entities are not swept — they appear in the report as watch items only. This keeps run length proportional to value.

**Retrieve once, not twice.** Discovery's four passes already retrieved substantial material on
every entity they surfaced. Stage 2 explicitly reuses that material — a per-entity sweep fills
only the depth the discovery passes lacked (per-entity filings detail, publication checks,
exposures), never re-runs queries whose answers the passes already returned. Collapsing the
two retrievals is sanctioned and expected, not a corner cut.

**The client hygiene check (always, part of the client's own sweep):** read the client's public
record the way a journalist would — is their registry record current or does it contradict
their announcements? Does the investor page agree with the filings? Has guidance lapsed? These
inconsistencies are exposures the account team must hear about, and experience says they are
often the single most actionable finding of the run. Deliberate step, not a side effect.

**Stage 3** consumes the discovery hand-off and the per-entity sweep hand-offs; it should not re-retrieve what stage 2 already established, only fill forward-looking gaps.

**Stage 4** consumes the catalyst hand-off and the client positioning from intake. Pass through every high-relevance event and every inherited-risk event, and pass the hand-off's `inherited_risk` field through untouched — scenario-planning consumes it as typed input, and an entry that gets dropped here silently loses its pre-positioning deadline downstream.

## Stage 5 — Assembly

**The reader is an account director, mid-task, about to walk into a client call, not an
analyst.** Page one is the landscape: bullets they can read in two minutes. The evidence follows
on the pages after. Write page one **last**, from the assembled evidence, not from memory of the
run. The content goes to client-deliverable, which renders it with the core plugin's
`gameplan-render build --type landscape-report` (the content shape is in the core plugin's
`office-files` skill).

**Page one, bullets only, no paragraphs:**
- **Where the client stands:** at most three bullets, one line each.
- **The dates that matter:** at most three, each one line: when, what, how sure (the grade), why.
- **Biggest risk** and **biggest opportunity:** one bullet each.
- **What to do, by when:** actions with dates, not observations (pre-positioning deadlines,
  registry fixes, message work).
- **One line on confidence:** sources used and the significant gaps.

Nothing essential lives only in the evidence; nothing that isn't essential is on page one.

**The evidence, after page one:**
- **Competitors:** the set as confirmed at Stop 1, each with its group in plain words (direct,
  adjacent, horizon) and why, in one line.
- **Head-to-head** (as lines under Competitors where it matters): development stage, runway from
  filings, IP position with the patent-coverage gap flagged; company-only claims marked as such.
- **Timeline:** every event with when, who, what, its grade, and its basis.
- **Scenarios:** about one page per event: each outcome, the client's messages (⚠ kept on any
  that rests on a claim not yet approved), and the holding statement.
- **Sources and gaps:** consolidated from every stage's gap fields and the preflight ledger
  (unavailable connectors, degraded passes, undateable events, unverifiable claims,
  private-company blind spots, the patent-coverage limit). If a gap you know exists is not in any
  hand-off, regenerate the hand-off; don't patch the document.
- **Method:** stages run, the space definition, the conflict check's answer, the run date, and
  the connectors used.

**Assembly verification, before Stop 2:**

- [ ] Every forward date carries its grade; no bare dates for ESTIMATED/SPECULATIVE events. This holds on page one too: an expected event named in a bullet there carries its grade beside its window
- [ ] Every factual claim in the evidence traces to a research hand-off fact with an authority tier
- [ ] All ⚠ tags from the scenarios survived into the document, the approved copy included: an accepted claim keeps its mark
      (the client-folder contract)
- [ ] The gaps list is non-empty (a run with zero gaps means gaps were dropped, not that none exist)
- [ ] Every inherited-risk event has a scenario with a pre-positioning plan
- [ ] The conflict check's answer is recorded in the method section
- [ ] Any LAPSED-GUIDED event appears as a finding, not as a still-pending date
- [ ] Page one is bullets only, within the limits above, and everything on it is backed by the
      evidence

If any check fails, fix the document; never deliver with a failed check and a caveat. A line that
exists is corrected, never replaced by a PENDING stub. The message that reports the checks shows
the corrected page one's bullets in chat, every bullet filled (an action whose date waits on
another stage gets a proposed date, marked proposed), and says what each fix changed ("the
conflict answer is now in the method section"). A check that needed a fix is reported as failed
and fixed, never as passed.

**Presenting Stop 2.** client-deliverable saves the copy for approval as
`<Client> - Competitive landscape - <D Mon YYYY>.docx` in `<Client>/Drafts/`. Then one message, short because the file's first page says the rest: three lines from page one, each one or two plain sentences (where the client stands; the date that matters most, and why; the first thing to do, and by when); any claims the document relies on that are not yet approved (each in its own words), never shortened, because the answer accepts them; one line counting what approving saves to the client's records, by kind (new competitors, new public claims, calendar events, agency deadlines), each of them in the document, and the list is given when the person asks (with no client folder that line says approving saves the document and nothing else); and the file's name,
said as "in <Client>, Drafts" and never as a path. Then one question: "Approve as <approver name>, accepting those claims?" (the claims
clause only when there are any). Edits come in plain words: presentation changes are applied and
shown again; a substance change (a company, a date, a scenario) goes back through its stage first
(client-deliverable's revision rule).

## Stage 6 — Approved copy and folder updates

On approval (client-deliverable's approval flow does the writing):
- the approved copy is saved under the same name in `<Client>/`, the client's folder itself (`<Client> - Competitive landscape - <D Mon YYYY>.docx`); the copy shown for approval stays in `Drafts/`;
- every claim accepted is written back to the claims ledger (`accepted by <name>, <date>`), so
  no later output asks about it again;
- the folder updates are applied in the same act: new and re-tiered competitors to
  `competitors.md`, with its two lines for other plugins set from this run
  (`Class definition searched:` the space definition, and `Incumbent named by the landscape:` the approved
  comparator, or none); to the calendar, every event the contract admits (client events, high or
  medium relevance, inherited risk, outside dates an agency deadline is tied to) that it lacks,
  each pre-positioning deadline as an agency deadline on the event it serves, a changed window or
  grade, and an outcome for a past event the run confirmed. Low-relevance events stay in the
  document. A row the calendar already holds unchanged gets no update and no note;
- a `landscape` row goes to `runs.md` (`approved`, the file's path).

Then the close, in plain words: "Saved: <Client> - Competitive landscape - <date>, in <Client>." and one line saying the folder updates shown at the approval were made, with their number and nothing else: "Those <n> updates are in <Client>'s records." No update is named again, in a sentence or in a bullet. Then ask the core plugin's suite router
for the next step (its close-of-run surface); inside its set-up-a-client job that is the next
step starting, and the router's line between steps takes the place of this close (the client-folder contract's "Saved:" rule):
neither the "Saved:" line nor the update lines are said here.

A run whose landscape is not approved writes a `landscape` row as `draft` and applies nothing to
the folder.

## Failure handling

**One source stops the run: the clinical trials registry.** The competitor set rests on it, so if
it is not live (unavailable, or reached only through web search: the core plugin's `rules/sources.md`, When a source is missing),
stop before discovery and say so in plain words: what it means ("I can't
reach the clinical trials registry, and the competitor list depends on it"), and the choice:
retry, add the free Clinical Trials connector (Customize, then Connectors), or go ahead knowing
the list may miss companies. That choice is asked even when the user asked for a run with no
stops: an earlier go-ahead does not cover a failure that did not exist yet. On go ahead, discovery runs
under its own partial-run rule and is not asked again.

**Every other gap is written down, not asked about.** A source that is unavailable, a pass that
ran thin, an entity that yields nothing: the run continues, and each one goes into the
document's sources and gaps section and the method section, named plainly. Never silently: a
landscape is a trust product, and its gaps are part of what it says.
