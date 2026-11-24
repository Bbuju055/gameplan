# Monitoring queries — {CLIENT NAME}

Owned by the account team. Every row traces to the client folder, the client's own terms, or something the user said; brief-run runs the active
rows every publication day. Categories appear in the brief in the order listed here.
Catch-all category: {CATEGORY NAME — uncategorized signal lands here}.

## {Category 1 — e.g. Competitive}

| # | Boolean terms (verbatim, quoted phrases and OR/AND as the feed expects) | Priority 1–5 | Sources |
|---|---|---|---|
| 1 | ("{Company Name}" OR "{Short Name}" OR ${TICKER}) | 5 | feed, radar, web |
| 2 | ("{competitor}" OR "{competitor asset}") | 4 | feed, radar |

## {Category 2 — e.g. Regulatory}

| # | Boolean terms | Priority 1–5 | Sources |
|---|---|---|---|
| 3 | ("{asset name}" OR "{generic name}") AND ("FDA" OR "approval" OR "CRL" OR "PDUFA") | 5 | feed, registry, web |

## {Category 3 — e.g. Capital markets}

| # | Boolean terms | Priority 1–5 | Sources |
|---|---|---|---|
| 4 | ("{Company Name}" OR ${TICKER}) AND ("offering" OR "financing" OR "earnings" OR "analyst") | 5 | feed, radar, web |

<!-- Sources vocabulary: feed (Newsdata), radar (scored mentions + alerts), registry
     (ClinicalTrials.gov), web (search backstop, priority 4–5 rows only).
     Owned-social rows (legacy Sprout imports) are noted here but not yet run: phase 2. -->

## Archived

<!-- Deleted rows move here with date and reason; never hard-delete — past briefs cite them. -->

## Proposed updates

<!-- brief-tune and close-of-run proposals land here, dated and evidenced, until the user says
     yes. A yes moves the row into its category above with a change-log entry. -->

## Change log

| Date | Who | Change |
|---|---|---|
| {DATE} | {NAME} | Initial setup{, imported from the agency's query workbook where noted} |
