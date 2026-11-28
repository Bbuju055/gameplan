# Pulse report — template spec (read before filling `pulse-report.html`)

One self-contained HTML file per run, in the client's `<Client>/` folder (its `Drafts/` for the copy for approval), named
`<Client> - <What Claude says | What AI engines say> - <D Mon YYYY>.html` (with ` - v2` when a second run is made the same day). It is in the suite's one look and fetches nothing: Georgia for the client's
name, the figures and quoted words, Arial for text, Verdana for small labels, all three on every
Windows and Mac.

## States

| State | Banner | Set by |
|---|---|---|
| `approved` (shipped default) | A filled green mark, "Approved · {{APPROVED_BY}} · {{APPROVED_DATE}}", under the client's name | pulse-render, once the review is approved: the review's approval is the report's approval |
| `for-approval` | The same mark in amber, its words replaced by "For approval · not yet approved", and the "Reviewed by" words beside it left out | pulse-render, for the copy the reviewer opens before approving; approval writes the page again as `approved` |

## Slots

Masthead: `{{REPORT_NAME}}` ("What Claude says about <client>" when Claude was the only engine
measured, otherwise "What AI engines say about <client>"), `{{CLIENT}}`, `{{RUN_DATE}}`,
`{{RUN_TYPE}}` (Baseline / Standing), `{{ENGINES_MEASURED}}`, `{{ENGINES_NOT_MEASURED}}`,
`{{REVIEWER}}`, `{{REVIEW_DATETIME}}`, and in the band `{{APPROVED_BY}}` and `{{APPROVED_DATE}}`
(the reviewer and the review date). Footer: `{{ORG_NAME}}` from the org config's
`org.name`, which also opens the top line; `brand.colors.primary` and `brand.colors.accent` override
`--primary` and `--accent` in `:root` when set. The status colors (`--good`, `--warn`, `--bad`) are
the same under every brand and are never overridden.

Dimension cards (five, fixed order): `{{PRESENCE_VALUE}}`, `{{PRESENCE_LINE}}`, then ACCURACY,
FRAMING, VOICE (share of voice), CITATIONS. Value is one row for each engine measured, in the markup
the template's comment shows: the engine's report label, its line in words or as a short count
("named in 2 of 5") with the count itself in bold, and, only where the line is one count out of a
total, the bar, whose two numbers are that count and that total. Never a percentage, and nothing
added across engines; with one engine measured, one row and no label. Line is one sentence of
meaning. With two or more engines the page itself adds a button for each engine, which dims the
other engines' rows; nothing is filled in for that. ACCURACY's value counts what was wrong, out of
date or unapproved, never the correct statements or a total checked. `{{*_TREND}}` is "baseline" or "no
comparison yet": runs are not compared yet.

Findings: exactly three `<article class="finding">` blocks, in rank order (wrong, unapproved claim repeated, stale, absent, names, outlets, flags): `{{F_KIND}}` (Wrong / Unapproved claim repeated / Out of date / Absent / Name / Outlet / Flag), `{{F_QUOTE}}` (the engine's sentence, verbatim),
`{{F_ENGINE}}`, `{{F_CHECK}}` (the client-folder line, in plain words), `{{F_MEANING}}` (one sentence).
Fewer than three findings: fill the remaining blocks with "No further finding at this level" and say
so honestly rather than promoting a minor item.

Fix at the source: `{{FIX_ROWS}}`, one `<li>` per line, at most three, per pulse-render's rules;
remove the whole section when there are none.

Next run: `{{NEXT_RUN_DATE}}`, `{{NEXT_RUN_REASON}}` ("seven days before <event>" or "monthly", with the org config's `pulse_lead_days` and `pulse_standing_days`).

Appendix: per-question table rows (`{{ROWS}}`, only answers that exist), per-engine notes (`{{ENGINE_NOTES}}`), raw excerpts
(`{{EXCERPTS}}`), ledger and conditions (`{{LEDGER}}`), not measured line (fixed text), gaps
(`{{GAPS}}`), and two plain tables: outlets the engines cite (`{{OUTLET_ROWS}}`: outlet, engines citing, kind, standing in
plain words) and companies the engines name that we do not track (`{{NAME_ROWS}}`). The HAND-OFF blocks themselves live in
`runs/<date>/handoffs.md` and never in this file.

## Rules

- Every number on page one appears in scores.md; every quote in answers.jsonl.
- No composite score and no percentages: counts with their denominators in words.
- Co-occurrence, not causation.
- No other client's name anywhere in the file or its metadata.
- There are two states, `approved` and `for-approval`, and one band, `.band`, whose words are the state's; the file never carries the words of the state it is not in, and no other banner.
