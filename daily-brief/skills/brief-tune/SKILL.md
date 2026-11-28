---
name: brief-tune
description: The monthly learning pass over a client's decisions logs. Mine the reviewer's keep/drop/edit decisions and reasons for patterns, then propose specific query and source-tier adjustments as changes the person says yes or no to. Use monthly per client, when the user says "tune the brief", "why do we keep dropping X", or accepts the suite router's monthly suggestion. It applies only the changes the person says yes to, and never claims a pattern thinner than its evidence. Cross-plugin requests route through core's suite-router.
---

# Brief Tune (The Learning Loop)

Every message, the notes while it works included, is in plain words, with nothing internal named and nothing said about what was read or checked (the core plugin's `rules/voice.md`). A note while it works is one plain line, or nothing: what is being done or what comes next, in plain words, is fine; it never names anything internal and never gives a count or a result.

The decisions logs hold months of a professional's judgment,
with reasons. This skill turns them into monitoring improvements — always as proposals, because
the account team owns the config.

The user is the account lead. Plain business English in conversation: no file names, headings,
or section names; the proposal files hold the detail and the quotes.

## Inputs

Resolve the client folder per the core plugin's client-folder contract, then read every
`briefs/*/decisions.md` in the lookback window (the org config's `brief_tune_days`, 30 as shipped), plus the current monitoring
files. Under 10 briefs → say once that the evidence is thin, go on without asking, and label
every proposal "thin evidence".

## Patterns to mine (each proposal cites its instances)

- **Consistently dropped sources** → propose a tier cut, quoting the drop reasons and count
  ("dropped 7 of 7 times in 30 days; reasons: 'aggregator, always late'"). A source dropped
  for one story's irrelevance is not a pattern; the reasons decide, not the count alone.
- **Consistently dropped query rows** → propose narrowing the boolean terms or cutting the
  priority — quote what the row actually returned versus what survived the gate.
- **Reviewer-added stories** → the strongest signal in the log, so their proposal leads the list: what did the gather miss, and
  which query or source would have caught it? Propose the addition, with the missed stories as
  the evidence.
- **Repeated Signal-line edits in the same direction** → propose the underlying fix: a
  constraints.md cannot-say added or widened when the edits keep out something the client can't
  say, else a positioning.md clarification or an approved-claims.md addition (routed as a client
  folder proposed update), not a prompt tweak hidden in the plugin.
- **Category moves** → propose re-homing the query row whose stories keep getting moved.
- **Tier-? sources accumulating** → propose tiers for unrated sources seen 3+ times, from
  the evidence of how the reviewer treated their stories.

## Output

Proposals appended under `## Proposed updates` in the relevant monitoring file (or the client
folder file, for constraints, positioning or claims items), each dated, evidenced, and self-contained. Then **one
short list in conversation, one line per proposal** (one sentence, one proposal per line, so a
new source and the search that goes with it are two lines; any count said is the number of
lines; the quoted reasons stay in the file) with its evidence in a few words ("Stop showing Endpoints' daily
roundups: you dropped them 14 times"), one line on what was looked at and
found healthy (the null results are part of the report: "queries look well-fitted" is a
finding), and one question: "Make these changes?" A yes applies them all; "all but the second",
or naming the ones to skip, applies the rest. After the yes the reply is one line and no list: "Those <n> changes are made." No change is named again. The list, the healthy line and the question are one
message, the last one: nothing said earlier in the run stands in for the list. Nothing takes
effect until that answer; it converts
the proposals to canon with a change-log entry, like every other client folder update.
The entry names the person who said yes (the client-folder contract's Who approves), never a role
and never this skill. A row that did not change gets no entry.

The whole message, in shape (the words are an example):

> Four changes from 22 briefs:
> 1. Stop showing Endpoints' daily roundups: you dropped them 14 times.
> 2. Watch Fierce Pharma: you added 3 of its stories by hand.
> 3. Narrow the biosimilars search: you kept 2 of 25.
> 4. Add "no comparisons with Arvex" to what the client can't say: you made that edit 5 times.
>
> Looked at and fine: the other searches, the rated sources, and the categories; Yahoo Finance stays (kept 2, dropped 5).
>
> Make these changes?

Nothing else is added: no section on where the proposals were written, no quotes.

Append a `brief-tune` row to the client's `runs.md` (the proposals, `draft`, the files they were
written to; an `approved` row when the user says yes), then ask the core plugin's suite
router for the next step (its close-of-run surface). The router suggests the next pass a month on
(its rule R13), so this skill never asks the user to remember it.

## Honesty rules

- Every proposal quotes its instances in the file it is written to; no proposal from vibes.
- Contradictory evidence is shown, not resolved silently (the reviewer kept it twice, dropped
  it five times — say both numbers).
- This skill reads logs; it never re-litigates individual editorial decisions or scores the
  reviewer. The reviewer is the ground truth being learned from.
