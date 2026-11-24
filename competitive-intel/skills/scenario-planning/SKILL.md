---
name: scenario-planning
description: Wargame upcoming competitive events for a life-sciences client. For each catalyst, branch the plausible outcomes, define the client's message and media posture per branch, and produce holding language prepared in advance, drafts to adapt and approve, so the team can respond in hours instead of days. Use whenever the user asks to "wargame", "scenario plan", "prep messaging for", "what do we say if", or wants pre-planned responses to a competitor readout, approval, regulatory action, or data release. Also invoked as the final analytical step of the landscape-report skill, consuming the catalyst-timeline hand-off. Cross-plugin requests route through core's suite-router.
---

# Scenario Planning

Every message, the notes while it works included, is in plain words, with nothing internal named and nothing said about what was read or checked (the core plugin's `rules/voice.md`). A note while it works is one plain line, or nothing: what is being done or what comes next, in plain words, is fine; it never names anything internal and never gives a count or a result.

Turn a catalyst timeline into pre-planned communications, so that when a competitor's news drops, the client's response is a matter of executing a reviewed plan rather than convening a panicked call. This is the plugin's highest-value skill and its most judgment-heavy: retrieval feeds it, but the output is strategy, and strategy is where a human must stay in the loop. Everything this skill produces is **draft-for-review, never send-ready** — say so on the output itself.

## Inputs

- **Catalysts** — from catalyst-timeline's hand-off or named directly by the user. The hand-off's `inherited_risk` field is typed input, not context: every entry in it gets the full-depth treatment described below. **Direct entry rule (no hand-off):** when the event arrives as a user phrase rather than a graded hand-off — whether via /wargame or this skill firing on its own — establish the factual ground first: run a focused source-sweep on the event and grade it per catalyst-timeline's rules before branching. Branching on an ungrounded event produces confident trees about a mischaracterized event; a lapsed or mis-graded catalyst changes which branches even exist.
- **Client positioning** — the client's current core narrative and differentiation claims. Load from the client folder (client-profile skill) when one exists — `positioning.md` and `approved-claims.md` are the canonical inputs, and only claims approved there may appear unqualified in messaging. If there is no client folder and no user-supplied positioning, ask and stop there: no branches, messages, or holding statements until it is answered; wargaming without knowing the client's own story produces generic crisis-comms filler.
- **Constraints** — anything the client cannot say (regulatory, legal, partnership NDAs). Load from the client folder's `constraints.md` when it exists and apply what it holds. These are optional facts (the core plugin's client-folder contract): when none are given, say nothing about it at the start, ask nothing about it (a reply that asks for the client's positioning asks for that alone, not which points are public) and add no banner; the "Before any of this is used" list below already asks the reader to check them.

## Which events to wargame

Not everything. Effort follows two axes: the event's confidence grade (from catalyst-timeline) and its client relevance. Full scenario trees for FIRM/GUIDED events with high client relevance; a single contingency paragraph for everything else that is dated (an ESTIMATED event, an event of medium relevance whatever its grade, and a conference whose content is not yet known); a watch-trigger only for SPECULATIVE items. Over-planning is a real failure mode — a 40-page wargame nobody reads loses to a 6-page one the account team internalizes.

One override: events typed `inherited_risk` in the catalyst hand-off are wargamed at full depth regardless of who owns them — they are high client relevance by construction, since their outcome sets how the client's own data will be read. Their wargame carries an extra obligation the ordinary trees don't: the **pre-positioning asset**. The timeline supplies a pre-positioning deadline; the differentiation argument (why the client's molecule, design, or population survives a class-level readout going the wrong way) must be drafted for publication *before* that deadline, as its own deliverable. A branch tree whose mitigation first appears in the response branch has missed the point — deployed for the first time after bad news, the argument reads as damage control.

## Branching

For each event, enumerate the outcomes that would produce *materially different* comms situations — not every possible result. Most clinical/regulatory events branch three to five ways. Standard trees:

**Competitor data readout:** clean win / mixed (efficacy hit, tolerability or subgroup problems) / miss / delay-or-silence. The fourth branch is routinely forgotten and routinely happens.

**Competitor regulatory decision:** approval as expected / approval with restrictive label / CRL / AdComm surprise (either direction).

**Competitor corporate event:** partnership or acquisition / financing (validates or crowds the space) / pipeline deprioritization.

For each branch, work through four layers:

1. **Read** — what this outcome actually means for the client's competitive position, stated honestly. If a competitor's clean win is genuinely bad for the client, the internal read says so; messaging built on a false internal read collapses under the first sharp journalist question.
2. **Narrative terrain** — what story the media will default to within 24 hours, and whether the client is a character in it. Use BioCentury and trade-press framing patterns from source-sweep to predict this rather than guessing: how did coverage frame the last three analogous events in this space?
3. **Message** — the client's 2–3 key points for this branch. Each point must be *substantiable*: run any factual claim through source-sweep's claim-substantiation standard before it goes in. A message that requires an unsupported claim gets flagged, not polished.
4. **Posture and assets** — proactive, responsive, or silent; which spokespeople; and the pre-draftable assets: holding statement (always), reactive Q&A (for high-relevance branches), proactive pitch angle (only where the branch genuinely favors the client — forced positivity reads as spin and burns credibility with beat reporters).

## The uncomfortable branches

Every wargame must include the branches where the news is *bad for the client* — competitor's clean win, client's own event going poorly if the client has catalysts in the window. These are the branches where pre-planning has the highest value and where the temptation to skip is strongest because nobody enjoys drafting them. A wargame with only favorable branches is a pep talk. A wargame asked about one event branches that event: the client's own event gets its tree when it is the event asked about, or when the wargame covers a window it falls in.

## Output

```
## Wargame: <space / client> — built <date>
Holding statements and messages are drafts to adapt before use.

### Event: <name> — <window> — <grade>

**Branch <n>: <outcome>** (est. likelihood: high/med/low, with basis if any)
- Read: ...
- Narrative terrain: ...
- Key messages: ... [each tagged ✓substantiated / ⚠needs-support, these two words only, exactly one on every key message in every branch, never both and never none (the client-folder contract's Words maps them to the ledger's four verdicts; an accepted claim keeps its ⚠); company-only or unpublished support is ⚠needs-support, on every message that leans on it]
- Posture: ...
- Holding statement: <draft>
- Q&A: <for high-relevance branches>

**Pre-positioning plan** (inherited-risk events only): the differentiation
argument to have on the record before the window opens — draft, proposed
channel (bylined piece, data publication, conference remarks), and the
deadline inherited from the timeline.

### Cross-event notes
Messages that must stay consistent across branches and events —
the things the client cannot say in one scenario without foreclosing another.

### Watch triggers
For undateable/speculative events: the observable signal that should
activate a full wargame.

### Before any of this is used
- Factual claims checked against primary sources (any ⚠ still open is named)
- What the client cannot say applied
- Spokespeople available for the high-relevance windows
- The client has seen the language for the uncomfortable branches
```

## Recording the run

When the wargame is for a client with a folder, append a `wargame` row to its `runs.md`, per the
client-folder contract's "Appending a row": the wargame, `draft`, naming every event it covered
and followed by `serves` with the calendar ids of those already in the calendar (events still
only proposed have no id yet; the name is what the
router's rule R7 matches them by). Run directly rather than inside the landscape chain, then ask the core
plugin's suite router for the next step (its close-of-run surface) and give it in one line
just above "Before any of this is used", which stays the last section of the reply: nothing
follows it.

## Constraints

**Substantiation is not optional.** Any factual claim about trial results, regulatory status, or competitive standing in a key message must pass the claim-substantiation check (source-sweep, Step 5 standard) or carry the ⚠ tag. The tag must survive into the final document — silently dropping it converts a known risk into a hidden one.

**Cross-branch consistency beats per-branch optimization.** The best message for branch A is worthless if it contradicts what the client must say in branch B a month later. Do the cross-event pass; it catches these.

**Don't speak for the competitor's data before it exists.** Pre-drafted language must never assert what a competitor's unreleased results show. Structure holding language around the client's own position, with bracketed slots for the actual facts once known. That includes their tone: "a welcome
sign", "encouraging" or "disappointing" speaks for data nobody has seen. Neither does a general welcome placed beside the acknowledgement ("progress in treatment options is important for patients"): next to unseen results it reads as a verdict on them.

**Likelihood estimates are soft.** If assigning branch likelihoods, base them on something (BioCentury expectations, trial design, base rates for the phase and modality) and show the basis. Unfounded percentages create false precision that misallocates prep effort.
