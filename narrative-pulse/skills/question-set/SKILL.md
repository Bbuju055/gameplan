---
name: question-set
description: 'Build a client''s Narrative Pulse question set, usually 12 to 20 questions a real buyer would type (fewer when the calendar holds no confirmed or guided event), in three families (direct, class, catalyst), drawn only from the client folder, the latest landscape run and the client''s own questions, written straight into use with no confirmation step (they are listed in every report), and change it later when the user asks ("add a question …", "drop the one about …"). Used by /pulse on its first run, and for "what questions do we ask the engines". Judgment-free by design: it assembles from files; it does not invent facts or decide what matters. Cross-plugin requests route through core''s suite-router.'
---

# Question Set (Builder)

Every message, the notes while it works included, is in plain words, with nothing internal named and nothing said about what was read or checked (the core plugin's `rules/voice.md`). A note while it works is one plain line, or nothing: what is being done or what comes next, in plain words, is fine; it never names anything internal and never gives a count or a result.

The questions are the instrument. If they drift between runs, nothing is comparable; if they are
invented from general knowledge, the run measures the model's imagination. So: build from files,
fix the wording, put them in use, then never edit a question in place: a change is a new question.

## Inputs

- `positioning.md`, `pipeline.md`, `competitors.md`, `approved-claims.md`, `constraints.md`.
- `calendar.md` for the dated events, and `competitors.md` for the tiered set and its two lines from
  the landscape, `Class definition searched:` and `Incumbent named by the landscape:` (the
  landscape writes all of it on approval). No class definition line means no landscape has run.
- No web search, no engines, no general knowledge about the client. If a fact needed for a question
  is not in the folder, the question is not written and the gap is named.

## Families and rules

**Direct** (the client by name; 4 to 7 questions). The buyer's plain questions: what the company is,
what the lead asset treats and how far along it is, whether it is a credible partner, what the
latest news is. Names and asset codes come from `pipeline.md` exactly as written there.

**Class** (the client unnamed; 5 to 8 questions). This is where presence is measured, so the
client's name must not appear in the question. The class is the space the landscape run searched,
in the landscape's own words (indication × mechanism), not the client's broader self-description. The class definition line carries the landscape's words exactly; each class question stays inside that class and may put it in a buyer's plain words ("oral obesity pills"), never a wider field, the alternatives question below excepted.
With no landscape (no `Class definition searched:` line in `competitors.md`), write these questions
from the client's own description of its field in `positioning.md`, record the class as a starter
class, and say so in the one line; the report says presence was measured against a starter class
until a landscape runs.
Include one "alternatives to <the incumbent product>" question when the landscape names an approved
comparator, and one "who are the leaders in <class>" question.

**Catalyst** (1 per FIRM or GUIDED event on the calendar; none for ESTIMATED or SPECULATIVE). Written
before the event so every run asks the identical wording: "What did <client>'s <trial>
show?" or "What happened at <event> for <class>?". If the calendar holds no FIRM or GUIDED event,
this family is empty and the set says so.

Every question carries: `id` (Q01…), `family`, `question`, `source_file`, `added_on`, `retired_on`
(blank), `confirmed` (`yes` means in use; see Writing the set). Wording rules: one question per line, buyer's voice, no jargon a
BD analyst would not type, no leading phrasing that presupposes the client's positioning.

## Framing labels (defined here, used by answer-score)

Propose a fixed label list for this client, four to six labels, from the positioning file and the
landscape's competitive read:

- `own-positioning` — the answer tells the client's own story in substance.
- `third-party` — a competitor's or analyst's framing of the space.
- `legacy:<what>` — a superseded story (a discontinued program, a prior pivot), named.
- `absent` — the client is not mentioned where it should be (class questions).
- Client-specific labels where the folder supports them, e.g. `format-only` when an answer reduces
  the client to its dosage form.

## Entities block (read by the scoring script)

Write an `## Entities` section: the client with its aliases and asset codes; each tiered competitor
with aliases and asset codes, tier from `competitors.md`; the incumbent products named in the
landscape. This is what presence and share of voice are counted against, so aliases matter:
"Veltrix", "Veltrix Bio", "VLX-401" are one entity. Every name the folder gives a company counts: its names, its asset codes, current or discontinued, and its trial names. A company the landscape demoted or removed is not written here in any role: every line in this section is counted.

## Engines

Write the engine list from the plugin's source-dependencies to `engines.md`: Claude (labelled
"<org short name>'s own engine", filling `{{ORG_SHORT_NAME}}` in engines.md per the core plugin's
`org-config` skill; the user hears only the filled label, never where the name came from), OpenAI
and Perplexity. Conditions: fresh helper for Claude, no history, region US, one question per call.
These are never varied between runs without a decisions-log entry.

What to expect is said once, in engine-query's message before the first question, never in this skill's one line, and promises nothing more: Claude is asked on every run,
in a fresh helper on the agency's own account. ChatGPT and Perplexity are asked too if they can be
reached automatically; if not, the step and the report are named for what was measured ("What
Claude says about Pellamune"), and the report says which engines were not measured.

## Talking to the user

The user is a communications professional. Plain business English in conversation: no file
names, no "HAND-OFF", no key: value blocks, no stage numbers. Reading the folder, rules, and
templates is silent: the reply opens with the work, never with the folder's status or with what
was loaded or resolved. The output contract at the end of this skill is for skill-to-skill use only; when this
skill is run for a person (via /pulse), the block
is written to the folder and never shown in the reply.

## Writing the set (no confirmation step)

Nobody is asked to read and confirm the questions. Write `narrative/question-set.md` from
`templates/question-set.md` with every question's `confirmed` column set to `yes` (it means "in
use") and the status line "In use since <date>". The client's own questions from `own-terms.md`
(kind `question`) are added in their family with source "asked for by <name>". Say one line, no
table: "I'll ask 16 questions about Pellamune: by name, about the field, and about the dates
coming up. They're all in the report; tell me any time to add or drop one." Then the run goes on.

## Changes, any time, in plain words

- **Add** ("add a question: is Pellamune a credible partner?"): a new id, its family worked out
  from the wording (by name → direct; the field without the client → class; a dated event →
  catalyst), source "asked for by <name>", `added_on` today, `confirmed: yes`. The wording is the person's own as typed, with only a capital letter and a question mark put right: the wording rules above are for the questions this skill builds. It is asked from
  the next run, and its comparison starts from its own first run.
- **Drop** ("drop the one about kidney cancer"): fill `retired_on` with today and record the
  user's words as the reason under `## Dropped`. When they gave no reason, their message as typed is the reason. Never deleted; earlier runs stay readable.
- **Reword:** a drop and an add, so earlier answers stay comparable to the question they were
  asked.

Confirm each change in one line ("Added: is Pellamune a credible partner? It's asked from the next check.") and nothing more: the family ranges are for building the set, so a change that leaves a family short is not remarked on.

## Output contract

The rules every block follows (empty fields, when it is written, who reads it) are the core plugin's `rules/hand-offs.md`.

```
### HAND-OFF: question-set
- status: in use since <date>
- counts: direct N | class N | catalyst N | in use N | dropped N
- class_definition: <the landscape's wording>
- framing_labels: <list>
- gaps: <facts the folder lacked that prevented a question, or "none">
```
