# Daily Brief

**The daily client media brief and coverage reports,** each approved once before it goes out. The [getting-started guide](../core/GUIDE.md) covers the whole suite: install, the first day, every command.

**New here? Read [GUIDE.md](GUIDE.md)**: the 10-minute user tutorial: what to type, what
happens at each step, and how to read the output.

The daily client media brief as a Claude plugin: gather scored signal, cluster duplicates to the canonical
source, curate a categorized draft with client-specific Signal lines, stop once for the
approval, render the standard Word deliverable into the client's Deliverables folder, and log every decision for the
monthly tuning loop. Sibling to competitive-intel, both built on the core plugin's
client-folder contract: same gameplan root, same client folders, same voice and approval
discipline; that plugin owns strategy (landscapes,
catalysts, wargames), this one owns the daily editorial product.

## Commands

| Command | What it runs |
|---|---|
| **`/brief <client> [date] [--draft-only \| --alert]`** | **The master entry point.** Profile + monitoring load (set up from a sample brief the first time) → gather → curate → one approval → Word deliverable → decisions log. `--draft-only` is the scheduled-morning mode (stops with the draft saved); `--alert` is the off-cycle radar-alert path (checks for wargamed holding language first) |
| `/clips <client or keywords> <period>` | The coverage report: feed + web + an attached monitoring export → verified clips with messages carried, firm-driven or organic, tone → one approval → Word report + clips spreadsheet |

## Skills and chain

```
/brief
 └─ brief-run (orchestrator)
     ├─ (core contract)          resolve the client folder per core's client-folder-contract
     ├─ monitoring-config        set up from a sample brief (one question); edits by typing
     ├─ signal-gather            radar handoff + feed + registry + web; cluster; tier
     ├─ story-curate             score, categorize, summarize, Signal lines; ends at the gate
     │   ── THE ONE APPROVAL ──  under the setup name; ⚠ flags accepted in the same answer; decisions.md
     ├─ brief-render             the Word deliverable; refuses without an approval record
     └─ brief-tune               monthly, over decisions logs (suggested by the suite router)

/clips
 └─ clips-run                  the coverage report; reuses signal-gather's feed and clustering
```

Skills pass structured blocks (GATHER, BRIEF DRAFT) with explicit gap fields, so partial-run
caveats survive stage boundaries and land in the deliverable's method note.

## Client folder additions

Monitoring lives in the client folder, never in the plugin (zero hardcoding):

```
clients/<slug>/
  monitoring/queries.md     query rows built from the folder: category order, boolean terms, priority, sources
  monitoring/sources.md     publication tiers 5→0; unrated sources get "?" and a proposal, never a guess
  monitoring/cadence.md     publication days, holidays, times, reviewer, recipients, alert path
  briefs/<YYYY-MM-DD>/      draft.md · decisions.md   (the Word file goes to Deliverables/<Client>/Daily briefs/)
  briefs/skipped.md         one line per calendar skip
```

Shipped briefs are immutable; config changes apply forward only. All monitoring changes append to per-file change
logs; deletions archive.

## Sources

**Web search is the only hard requirement.** Radar, an optional external monitoring service
with a read-only handoff API (`RADAR_API_BASE` + `RADAR_API_TOKEN`,
consuming the `RadarToQcHandoffV1` manifest at `/api/reports/qc-handoff`) and the Newsdata feed
(`NEWSDATA_API_KEY`) are first-class when configured and degrade to named gaps when not;
signal-gather's preflight probes rather than assumes, and web-mediated fallback never claims
feed-grade completeness. ClinicalTrials.gov via session tools. Machine-readable:
`.claude-plugin/source-dependencies.json`.

Radar boundary honored: radar's facts are consumed read-only; all prose is written on this
side, from the client folder's approved claims and constraints. (Radar's contract carries a
negative-capability attestation for exactly this split.)

## Scheduling

No schedule needed. On a publication day, asking the suite what's due (core's `/today`) offers
each client's brief that hasn't started, and a yes runs it with its one approval. For someone who
asks for it, the optional morning check (core's `/today --scheduled`, one job per gameplan root) runs
`/brief <client> --draft-only` every day for every client with monitoring set up; the run checks
`cadence.md` (holidays skip with a record; a human asking always overrides). A new client is picked
up with no setup.

## Changelog

- **1.1.0**: setup from a sample brief with defaults; one approval under the setup name; the Word
  file in Deliverables/<Client>/Daily briefs/; no unvetted banner; tuning as one list; any
  monitoring connector used in briefs a person starts.
- **1.0.0**: first public release.

## Known limitations

- **Owned social is not wired.** Owned-social rows in an imported workbook become visible
  phase-2 notes, never dropped. Wiring it is a small fetch script once the account team wants owned-social
  echo in the brief.
- **Radar coverage requires the client to be a radar brand.** signal-gather names the gap and
  the operator action when not; it cannot add brands to radar itself.
- **No .docx binary template registered yet.** brief-render builds from the shipped structure
  spec (`templates/daily-brief.md`); registering a firm .docx template in the gameplan
  root will standardize typography beyond what element-by-element building guarantees.
- **The brief is only as complete as its queries.** The tuning loop narrows the miss rate
  (reviewer-added stories are its strongest signal) but the first line of defense is a good
  set of searches at setup.
- **Everything ships through a human.** By design; there is no unattended send. The scheduled
  run stops at the draft.
