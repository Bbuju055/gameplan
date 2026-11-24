# Parsing rules for the media log

The agency-specific rules `reporter-list` applies when normalizing log rows. It
learns them when the parse-coverage line reports drift ("read 412, used 407,
skipped 5") and the operator explains the skipped rows. Fixing drift is an edit to
the agency's copy — never a skill rewrite.

**This is the shape only: the values below are illustrative examples, not rules.
The agency's rules live at `<gameplan root>/media/parsing-rules.md`, because a
plugin's own folder can't be written once uploaded.** Until that file exists,
`reporter-list` parses conservatively and reports its coverage every run.

## Beat label synonyms

Map the log's beat vocabulary to canonical beats. One canonical beat per line;
synonyms are what actually appears in the log.

| Canonical beat | Log synonyms (examples — replace) |
|---|---|
| fintech | "fin-tech", "financial technology", "payments/fintech" |
| healthcare | "health", "med", "healthcare & pharma" |

## Delimiter tolerance

How multi-value cells are split (examples — replace with the log's reality):

- Beats: split on `,` `;` `/`
- Geography: split on `,` `;`

## Skip rules

Rows dropped as unusable, always counted in the parse-coverage line:

- Missing reporter name → skip (always: reporter-list skips such a row whatever is listed here)
- Header repeats / section-divider rows (e.g. all-caps single-cell rows) → skip
- (add patterns observed in the real log)

## Known quirks

Free-text notes on the log's habits (examples — replace):

- (e.g. "Tier column uses 1/2/3 for print but A/B/C for broadcast")
- (e.g. "Freelancers have outlet 'Freelance — see notes'")
