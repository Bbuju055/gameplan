# Template spec: daily-brief (deliverable type: daily-brief)

The structure spec for the daily Word deliverable. brief-render reads this before building the
docx. If a `.docx` binary template is registered later in the gameplan root's `templates/`, it
takes precedence and ships with its own same-name mapping spec; until then this spec IS the
format, built element by element.

This is the suite's default. An agency whose clients already receive a daily brief registers that
format as its `.docx` template, so its clients see no change.

## Brand (from the org config)

Every brand value below comes from the suite's org config, never from this file: `{org_name}` is
`org.name`; "primary" is `brand.colors.primary` and "accent" is `brand.colors.accent` (hex, shipped
defaults 0F2F2C and 8A6420); the heading font is `brand.fonts.heading` (shipped default Georgia) and
"Arial" is `brand.fonts.body` (shipped default). Small labels are Verdana capitals in every brand. An
accent too pale to read on white still draws rules; its labels take the primary. An agency that
fills the brand section changes the look without touching this spec.

## Page setup

- Letter, portrait, 1" margins.
- Footer, every page, centered, 8pt Arial gray: `org.confidential_footer`, omitted while unset,
  as on every other deliverable.

## Title block

| Element | Spec |
|---|---|
| Top line | small labels over a light rule: `{org_name}` (primary, bold; left out while unset) · "Daily Media Brief" (gray), and the prepared date at the right margin |
| Client name | heading font 26pt, primary |
| Coverage window + prepared date | Arial 9pt, gray — `Coverage: {window_start} to {window_end} · Prepared {prepared_date}` |

## Category sections (draft order, repeated per category)

- Category heading: a small bold label in the accent, under a thin accent rule.
- Per story, in draft order:
  1. **Headline** — Arial 11.5pt bold, primary, hyperlinked to the canonical URL, with a light underline.
  2. **Summary** — Arial 10pt, the approved summary verbatim.
  3. **Source line** — Arial 8.5pt gray: `{source_name} · {date}` (cluster note appended
     when cluster size > 1: `· also carried by {n} other outlets`).
  4. **Signal line** — a thick accent rule down its left side, so the eye can go from Signal to
     Signal: the word `Signal:` as a small bold label in the accent; the approved line follows in
     Arial 10pt, body color. Accepted-⚠ stories render clean here; their acceptance stays in
     the decisions log, never in the Word file. A story's flags and reviewer note are never rendered.

## Method note (final section)

Heading "About this brief", a small bold gray label under a light rule. Arial 9pt body:
- Sources run: the approved draft's sources line, word for word.
- Then the coverage gaps: the approved draft's gap sentences, word for word, one per
  missing source (signal-gather's "A gap in the brief" lists them). No gap line when nothing was
  missing. Why a source was missing never appears here.
- Story counts: {included} included of {candidates} candidates reviewed.
- `Prepared with AI assistance. Reviewed and approved by {approver_name}, {approved_datetime}.`

## Filled-example checks (render verifies against decisions.md)

- Story set = approved dispositions exactly; order = draft order.
- No placeholder braces survive in the output.
- No text anywhere in the file (including metadata) referencing another client.
