---
name: pulse-render
description: 'Render an approved Narrative Pulse run into the report ("What Claude says about [client]", or "What AI engines say" when more than Claude was measured), a page with the five dimensions, the findings that matter, the next run date, an evidence appendix, and the two hand-off blocks (cited outlets for media-targeting, names for competitor-discovery). Use as Stage 4 of pulse-run after the one approval, or for "format the pulse for the client". Formatting only: no new analysis, never renders without that approval, and needs no second one. Cross-plugin requests route through core''s suite-router.'
---

# Pulse Render

Every message, the notes while it works included, is in plain words, with nothing internal named and nothing said about what was read or checked (the core plugin's `rules/voice.md`). A note while it works is one plain line, or nothing: what is being done or what comes next, in plain words, is fine; it never names anything internal and never gives a count or a result.

One deliverable, the client's eyes. Every number traces to `scores.md`, every quoted sentence to
`answers.jsonl`, and the review's decisions are respected exactly.

## Preconditions (verified, not assumed)

- `runs/<date>/review.md` exists with an approver name and date-time, or pulse-run asked for the
  copy for approval (below). Otherwise, no review, no render: the
  reply is this one sentence and nothing else: "This run hasn't been reviewed yet, so the report
  can't be rendered; the review comes first." Do not describe the folders, the run, or this
  check, and do not describe, draft, or preview the report; the description is the render.
- Struck questions in the review are excluded everywhere, including counts.

## The file

`Deliverables/<Client>/<Client> - <What Claude says | What AI engines say> - <D Mon YYYY>.html` at
the gameplan root (the client-folder contract's naming), with ` - 2` when the run folder has its
`-2` suffix, so a second run that day never overwrites the first report; always filled from
`templates/pulse-report.html`, never copied from an earlier report (read `templates/pulse-report.md`
first for the slot rules). Load the
suite's org config (the core plugin's `org-config` skill) for `{{ORG_NAME}}` and the brand tokens.
`data-doc-state="approved"`, the band naming the reviewer and the review date: the review's
approval is the report's, and nothing approves it again. **The copy for approval**, which pulse-run asks for before the review,
is the same page under the same name with `data-doc-state="for-approval"`, the band's words replaced by "For approval · not yet approved" and the
"Reviewed by" words left out; on approval the page is written again as approved, over it, with `data-doc-state="approved"`. The band's words and the page's state always agree: a page whose band says "Approved" is in the approved state, and the last check before the file is named is that the two match. The name is "What Claude says" when
Claude was the only engine measured (always the case in the Claude app), "What AI engines say"
when ChatGPT or Perplexity was measured too, in the file name, the page title, and the masthead. Baseline runs also write
`narrative/baseline.md`: the roll-ups and per-question table in plain markdown, once, never
overwritten.

## Page one

- Masthead: client, run date, run type (baseline / standing), engines measured and not measured
  (an engine whose answers were pasted reads "ChatGPT, answers collected by hand", with the
  conditions line saying they were asked on the agency's own account, once, and an engine first
  measured after the baseline says this run is its starting point),
  the reviewer's name and the review date-time. The reviewer
  line is in the masthead, not only in the footer.
- Five dimension cards: presence, accuracy, framing, share of voice, citations. Each card carries
  one value in words or a count with its denominator ("named in 2 of 5 class answers", "2 facts
  out of date and 1 wrong; everything else checked was correct", "own positioning in 1 of 7 answers, 5 just 'an oral
  GLP-1'", "4 of 17 mentions", "7 of 12 citations from editorial outlets") and one line of
  meaning. **Never a score out of 100, a grade, a percentage, or an
  overall number for the run.** If you find yourself writing
  "65 / 100", stop: that is the composite this report refuses to have. Counts are per engine and
  never added across engines: with several engines, the value gives each engine one short line with
  its own count ("ChatGPT: 1 fact out of date and 1 wrong"), never a table: in the template that is
  one row for each engine, in the markup the template's comment shows (the engine's label, its line
  with the count in bold, and a bar only where the line is one count out of a total), and
  the card still has one line of meaning, which never states a count the appendix table doesn't show. The accuracy card counts what was
  wrong, out of date or unapproved, and never gives a number of correct statements or of statements
  checked: that total does not repeat between scorings. With nothing to count it says so in words
  ("Nothing wrong, out of date or unapproved"). There are no trend arrows: runs are not
  compared yet, so the card says "baseline" or "no comparison yet". No composite.
- Three findings that matter, in answer-score's rank order and no other: **1 wrong, 2 unapproved
  claim repeated, 3 stale, 4 absent, 5 names, 6 outlets, 7 flags.** Take the top three that exist.
  Each carries the engine's quoted sentence, its words exact but without markdown marks such as
  `**`, and the folder line in plain words.
- Fix at the source: at most three items, each one or two sentences with no sub-items, drawn from answer-score's sources for findings the
  reviewer accepted, own pages first, then other sites, then what may correct itself; left out when
  there are none. Every accepted finding counts, including one an engine made in only one of its
  passes, which says so ("in one of two passes"). Own page: "Update your pipeline page: Claude cited it when it repeated
  'best-in-class safety profile'." Unless the page was read this run, say "if it still says…".
  Someone else's page: ask that outlet for a correction when the page was wrong when published, or
  get fresh coverage that replaces it when it was right at the time; when it was not checked, say
  both: "Read the Fierce Biotech article first. If it is wrong, ask for a correction; if it was
  right when published, new coverage replaces it." Never offer to edit another
  site. A flagged site is never asked for anything; say it was flagged. Your own pages that need the same
  change share one item; every other page gets an item of its own. With more than three, a flagged site's note is the first left out: it is the only one that
  asks for nothing. May correct itself: "This
  was announced recently; check again next run." Pages go by plain names ("your pipeline page", "a
  Fierce Biotech article"), never a web address.
- Next run: the first day of the next FIRM or GUIDED event on the client's calendar minus
  `pulse_lead_days`, otherwise `pulse_standing_days` after this run (both from the org config's
  `next_actions`; never a date before today), with the event named in plain words. An event whose window has
  already opened is not ahead: the next run is counted from the next one that starts after today.

## Appendix

- Per-question table: question, family, per engine: presence, accuracy verdicts, framing label.
  Only answers that exist get a row; an engine or question not measured is one line in the
  conditions, not a row per question.
- Per-engine notes: two sentences each and no more, each naming one thing: the first, one thing
  the engine got right; the second, the highest-ranked finding against it. The table above carries
  the rest. Both are drawn only from the findings. An engine with nothing on one side still gets
  that sentence, and it says so: "Nothing ChatGPT said about the company was confirmed as correct."
  or "Nothing wrong, out of date or unapproved."
- Raw excerpts behind each page-one finding, quoted, with engine and pass.
- The engines ledger and conditions, each engine by its report label only (`templates/engines.md`),
  and in these words for Claude: "Asked on the agency's own account by a fresh helper told to use
  web search only. Account settings may still shape the answers; how much has not been measured." Never say what a setting did or did not
  change, and never "no other instructions". With `account_context` client visible, add: "Claude's account already knows this client,
  so its being named is not independent evidence."
- Not measured: Gemini and Google AI Overviews, by decision, in one line.
- Gaps: folder gaps that blocked verdicts.

## What travels onward (client appendix, plain English)

Two short tables in the appendix, in the client's language, no internal vocabulary:

- **Outlets the engines cite** — outlet, how many engines cited it, editorial or company-issued,
  tier in plain words ("original trade reporting", "company release"). With one engine measured,
  the outlets it cited across two or more questions, said as one engine's citations. The same
  outlets the review showed, with the same counts. The client's own site and
  any source flagged this run each get their own row whose standing column says, in those words,
  "not an outlet to pursue" and why. This sentence is not optional and does not live in a footnote.
- **Companies the engines name that we do not track** — company, which engines, in which questions.

## Hand-off blocks (internal only: `runs/<date>/handoffs.md`, never in the client file)

The rules every block follows (empty fields, when it is written, who reads it) are the core plugin's `rules/hand-offs.md`.

```
### HAND-OFF: cited-outlets            → media-targeting (ai-cited-outlets.md proposals)
- outlet | domain | engines citing | questions where cited | tier | proposed action (add / keep / drop)

### HAND-OFF: names                    → competitor-discovery (re-screen candidates)
- entity | named by which engines | in which questions | in tiered set? (yes / no / borderline)
```

Both are proposals; write the blocks even when empty (`- none this run`). Every cited-outlets row
ends with exactly one of `add`, `keep`, or `drop`; "already listed" is `keep`, not a note. media-targeting's config
is not written from here: media-targeting reads these proposals the next time it builds a list for
this client; the competitor set changes through a landscape run, not here. The words
"HAND-OFF", "media-targeting", "competitor-discovery" and any file name stay in `handoffs.md`; the
client file carries only the two plain tables above.

## Voice

Plain business English throughout; the core plugin's `rules/voice.md` is the rule. Say "the engines",
"the question set", "the client folder", "the approved claims list", "the review". Never "claims
ledger", "jsonl", "script", "hand-off",
"pipeline file", "org config", "gameplan root", "run folder", or an error code. Co-occurrence, not causation: "in the same window as" never "because of".

## Non-negotiables (checked before handing the file over)

- [ ] Approver name and date-time present in the report footer.
- [ ] The name matches the engines actually measured.
- [ ] Every page-one number appears in `scores.md` and agrees with the appendix table; every quoted
      sentence appears in `answers.jsonl`.
- [ ] No composite score anywhere.
- [ ] Both HAND-OFF blocks present in `handoffs.md`; neither appears in the client file.
- [ ] Findings on page one follow the rank order exactly: wrong, unapproved claim repeated, stale,
      absent, names, outlets, flags.
- [ ] No other client's name anywhere in the file or its metadata: checked by the core plugin's
  `gameplan-render check <the page> --root <gameplan root> --client <slug>` (its office-files
  skill), with anything it reports fixed before the page is named.
- [ ] No model string or version (gpt-5, sonar) anywhere in the client file; the models stay in `answers.jsonl`. The engines go by their names: Claude, ChatGPT, Perplexity.
- [ ] Fix at the source uses only accepted findings and never offers to edit another site.
- [ ] Struck questions absent from every table and count.
