---
name: office-files
description: How the Gameplan suite makes every Word or PowerPoint file and CSV it hands over, and reads an agency's .xlsx, with the gameplan-render command, its steps and the content shapes. Use when a Gameplan skill builds, fills, checks or reads one of these files for the agency's work; not for a person's own documents.
---

# Office files: one way to make them

Every message, the notes while it works included, is in plain words, with nothing internal named and nothing said about what was read or checked (the core plugin's `rules/voice.md`). A note while it works is one plain line, or nothing: what is being done or what comes next, in plain words, is fine; it never names anything internal and never gives a count or a result.

Every Word or PowerPoint file the suite hands over is made by `gameplan-render`, the core plugin's
command. Run it as `python3 "${CLAUDE_SKILL_DIR}/scripts/gameplan-render"` followed by its
arguments; below, `gameplan-render` stands for that whole command. Spreadsheets are CSV files,
written directly (UTF-8, a header row); Excel opens them.

**How any suite script is run.** A script's path comes from the skill that owns it, and it is
real only when that skill is loaded with the Skill tool: the folder name written in a skill's
command is filled in at load, and is not a shell variable. So load the owning skill before
running its script, and never run one from a skill file opened as text. No script is on the
PATH, and another plugin's folder cannot be found any other way.

**Never install a package, download a tool, or write document code of your own to make a file.**
If `gameplan-render` is not found, is refused, crashes, prints anything but its usual result, or
returns `error` for anything other than the content file or a name already taken, stop: tell the user in plain words that the file was not made and why, and keep the approved
content where it is. No file is better than an improvised one.

## Making a file

1. Write the approved content as JSON in the memory folder's `build/` folder (the client-folder contract's `<memory>/build/`, made the first time),
   named `<file name>.content.json`, extension kept (`x.pptx.content.json`), so a .docx and a .pptx
   of the same name never share one. Never in a client's folder or at the top of the gameplan root, which hold only what a person
   opens: the command refuses a content file anywhere else in the gameplan root. A line shown while this is done says
   "Building the <what it is>." ("Building the coverage report."), never "the content file".
   Shapes below. Text goes in exactly as
   approved, and every link is a full web address starting `http://` or `https://`; the command
   refuses anything else, so a story with no real address goes back to the review.
2. Run one of:
   - a suite format: `gameplan-render build --type <type> --content <content.json> --root <gameplan root> --client <slug> --out <file.docx>`;
     a brief adds `--decisions <its decisions.md>` and `--draft <its saved draft.md>`, and the
     build stops unless the gaps match the log line for line and every headline, summary, Signal
     line and the sources line stands in the saved draft word for word;
   - an agency's own `.docx` or `.pptx` registered in the memory folder's `templates/`:
     `gameplan-render fill --template <it> --content <content.json> --root <gameplan root> --client <slug> --out <file>`.
   Leave out `--client` only for work with no client folder (a keyword clips report, a list not
   linked to a client).
3. Read the result. `say`, when the result has it, is said in chat as it is, word for word, before the Saved line. `ok` means the file passed the residue check (every other client's name, in
   the text and in link targets, image descriptions and tooltips, any
   unfilled marker, text in hidden table cells, notes and metadata) and lists its links. The
   links are checked to be web addresses, not opened: never say they work or are live. An
   `allowed` line names another client that was let through because this client's own
   `competitors.md` lists it; nothing else is let through. Say nothing
   about a check that passed: the reply names the file and goes on (the core plugin's
   `rules/voice.md`). `error` names what is wrong: a content-file field → fix that field and
   run again, unless fixing it means changing approved wording or dropping approved content, which
   goes back to the review; a residue finding → the content carries another client's material, which is a
   content problem to bounce back, not to patch here; a client folder whose name cannot be read →
   no file can be checked until that folder's `README.md` has a first line with the client's
   name, so say which client's folder needs it and stop.
4. A file is never overwritten. Name it as the client-folder contract says (`<Client name> -
   <What it is> - <D Mon YYYY>.docx`, in `<Client name>/`: its `Drafts/` when it is saved for approval,
   the folder itself for the approved copy); a revised one ` - v2`, and the earlier one stays. When the name is already taken,
   take the next one (` - v2`, then ` - v3`) and build again. The command makes the folder the
   file goes in when it is not there yet (a client's first brief, pitch list or coverage
   report): never ask the person to make it.
5. Before handing over a CSV or an HTML page, run `gameplan-render check <file> --root <gameplan root> --client <slug>`
   (leave out `--client` for work with no client folder). It reports another client's name or an
   unfilled marker: fix what it reports, then check again. A line shown while it runs says
   "Checking the file." and no more: never the command, "the page check" or what the check
   looks for. When the check cannot be run here, say once what that means for the person, never "the automatic check": "I couldn't confirm this is free of other clients' names, so read it through before it goes out."
6. To read an agency's `.xlsx` (a media log kept as a file), run `gameplan-render read-xlsx <file>`:
   one sheet's rows as text, the file never written. It reads the first sheet, or the one named
   with `--sheet "<name>"`, and lists every sheet's name under `sheets`.
7. A scheduled task, which is not told a time zone, reads the date and time with
   `gameplan-render clock --zone <zone>` (the saved `org.time_zone`, a name such as
   `America/New_York`): it gives `date`, `time` and `weekday` in that zone. A conversation never
   needs it.

## Content shapes

Dates are written as they should read. No shape carries an "unvetted" banner (the client-folder
contract's Optional facts); an older content file's `constraints_unfilled` is accepted and
ignored.

- **daily-brief**: `client`, `window_start`, `window_end`, `prepared_date`,
  `categories` (in draft order: `name`, `stories`, and `empty_line` when `stories` is empty; a
  story: `headline`, `url`, `summary`, `source`, `date`, `signal` (the sentence alone, never a ⚠ or a reviewer tag), optional `also_carried_by`
  count, the number of other outlets: the cluster's size minus one), `method` (`sources_run` as the draft's sources line, which the file prints after "Sources run:" once, with or without that label given, `gaps` as the draft's gap sentences and an empty list when it has none, `included`, `candidates`,
  `approver`, `approved_at`; an older content file's `accepted_flags` is accepted and never printed: which claims were accepted stays in the decisions log and the claims ledger).
- **alert-brief**: the daily-brief shape with exactly one category, plus `alert_time`.
- **quarterly-snapshot**: `client`, `quarter`, `prepared_date`, `approved`
  (`name`, `date`, `version`, the number in the file's name: 1 for the first approved copy, 2 for a ` - v2`; leave it out while DRAFT), `milestones` (`client` and `field` line
  lists), `activity` (groups in the spec's order: `group`, `lines`), optional
  `activity_absent_line`, `next_quarter` (`events`, `deadlines` line lists).
- **clips-report**: `subject` (client or keywords), `period_start`, `period_end`,
  `prepared_date`, `approver` (the approval the file rests on; not printed),
  `at_a_glance` (`total`, `by_outlet_type` and optional `by_month` as `[label, count]` pairs,
  `agency_driven`, `organic`, `top_messages` as `[claim, count]` pairs, or `top_messages_omitted`
  for a keyword report, `tone` with `positive`, `neutral`, `negative`, `mixed`), `clip_groups`
  (optional `month`, `clips`: `outlet`, `headline`, `url`, `date` published, `reporter`, optional
  `from_export` when the article could not be opened to confirm it).
- **coverage-report**: `client`, `campaign`, `pitch_date`, `report_date`, `targeted` (the reporters who were pitched),
  `placements` (`reporter`, `outlet`, `headline`, `url` or an operator `note`, `date`, `segment`),
  `by_segment` (`segment`, `targeted`, `covered`, `no_coverage`, `unresolved`), optional
  `discovery_line`, optional `ai_visibility`.
- **landscape-report**: `client`, `space`, `prepared_date`, `horizon`, `approved` (`name`,
  `date`; leave it out for the copy shown for approval, which reads "Draft for review"); page one,
  all bullets: `stands` (1 to 3 lines), `dates` (1 to 3: `when`, `what`, `grade`, `why`), `risk`,
  `opportunity`, `actions` (`what`, `by`), `confidence` (one line); then the evidence:
  `competitors` (`name`, `tier` in plain words, `why`), `timeline` (`when`, `who`, `what`,
  `grade`, `basis`), `scenarios` (`event`, `window`, `grade`, `branches`: `outcome`, `messages`
  lines, `holding`), `gaps` and `method` line lists.
- **wargame** (a wargame run by itself): `client`, `space`, `prepared_date`, `approved` (`name`, `date`; left out for the copy in `Drafts/`, which reads "Draft for review"), `events` (each `event`, `window`, `grade`, `branches`, and `pre_positioning` for an inherited-risk event; each branch `outcome`, `likelihood` when one is given, `read`, `terrain`, `messages`, `posture`, `holding`, and `qa` lines for a high-relevance branch), then the line lists `cross_event`, `watch` and `before_use`, and `say` (the lines said in chat when the file is handed over: 1 to 3, each 260 characters at most; never printed in the file). Every line of `messages` carries exactly one claim tag, `✓substantiated` or `⚠needs-support`: the command builds no file otherwise.
- **catalyst-timeline** (a timeline run by itself): `client`, `space`, `prepared_date`, `horizon`, `approved` as above, `next_90` and `later` (each event `when`, `who`, `what`, `grade`, `basis`, and `why`, the line saying what it changes for the client), `collisions` lines, `inherited_risk` (`when`, `who`, `what`, `grade`, `means`, `deadline`), `undateable` and `dating_gaps` lines, and `say` (the lines said in chat when the file is handed over: 1 to 3, each 260 characters at most; never printed in the file). A part with nothing in it is an empty list, and the file says none was found.
- **fill**: `title` (the file's title), `replace` (each inline placeholder, braces included, to
  its text), `lists` (each placeholder line to its lines; an empty list removes the line),
  `pictures` (a logo block's alt text to `{"text": ...}` or `{"image": "<path to a file of the
  block's type>"}`). The template's mapping spec says what each placeholder takes.
