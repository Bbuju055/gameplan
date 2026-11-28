---
name: setup
description: Set the suite up for an agency by talking ("set us up", "set up Gameplan", "change our agency name", "our media list moved"). Asks once, in one message (your name, the agency name, and where the media list lives if there is one), writes the agency's org config into the gameplan root, and ends with what is set and the next step. Cross-plugin requests route through core's suite-router.
---

# Setup

Every message, the notes while it works included, is in plain words, with nothing internal named and nothing said about what was read or checked (the core plugin's `rules/voice.md`). A note while it works is one plain line, or nothing: what is being done or what comes next, in plain words, is fine; it never names anything internal and never gives a count or a result.

The agency sets the suite up in conversation. Nobody sees the org config, YAML, a key name, or
`TODO(org)`; they answer questions and Claude writes the file. Load the core plugin's
client-folder contract (for the gameplan root) and org-config skill (for the keys) first,
silently.

## Before the questions

These checks are silent: never say what was found or looked for. Saying what an agency already has set is the answer to an agency set up before, not a finding, so it is said.

- **Find the gameplan root** per the contract. No root (a project with no folder) → say the
  contract's no-folder line and stop: there is nowhere to keep the agency's details.
- **Already set up** (the agency's `org-config.yaml`, in the memory folder, has the agency's name or an approver's name
  filled) → say in two or three plain lines what is
  set, and ask what they want to change. Only what the suite still uses counts as set: a value an
  older config holds that the shipped one no longer has (a claims sign-off column, say) is left in
  the file and never mentioned. Ask only about that, then write and close as below. A
  config saved before the approver's name existed has no `org.approver_name`: say what is set
  the same way, then ask question 1 as the only question in that message; once it is answered
  and written, ask what they want to change.
- **Not set up** (no `org-config.yaml` in the memory folder, or one with neither of those filled: a file
  with nothing in it is not a setup) → open with "Setting up takes about two minutes." with nothing before it, then ask the questions below in that one message, and nothing else.
  Every question can be skipped ("not sure", "later"); a skipped answer leaves that value unset.

## The questions

One message asks all three, numbered, and the person answers in one reply. The only thing asked
again is a name still missing from question 1 or 2, once. No answer is confirmed back and none is
acknowledged ("Saved.", "Got it."): after the reply, the next thing said is the closing.

1. **Your name**, as it should appear on what you approve ("J. Alvarez"). Say why in one line: it
   goes on everything you approve, so nothing asks "approved by whom?" again. Writes
   `org.approver_name`.
2. **The agency's name**, as it should appear on reports. From it, work out the short name used in
   a sentence and the confidential footer ("Prepared by <name> - Confidential") and write them:
   never ask the person to confirm them. A name typed all in lower case gets ordinary capitals.
   The closing shows both as they will print, and that is where a wrong one is caught. Writes
   `org.name`, `org.short_name`, `org.confidential_footer`.
3. **Where the agency's media list lives, if it keeps one.** Asked as something to skip: "If you
   already keep a list of reporters, tell me where it is (a spreadsheet in Microsoft 365 or
   Google, or a file). If not, skip this: I'll start one with your first media list."
   Ask only where it is, never about its
   columns; reading the list comes later, on the first media list or target list.
   - Microsoft 365: the file's link, or its name and the site it sits on; ask once for whichever
     is missing. Write
     `media_log.source: m365` and fill `sharepoint_site`, `library_path` and `file_name` from what
     they give; ask for the sheet name only if they mention more than one.
   - Google Sheet: its name or link. `source: google`, `google_sheet`.
   - A file: ask them to put it in the project's folder and name it. `source: file`, `file_path`
     relative to the gameplan root. If it is not there yet, leave `source` unset and say so in the
     closing summary.
   - No list: `source: suite`. No answer to this question is no list.
   - Who looks after a list of their own is taken when they say it ("Priya Natarajan looks after
     it") and never asked. Writes `media_log.log_owner`. Not given → new names
     wait "for whoever looks after your media list".

Two things are never asked. Each is taken whenever the person gives it, in that reply or any later
one:

- **A logo.** A PNG or JPG they put in the project's folder and name. Writes `brand.logo` as its
  file name, relative to the gameplan root. Not given → the agency name prints as text where a
  logo would go.
- **Other people who approve work here.** Their names, as they should appear.
  Writes those names to `org.team_approvers` (the first person's stays in `org.approver_name`)
  and changes the closing, below. Told that others will use this but given no names → nothing is
  written for it and approvals carry the one name.

Never ask for anything else here: brand colors, fonts, the contact email, the digest mailbox and the
targeting tuning keep their shipped values. The exceptions are things they ask to add:

- the contact email (SEC's own search asks for it in Claude Code): write `org.contact_email` as
  given, the agency's address, never a person's;
- the mailbox that receives journalist source-request digests: write `digest_inbox.mailbox`, and
  the digests' sender addresses to `digest_inbox.digest_senders` when they give them;
- another approver, at any time ("add Sam Ortiz as an approver"): add the name to
  `org.team_approvers`;
- the time zone the morning check works in ("we're on Pacific time"): write `org.time_zone` as
  its full name (`America/Los_Angeles`). It is otherwise asked only when that check is set up.

## Writing

A value is written once its question is answered, never before (the client-folder contract's Writing, and what a reply may say).
Write only the values answered, to `org-config.yaml` in the memory folder (the client-folder
contract's `<memory>/`, made now if it is not there). With a file already there:
Replace only the values answered, keep every other line and comment as it is. With none, make it holding just the
answered values, each under its section and key as the shipped default names them (read
`${CLAUDE_PLUGIN_ROOT}/config/org-config.yaml` for the names and the nesting; none of its other
lines go in). Everything not answered stays the shipped default's and is never written. Then read
it back and check each answered value is there. Say nothing about the file.

## Closing

Short parts, plain words, no key or file names:

- **Set:** what was saved, one line each ("Reports will say Prepared by Lanthorn & Reed PR -
  Confidential"), the agency's name as it will print in a sentence among them. The approver line says who it covers: with one name saved, "Priya Nair goes on
  everything you approve"; with other approvers saved, one line naming them all ("Priya Nair, J.
  Alvarez and Sam Ortiz can approve work here"), never the single-name line as well.
- **Optional:** what was skipped and what it costs ("No logo: the agency name prints as text in
  its place"), each with how to add it in a few words ("put one in this project's folder and tell
  me its name"; with one name saved and no word of colleagues, "If colleagues approve work too,
  give me their names any time"), and always this line: "For complete trial and research coverage, add the free
  Clinical Trials and PubMed connectors (Customize, then Connectors). Any news-monitoring or
  journalist database service you already have connected there is used too."
- **Before your first pitch list:** only when the media list cannot be read yet, and this is the only place the media list is spoken of after the reply. A pitch list
  is built from the agency's list, so say what it waits on, in the reporter list's own two sentences: "I don't know where your media list
  is yet." followed by "Pitch lists can't run until you tell me.", or, with no list of their own,
  "You don't have a media list yet: your first media list starts one."

- **Working as a team:** only when more than one person will use this. "Each person's Claude only
  sees lists saved in the folder their project is linked to, so a colleague's pitches won't show
  in a repeat-pitch check unless you share that folder. To share it, keep this project's folder
  in a drive your team already syncs, such as OneDrive or Google Drive, set to stay on each
  computer, and have each person link their own project to it. Everyone with that folder can see
  every client in it." Then, with other approvers saved: "I'll ask once in each conversation who
  is approving, so each approval carries that person's name." With none saved: "Everything
  approved here carries <name>. Give me your colleagues' names any time and I'll ask who is
  approving instead."

Then how to change any of it later ("say 'set us up' again any time"), and last, always, the
next step, as one question: with no client folder yet, "Next, set up your first client: say
*set up* and the client's name. Want to do one now?"; with clients already, "Next, ask what's due
for your clients." A yes (or a client's name) hands over to the suite router's set-up-a-client
job. Nothing else is offered: the daily routine is said when a client is fully set up.
