---
name: brief-render
description: Render an approved daily brief into the standard Word deliverable, in the same format every time. Use as Stage 4 of brief-run after the brief's approval, or directly when the user says "make the Word file" for an already-approved brief. Formatting only. This skill adds no analysis, never alters approved content, and refuses to run on an unapproved draft. Cross-plugin requests route through core's suite-router.
---

# Brief Render (Formatter)

Every message, the notes while it works included, is in plain words, with nothing internal named and nothing said about what was read or checked (the core plugin's `rules/voice.md`). A note while it works is one plain line, or nothing: what is being done or what comes next, in plain words, is fine; it never names anything internal and never gives a count or a result.

Produce the file the account team actually emails. Identical structure every brief, so clients
learn to read it and account leads learn to review it fast.

## Gate check (before anything renders)

An approval record must exist for this brief: approver name and date-time, all ⚠ tags either
substantiated or accepted (from the brief's approval, recorded in `decisions.md`). No
record, or no saved draft (`briefs/<YYYY-MM-DD>/draft.md`) → refuse plainly and route back to the review gate. There is no draft-watermarked
Word output; the Word file exists only after approval, which is what makes its existence
meaningful.

## Template resolution

Deliverable type **daily-brief**, template `daily-brief.md` (a structure spec, not a
binary). Resolution order: the gameplan root's `templates/`, then the working directory's
`templates/`, then this plugin's `templates/` (shipped default). If a `.docx` template is later
registered alongside the spec, prefer it and read its same-name mapping spec first; it is filled
with `gameplan-render fill` instead of built.

Load the suite's org config (the core plugin's `org-config` skill) before building: `org.name`
fills the footer and `brand.*` supplies the fonts and colors the spec names.

## The format (from the shipped spec — summary here, spec is authoritative)

- Title block: client name, "Daily Media Brief", coverage window, prepared date.
- Category sections in the draft's order; within each, per story: hyperlinked headline;
  summary paragraph; source and date line in italics; the Signal line prefixed **Signal:** in
  the brand accent color.
- Method note (last section, small type): sources run, gaps named, story counts, "prepared with
  AI assistance, reviewed and approved by <name>". The gaps survive formatting — a silent gap
  is the failure this line exists to prevent.
- Footer every page: the agency's saved confidential footer from the org config; no footer while
  none is saved (never say a footer is missing: there is simply none).
- Fonts and colors per the spec, from the org config's brand section (heading and body fonts,
  primary and accent colors; shipped defaults Georgia, Arial, 0F2F2C, 8A6420). Build the docx with
  the core plugin's `gameplan-render build --type daily-brief` (an alert addendum:
  `--type alert-brief`), passing this brief's `decisions.md` with `--decisions` and its saved draft with `--draft`. Never install
  anything to make the file; if the command is missing or fails, say so and stop. Load the core
  plugin's `office-files` skill first, without announcing it: it gives the command's path, the full rule and the content
  shape.

## Non-negotiables (verified before handing the file over)

- [ ] Every approved story present; no story not in the approved draft present. Diff against
      `decisions.md` dispositions, not against memory.
- [ ] Every headline, summary, Signal line and the sources line is the saved draft's, word for
      word (the build stops otherwise). A wording problem goes back to the review; it is never
      settled in the content file.
- [ ] Every hyperlink is its story's URL in the saved draft (the build stops otherwise). Links
      are listed in the result, not opened: never say they were checked to work.
- [ ] Which claims were accepted is not in the Word file (the client-folder contract's claims
      rule): the acceptance stays in the decisions log and the claims ledger, where it is
      never cleaned up.
- [ ] The method note's gaps are the draft's gap sentences word for word (the content file's
      `gaps` is an empty list when the draft says "none"), and nothing from the decisions log's
      Source record is in the file.
- [ ] Each Signal line is the draft's `signal` sentence alone: no ⚠, no tag from the story's
      flags, nothing from its reviewer note.
- [ ] Residue check: no other client's name anywhere in the file, including metadata.
- [ ] File named `<Client> - Daily brief - <D Mon YYYY>.docx` (alert addenda:
      `<Client> - Alert brief - <D Mon YYYY> <HHMM>.docx`), saved in
      `Deliverables/<Client>/Daily briefs/` (the core plugin's client-folder contract). brief-run names it to
      the user, once; this skill says nothing about it.

If any check fails, fix the document before delivery — never deliver with a caveat in place of
a fix.

## Scope discipline

Formatting reveals problems; it never fixes them. A missing Signal line, a category out of
order, contradictory dates — bounce to the review gate. This skill changes presentation, not
substance, and the decisions log is the only authority on what the substance is.
