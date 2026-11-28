# Competitive Intel

**Know the field for a life-sciences client:** the client folder, competitors, the calendar of upcoming
news, and wargames with ready messages. The [getting-started guide](../core/GUIDE.md) covers the whole suite: install, the first day, every command.

**New here? Read [GUIDE.md](GUIDE.md)**: the 10-minute user tutorial: what to type, what
happens at each step, and how to read the output.

Competitive-intelligence and client-folder plugin for life-sciences communications planning.
Covers the on-demand workflow: client folders, competitor discovery, source sweeps, the catalyst
timeline, wargames, and the client deliverable. Continuous monitoring and alerts are out of
scope: plugins run only when invoked.

## Commands

| Command | What it runs |
|---|---|
| **`/gameplan <client> [space]`** | **The suite's master entry point.** Hands the client to core's set-up-a-client job, whose first two steps are this plugin's: the client folder (client-onboard), then the landscape |
| `/landscape <client> [space]` | The landscape on its own: competitor check (stop 1) → research → timeline → scenarios → the Word landscape → one approval (stop 2), with the folder updates applied on it |
| `/triggers <company or space> [horizon]` | Catalyst timeline only |
| `/wargame <event> [client]` | Scenario planning for one event |

## Skills and chain

```
/landscape  (and step 2 of core's set-up job, /gameplan)
 └─ landscape-report (orchestrator)
     ├─ client-profile          load the client folder (Stage 0)
     │   └─ client-onboard      build the client folder (step 1 of core's set-up job)
     ├─ competitor-discovery    find + tier the field
     ├─ source-sweep            retrieval primitive, authority-weighted
     ├─ catalyst-timeline       forward events, confidence-graded
     ├─ scenario-planning       branch outcomes, pre-draft messaging
     └─ client-deliverable      the Word landscape, then its one approval (Stage 6)
```

Skills pass structured HAND-OFF blocks between stages (shared rules: the core plugin's `rules/hand-offs.md`); each SKILL.md defines its own fields,
and every contract carries its own gap fields so partial-run caveats survive
stage boundaries. Routing precedence lives in `ROUTING.md` (skill descriptions carry a one-line pointer): the orchestrator
wins multi-stage requests, stage skills win their single-stage requests, and source-sweep is
the single-question primitive.

## Client folders

One folder per client (`clients/<slug>/` in the memory folder), fixed schema defined by the core plugin's
client-folder contract, built by `client-onboard`, loaded by `client-profile`, updated via
per-run updates applied when the output they came with is approved. Every
fact carries `| source | date | tier`; what only the firm can know is an explicit
`[TBD — account team]` placeholder, never a guess. The client folder's `relationships.md` feeds the
conflict check at the competitor check.

## Sources

ClinicalTrials.gov is required for discovery/timeline/landscape. **SEC filings are first-class
via EDGAR direct in Claude Code sessions** (no connector needed); the Beat and Raise connector
serves claude.ai sessions. BioCentury is preferred wherever available; without it,
editorial-pass coverage may not be claimed and becomes a named gap. PubMed preferred; Daloopa and Exa optional.

Connector registration and session availability are different surfaces, so every run starts with
source-sweep's preflight (probe by tool search, keep a ledger, run once per chain and reuse).
The fetch constraint is also probed, not assumed: claude.ai fetch accepts only search-surfaced
URLs; Claude Code fetches EDGAR and registry API URLs directly.

## Install

In Claude Code: `/plugin install competitive-intel --marketplace Bbuju055/gameplan`. It needs `core` beside it.
In the Claude app, the [getting-started guide](../core/GUIDE.md) says how.

## Changelog

- **1.2.0**: a wargame or a timeline run by itself is a Word file and a few lines in chat; the
  landscape's approval gives three lines from page one and a count of what it saves; the field's
  definition decides the first tier and no drug in the client's disease is dropped; an accepted
  claim keeps its mark in the approved file.
- **1.1.0**: /gameplan sets a client up across the suite; /landscape is a Word landscape with two
  stops (the competitor check, one approval); no draft banners, no progress page, no resume hook.
- **1.0.0**: first public release.

## Known limitations

- **No patent connector.** Patent events come from filings/news only; flagged in outputs,
  yet the report format asks for an IP assessment. Structural gap the plugin owns explicitly.
- **Non-US registries are search-mediated only.** ClinicalTrials.gov is the only first-class
  registry; trials in Australia, Europe, Korea, or China (a recurring reality for biotech
  clients) are covered via ANZCTR/EU
  CTR/ICTRP web checks per source-sweep's discipline, with the gap named when unchecked.
- **No conference-abstract source.** Abstract drops are covered only as far as web/BioCentury
  surfaces them.
- **The conflict check is only as good as `relationships.md` plus the human.** At the
  competitor check it checks the names found against the client folder and always asks the user;
  it still cannot read the firm's actual client roster.
- **Two Word layouts shipped.** The landscape (core's `gameplan-render` landscape-report layout)
  and the quarterly snapshot (`templates/quarterly-snapshot.md`); a firm can register its own
  document under either name in their place.
- **Scenario messages are drafts to adapt before use.** The landscape's one approval covers the
  document; holding statements still need fitting to the moment they're used.
