# Coverage report — template spec

Produced by track-outcomes after outcomes are confirmed and recorded.
Client-facing: plain, proud, and precise. Built as a Word file by the core plugin's
`gameplan-render` on every run; a CSV of the placements is written beside it as well.

## Structure

The document goes to the client as it is: nothing about how the outcomes were
found or confirmed appears in it; that stays in the run record.

1. **Header** — client, campaign (release title), pitch date, report date,
   `org.confidential_footer` from config.
2. **The numbers that matter first** — a short summary in sentences, figures in
   bold: placements won from how many targeted reporters, the placement rate and
   segments; which segment won the most; how many reporters are not yet resolved. No rate is
   given when nothing was won ("won no placements from 12 targeted reporters"); segments that
   tie are named together; and the not-yet-resolved line is left out when every reporter is
   resolved.
3. **Placements** — a section titled with which segment won the most,
   its bars by segment, then one row each: outlet, headline (linked), date,
   reporter, segment. Unlinkable hits (radio, podcast) carry the operator's
   note instead of a link; a hit whose link was not found carries
   "link not found".
4. **By segment** — targeted / covered / no coverage / not yet resolved, per
   segment (from the archive's `performance --by segment`). Never report a hit rate over
   unresolved entries. Targeted means pitched: a reporter recorded as not
   pitched is in none of the document's counts.
5. **Discovery performance** — when any placement came from a discovered or
   reactive reporter, one line naming it: discovery earning its keep is a
   story the agency should get to tell.
6. **(Optional) AI-answer visibility** — when checked: whether won coverage
   surfaces in AI-engine answers about the client, with the query themes used.
7. **How the outcomes were found** ("placements found by search and confirmed
   by the team; broadcast mentions added manually") is said to the operator at
   the hand-over and kept in the run record, not printed in the document.

## Tone rules

- No adjectives the data doesn't earn. "Strongest segment: fintech & lending
  (4 of 12)" — not "incredible results."
- Reporters who didn't cover are counted, never named in the client report.
