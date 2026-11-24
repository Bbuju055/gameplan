# narrative-pulse

**Narrative Pulse.** When an investor, a partner's BD team, or a journalist asks an AI engine about
a client or its drug class: what comes back, is it accurate, who gets cited, and did our work
move it? This plugin measures that, scored against the client folder's approved claims, before each
catalyst and about monthly otherwise. Fourth plugin in the suite. New here? Read [GUIDE.md](GUIDE.md). The [getting-started guide](../core/GUIDE.md) covers the whole suite: install, the first day, every command.

Pulse is the third step when core sets a client up, and can be skipped there. A client is in scope
once a question set is in its client folder; the first run writes it, with no confirmation step.

## Commands

| Command | What it does | Stops for the user |
|---|---|---|
| `/pulse <client>`, first time | Builds the question set from the client folder, the latest landscape run and the client's own questions, writes `narrative/`, then runs the baseline (two passes per engine) | Once: approving the findings, which also approves the report |
| `/pulse <client> --baseline` | First measurement: two passes per engine, becomes the baseline | Once: approving the findings |
| `/pulse <client>` | Standing run (scored on its own; not yet compared with the first run) | Once: approving the findings |
| "add a question …", "drop the one about …" | Changes the question set from the next run | No |

## Skills and chain

`pulse-run` (orchestrator) → `question-set` (via setup) → `engine-query` → `answer-score` →
review gate → `pulse-render`. Deterministic counting (presence, share of voice, citations, noise)
lives in `scripts/scoring.py`; the HTTP engines are called by `scripts/engine_query.py`; the Claude
engine runs as a fresh subagent so the client folder cannot contaminate its answer.

## Engines

Claude, labelled "<org short name>'s own engine" in every report (the short name from the org config), is asked on
every run. OpenAI (Responses API with web search, `OPENAI_API_KEY`) and Perplexity (Sonar,
`PERPLEXITY_API_KEY`) are asked when reachable, which in practice means Claude Code with keys. In the
Claude app there is nowhere to keep a key and scripts can't reach the internet, so those two are
not measured and the report says so; the review offers pasting their answers in by hand. Gemini and Google AI Overviews are not
measured; the report says so in one line. Keys live in the environment, never in files. Engine fees
are the engines' own: at 20 questions × 3 engines × 2 passes a month, low single-digit dollars per
client per month.

## Client folder additions

```
clients/<slug>/narrative/
  question-set.md    questions in use (family, source, added_on, retired_on, confirmed = in use), framing labels, Entities
  engines.md         engines, models, conditions, ledger history
  baseline.md        first run's scores, written once
  runs/<date>/       answers.jsonl (verbatim), scores-deterministic.md, scores.md, review.md, handoffs.md
  decisions.md       append-only run log and tune decisions
```

Reads positioning, pipeline, approved-claims, constraints, the calendar, and competitors, whose
`Class definition searched:` line the landscape writes. Writes only inside `narrative/` and the client's `Deliverables/` folder,
where the report is "What Claude says about <client>" when Claude was the only engine measured.

## Hand-offs

Consumes the PROFILE block (defined by the core plugin's client-folder contract), and
reads competitive-intel's work from the client folder (dated events from `calendar.md`, the tiered set
from `competitors.md`), never from its blocks (the core plugin's `rules/hand-offs.md`). Produces `HAND-OFF: cited-outlets` (proposals for media-targeting's
AI-cited-outlets list) and `HAND-OFF: names` (re-screen candidates, which competitor-discovery checks at the next landscape). Both
are proposals; the owning plugin's operator decides.

## Changelog

- **1.1.0**: no setup question and no question confirmation; one approval that also approves the
  report; the report is named for the engines measured and saved in Deliverables/<Client>/.
- **1.0.0**: first public release. Planned: a diff against the baseline, catalyst-driven
  scheduling, `/pulse-tune`.

## Known limitations

- No comparison yet: a later run is scored on its own and is not compared with the first one;
  the report's trend line reads "no comparison yet".
- The OpenAI and Perplexity request shapes follow their 2026 APIs as documented at build time; a
  model or endpoint change surfaces as an unavailable engine in the ledger, never as a silent gap.
- Claude's answers come from a subagent in the operator's own session; the model string is the
  session's, so it is labelled rather than pinned. The subagent can see the account's saved
  preferences, memory and connectors. Its prompt tells it to ignore them and each run checks whether
  the client appears there, but this measures Claude on the firm's account, not what a member of
  the public sees.
- In the Claude app a run usually measures one engine, so "cited by two or more engines" becomes
  "cited across two or more questions", labelled as one engine.
- Accuracy is checked against the claims approved in the client folder; a claim never approved
  can only be "unverified", never "wrong".
