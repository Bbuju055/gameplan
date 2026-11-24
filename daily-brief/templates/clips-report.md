# Template spec: clips-report (deliverable type: coverage report)

The structure spec for the Word coverage report clips-run builds after approval. A neutral
default: no agency's format is copied. If a `.docx` template is registered in the gameplan root's
`templates/`, it takes precedence with its own same-name mapping spec; an agency's house format
arrives that way.

## Brand (from the org config)

`{org_name}` is `org.name`; the client's name and the opening sentences use `brand.fonts.heading`,
section titles and body text `brand.fonts.body`, both in `brand.colors.primary` where they are
colored; rules use `brand.colors.accent`. Tone takes the suite's fixed status colors (green for
positive, red for negative), the same under every brand. Nothing here names a brand color or font.

## Page setup

- Letter, portrait, 1" margins.
- Footer, every page, centered, 8pt, gray: `org.confidential_footer`, omitted while unset, then
  the page number.

The report goes to the client as it is: it carries the coverage and what it adds up to, and
nothing about how the run was made. Sources, gaps, the approval, clips dropped at review, and what
the report does not measure are said to the reviewer at the review, never printed in the document.
Each clip's detail is kept in the companion spreadsheet; the run's sources, gaps and dropped clips
are not saved anywhere after the review.

## Cover block (top of page one)

- The client or keywords, large; "Coverage report · {start} to {end}"; the date.
- Then the summary, three short sentences built from the approved counts, the figures in bold:
  the clips and how many came from the agency's outreach; which outlet type carried the most (and
  the month coverage peaked, when the period spans months); the tone split and the most carried
  message. A count of zero reads "none", types that tie are named together ("Trade and national
  outlets each carried 2 of 5"), a single clip reads in the singular, and a message no clip
  carried is left out. A period with no clips gets no report.

## Section 1 — At a glance

Sections, each titled with a full sentence stating what its chart shows, worked out from the
approved counts (the renderer adds no analysis), under a light rule. No labels, numbers, or
badges above them. In each bar chart the bar the title is about
is the brand color at full strength and every other bar is the same color made pale: a chart has
one color.

- **Outlets:** clips by outlet type (national, trade, regional/local, online, wire).
- **Timing:** clips by month, when the period spans more than one.
- **Tone:** one bar split into positive, neutral, mixed, and negative, with the counts.
- **Outreach:** agency-driven versus organic.
- **Messages:** the approved claims carried most often, each with its count, in the claim's
  approved wording. None carried is said in the title. Keyword reports leave this section out.

## Section 2 — The coverage

One table, newest first; one table per month when the period spans more than one. One row per
clip: outlet, the article (its headline, linked), the date it was published, and the reporter. A
clip from the agency's monitoring export that could not be opened to confirm it carries a marker,
explained under the table ("Not independently confirmed").

Each clip's matched passage, messages carried, agency-driven or organic, tone, and syndicated
pickups are judged at review and feed the totals in Section 1; they are listed per clip in the
companion spreadsheet, not in the report.

## Companion spreadsheet (offered beside the report)

`{Client name} - Coverage report - {period}.csv`, saved beside the report, a header row, then one row per clip: date, headline, link,
outlet, outlet type, reporter, matched passage, messages carried, agency-driven or organic, tone,
also ran in, source (feed, web, export).
