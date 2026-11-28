---
name: client-deliverable
description: Render a finished analysis (the competitive landscape, a quarterly snapshot) into the standard client deliverable, a Word file in the same format every time, on the firm's template, then take its approval, one per version. Use as the final stage of a landscape run, or directly when the user says "format this for the client", "make the deliverable", "put this in our template". Formatting only. This skill adds no analysis and never alters verified content. Cross-plugin requests route through core's suite-router.
---

# Client Deliverable (Formatter)

Every message, the notes while it works included, is in plain words, with nothing internal named and nothing said about what was read or checked (the core plugin's `rules/voice.md`). A note while it works is one plain line, or nothing: what is being done or what comes next, in plain words, is fine; it never names anything internal and never gives a count or a result.

Take verified content and produce the document that actually goes to the account team and the
client: identical structure every time, so clients learn to read it and reviewers learn to
review it fast.

## Template registry and resolution

Deliverables are typed; each type has a named template. Resolution order for a template file:
the memory folder's `templates/` (the core plugin's client-folder contract says where memory is), then the plugin's own `templates/` directory (shipped defaults). Finished deliverables are
saved where the contract says: in the client's own folder, `<Client name>/`, its `Drafts/` for the copy shown for approval and the folder itself for the approved copy, named
`<Client name> - <What it is> - <D Mon YYYY>.docx`, the folder made if it is missing. Each
`.pptx`/`.docx` template ships with a same-name `.md` mapping spec; read it before populating. A
type whose shipped default is a layout in the core plugin's `gameplan-render` is built with
`gameplan-render build`; an agency's `.pptx` or `.docx` of the same name in the memory folder's `templates/` takes its place and is filled with `gameplan-render fill`. Never install anything to make a file;
if the command is missing or fails, say so and stop. Load the core plugin's `office-files` skill
first, without announcing it: it gives the command's path, the full rule and the content shapes.

Org name, confidential footer, brand colors, fonts, and logo come from the suite's org config (the core
plugin's `org-config` skill), loaded before any template is filled. A shipped template never
carries an agency's own mark; where the logo would go, an unset `brand.logo` renders the org
name as text.

| Type | Template | Use for |
|---|---|---|
| **landscape-report** | `gameplan-render`'s landscape-report layout (shipped) | The competitive landscape: page one in bullets (where the client stands, the dates that matter, the biggest risk and opportunity, what to do by when), then the evidence. Named `<Client> - Competitive landscape - <date>.docx` |
| **quarterly-snapshot** | `quarterly-snapshot.md` (shipped spec, rendered as Word) | Quarterly activities one-pager: the quarter's milestones from the client's calendar (client and field events, grades and inherited-risk tags carried), what the agency did from the activity log, and what is dated next quarter; no fixed text. An agency's own snapshot registered under this name replaces it. Made when asked, or when the suite router suggests it at quarter end. Named `<Client> - Activities snapshot - <quarter>.docx` |

Every person-facing deliverable is a Word file (or the agency's own registered format); none is
Markdown. Pick the type from what the user asked for: "the deliverable" or "the document" for a client with a finished landscape is the landscape, and the quarterly snapshot is made only when it is named (or offered, in one line). Ask only when nothing points to either. Client logos come from
the client's folder or brand assets; the shipped template carries a placeholder block, never
another client's mark.

**A snapshot reads the calendar as it stands today.** Before the snapshot reads a date, bring the calendar up to date as the contract's lapse rule says, and write it: a GUIDED window that ended without news is LAPSED-GUIDED in the calendar, and the snapshot says the window passed without news.

**Some templates need input the analysis cannot produce.** The quarterly snapshot's activity
section comes from the client's activity log for the quarter; ask once whether anything went out
that the log does not hold, log what the user names per the contract (`entered-by`), and if
there is still nothing, the section says so in one line, never invented content. A user who has
already said nothing went out unlogged has answered: do not ask again, build from the log. If the
runs record shows something sent that the log does not hold, build anyway, leave it out, and say
so in one line after the draft; it is never a reason to stop before building.

## Non-negotiables (verified before handing the file over)

- [ ] The copy shown for approval reads "Draft for review" on page one; the approved copy names
      the approver and date instead.
- [ ] **Every ⚠needs-support tag survives** formatting, visibly, next to its claim, in the copy for approval and in
      the approved copy alike: an accepted claim keeps its mark, and what the acceptance stops is
      the question (the client-folder contract). Formatting that silently drops
      a tag converts a known risk into a hidden one.
- [ ] Every forward date keeps its confidence grade; ESTIMATED/SPECULATIVE stay windows.
- [ ] The sources and gaps and the method sections are included: they are part of the product's
      credibility, never trimmed for polish.
- [ ] **Residue check:** `gameplan-render` checks ALL text in the produced file, including
      merged or hidden table cells, speaker notes, and metadata, for content belonging to any
      other client or to the template's source engagement.
- [ ] Named and saved as the contract says, and said in the reply as the contract's "Saved:" line says it (the file's name, then "in <Client>, Drafts" for a copy for approval or "in <Client>" for an approved one), never as a path.
- [ ] A `deliverable` row (or the calling run's own row, such as `landscape`) appended to the
      client's `runs.md`: what it is in plain words, `draft`, its path.

If any check fails, fix the document before delivery; never deliver with a caveat in place of a
fix (landscape-report's assembly rule applies here too). The checks are run, not recited: say nothing about
a check that passed (the core plugin's voice rule), and never which markers or residue a check looked for.

## Approval and revision

**Who approves: the person running it**, as the approver (the client-folder contract's Who approves). No role gate: the firm's control is the trace and the
versions, not a title. One person approves a copy; nothing asks for a second sign-off on it. A
new version is a new copy and is approved again. Approving a later version does everything approving the first would have: the folder updates the run brought are applied then, if no approval has applied them yet.

**Approving.** When the user approves ("approved", "looks good"):
1. **Claims in the same breath.** The message that asks for approval names any claim the
   document relies on that is not yet approved, so one answer accepts them too. It is one
   yes-or-no question ("Approve, accepting <the claim, in plain words> as it stands?"), never a
   choice between options: a yes approves and accepts. Each acceptance
   is written back to the claims ledger (`accepted by <name>, <date>`) and never asked about
   again. A user who declines a claim gets it cut or qualified, then the approval question again. A copy approved in a later conversation is asked about there, with its open claims named again: a question asked in an earlier conversation does not count.
2. **The approved copy.** Build it again with the approval in it, saved under the same name in the client's folder itself; the copy shown for approval stays untouched in `Drafts/`.
3. **Close the loop.** Record the approval in the method section, append an `approved` row to
   `runs.md` naming the file, and apply the run's folder updates in the same act (the contract's
   Proposed updates).
4. **Sent.** Approval is not sending, and nothing is said or asked about sending. When the user says the document went to the client (now or
   later), append a `deliverable` row to the activity log per the contract, naming the file and who
   received it, and a `sent` row to `runs.md`. Nothing asks again.

**Revision notes.** Classify every note before acting:
- **Presentation** (rewording, reordering, cutting, tone): apply directly, save a new copy for
  approval (` - v2`), still marked draft for review, and ask for approval again. Fast loop.
- **Substance** (add or remove a company, disagree with a date or grade, change a scenario):
  never hand-edited into the document. Route it back through the owning stage (a new company goes
  through the research and the conflict check; a date through the timeline's grading rules; a
  branch through scenario-planning), then reassemble. The document's credibility is that nothing
  in it is unverified, including edits.
- **Both kinds in one round:** neither waits for the other. The presentation note becomes the next
  copy now, with its own approval asked; the substance note's result is the version after that,
  with its own approval. Never one merged version for one approval.

Every version carries a one-line note of what changed since the previous one.

## Scope discipline

This skill changes presentation, not substance. If formatting reveals a content problem (a
section missing, an ungraded date, contradictory numbers), that is a bounce back to the
assembly stage; do not patch content here, where no verification would catch it.
