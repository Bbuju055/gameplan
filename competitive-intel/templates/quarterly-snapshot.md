# Template spec: quarterly-snapshot (deliverable type: quarterly-snapshot)

The structure spec for the one-page quarterly activities snapshot that client-deliverable builds
as a Word document. A neutral default: no agency's format is copied, and no line is fixed text
apart from the headings; every entry comes from the client's calendar and activity log. If a
`.docx` or `.pptx` template named `quarterly-snapshot` is registered in the gameplan root's
`templates/`, it takes precedence with its own same-name mapping spec; an agency's house format
arrives that way.

## Brand (from the org config)

`{org_name}` is `org.name`; headings use `brand.colors.primary` and `brand.fonts.heading`, body
text `brand.fonts.body`, highlights `brand.colors.accent`. Nothing here names a color or font.

## Page setup

- Letter, portrait, 1" margins, one page.
- Footer, centered, 8pt, gray: `org.confidential_footer`, omitted while unset.

## Title block

- Top line: the agency's name (left out while unset) and "Activities snapshot"; at the right margin
  the DRAFT FOR REVIEW mark until approval.
- Title: the client's name, then "{quarter} activities snapshot" under it (quarter as "Q4 2026").
- Prepared date. Once approved, the DRAFT FOR REVIEW mark goes and a line under the date reads
  "Reviewed and approved by {name}, {date} · v{N}".
- The three sections below are rows: the section's name on the left, its lines on the right.

## Section 1 — Milestones this quarter

Calendar rows whose window falls in or overlaps the quarter, from `## Upcoming` and `## Past`, in
two short lists:

- **{client}:** rows whose entity is the client.
- **The field:** every other row, with its INHERITED-RISK tag where the calendar carries one.

One line each: event, window (grade). A past row adds its outcome in a few words; a
LAPSED-GUIDED row says the window passed without news. None: "No dated milestones this quarter."

## Section 2 — What we did

The quarter's activity-log rows, grouped by type in this order, each group headed with its
count: placements, pitches, statements, owned content, spokesperson, deliverables. One line
each: date — what — audience, with "for {event}" when `serves` names a calendar row. A placement
that answers a logged pitch says so ("from the {date} pitch"); a correction row replaces the row
it corrects. Groups with no rows are left out and named together in one closing line ("No
statements or spokesperson engagements this quarter").

Before building, ask once whether anything went out this quarter that the log does not hold;
what the user names is logged first (`entered-by`, per the contract), then shown. Nothing logged
and nothing named: "No activity recorded this quarter." Never invented.

## Section 3 — Coming next quarter

Calendar rows that start after this quarter and overlap the next one, one line each: event,
window (grade). Then every agency deadline due next quarter, whichever event it serves (a row
already shown in Section 1 included): what · by when · for {event}. Owners stay in the calendar,
not on the page. None: "Nothing dated next quarter yet."

## Rules (client-deliverable's non-negotiables apply, including the residue check)

- Confidence grades survive: an ESTIMATED window is never rendered as a bare date; "Jun–Oct
  (est.)" fits.
- Inherited-risk field events keep their tag; that tag is why the client sees the event at all.
- A recap surface, not an analysis document: anything needing a caveat deeper than a
  parenthetical belongs in the accompanying report, and the line gets the short form.
- Nothing from `runs.md` appears here.
- Last line, 8pt: "Drawn from the client's calendar and activity log as of {prepared date}."
