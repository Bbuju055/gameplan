---
name: org-config
description: The suite's org config, the one file that says who the agency is (name, brand, confidential footer, the approver's name, and media-targeting's media log, pending-review workbook, digest inbox, and archive). Where the file lives, how it is resolved, and the TODO(org) rule every skill follows for an unfilled value. Loaded by other skills before they read any org value; not a user-facing entry point.
---

# Org config

Every message, the notes while it works included, is in plain words, with nothing internal named and nothing said about what was read or checked (the core plugin's `rules/voice.md`). A note while it works is one plain line, or nothing: what is being done or what comes next, in plain words, is fine; it never names anything internal and never gives a count or a result.

Every org-specific fact in the suite lives in one file, `org-config.yaml`, shipped by the core
plugin with neutral defaults. No skill hardcodes an agency name, a footer, a brand color, a
SharePoint location, a reporter-list location, or a mailbox; it reads the value from here. A skill that cannot load this
file treats every value as not set up for this workspace and says so once, in plain words,
never from memory of some other agency.

## Resolving the file

Read, in order, the first that exists:

1. `org-config.yaml` at the **gameplan root** (the root found as the client-folder contract
   says, the same root that holds `clients/`, `templates/`, and `Deliverables/`). This
   is the agency's filled copy; a plugin update never touches it.
2. `${CLAUDE_PLUGIN_ROOT}/config/org-config.yaml`, the shipped default in the core plugin.

In an eval, a fixture presented as the org config stands in for both.

**Not set up yet.** In a run a person started, when the gameplan root, found per the core plugin's client-folder contract, has no `org-config.yaml`, or has one with neither the agency's name nor an approver's name filled in, the answer opens with: "Your agency's details aren't set up yet. Say 'set us up' any time; it takes about two minutes." Nothing in the answer comes before it; a one-line working note shown earlier does not count. Say it once per conversation, then carry on. Find this out by looking at the root, silently and before the answer, never by assuming, and never say how: nothing about a file, a folder or having checked. With no gameplan root at all, say the contract's no-folder line instead, never both.
It is never said in an unattended run, and never during setup itself (core's setup skill opens
with its own line). After it, carry on with the shipped default; nothing is written until they
ask for setup. Every command and the suite router carry these sentences word for word, because a
run reads its entry point before anything else: keep them identical.

## The keys and who reads them

| Section | What it holds | Read by |
|---|---|---|
| `org.name` | The agency's display name, for footers, cover pages, and report headers | every renderer |
| `org.short_name` | The name as it reads in a sentence ("a <short_name> client", "<short_name>'s own engine") | every plugin's user-facing prose |
| `org.confidential_footer` | The footer line on exports and reports | export-list, track-outcomes, brief-render, pulse-render, client-deliverable |
| `org.contact_email` | The agency's address for public data sources that ask automated requests to identify themselves (SEC EDGAR); never replaced by a person's own address | source-sweep |
| `org.approver_name`, `org.team_approvers` | The people who approve what the suite makes (the client-folder contract's Who approves). One name saved → attached to every approval automatically; other names in `team_approvers` → a run asks once per conversation which of them is approving; none → asked once per conversation | every plugin with an approval step |
| `org.time_zone` | The zone a scheduled task works in, as a name such as `America/New_York`. Asked once, when the morning check is set up; a conversation never needs it, because the person's own clock gives the time | the suite router (the morning check), daily-brief's draft-only runs |
| `brand.colors`, `brand.fonts`, `brand.logo` | Primary and accent colors (hex, no #), heading and body fonts, logo path (relative to the gameplan root) | client-deliverable, brief-render, pulse-render |
| `media_log`, `pending_review`, `digest_inbox` | Where the media log lives (`media_log.source`: a Microsoft 365 workbook, a Google Sheet, a file in the gameplan root, or the suite's own list) and its column map, where pending-review rows go, the digest mailbox. An unset `source` means Microsoft 365 when the SharePoint location is filled, else the suite's own list when it exists, else no list yet | media-targeting only (the log and pending review through its reporter-list skill) |
| `scoring`, `parsing`, `history_windows_days`, `discovery` | Tuning for the targeting chain; the agency's parsing rules and AI-cited outlets are files in `<gameplan root>/media/` | media-targeting only |
| `next_actions` | Thresholds for the next-action rules: how many suggestions show at once, how long "not now" lasts, each rule's day counts, and the morning check's look-ahead | the suite router |

## The TODO(org) rule

A value still equal to `TODO(org)` is a placeholder, not a value.

- A skill that needs it **states the gap in plain English** ("the media log's location has not
  been set up yet; say 'set us up' to add it") and degrades the way its own skill says. It
  never guesses, never fills in a plausible agency, and never substitutes another agency's value
  it may have seen elsewhere.
- Loading this config is silent, apart from the not-set-up line above. No "config loaded",
  "skills loaded", or "archive is configured" preflight line ever reaches the operator; the first
  thing they read is that line or the work.
- The operator never sees a key name, a file name, or YAML, and never hears about this file,
  the gameplan root, the shipped default, or "config" at all. In conversation the gap is only
  ever "<the item> has not been set up for this workspace yet". The only setup guidance in a
  run is the not-set-up line above and, where a value is needed, "say 'set us up' to add it".
- **The literal `TODO(org)` never appears in a deliverable, a client-folder file, a hand-off, or
  a message.** It is a value in the config file and nothing else. Where an unset value would be
  printed, the renderer omits that element: no footer line, no org mark, an empty header cell.
  Where it would be spoken, the sentence says "the agency". Never write "org config not loaded"
  or any other machinery note into a document.
- `brand.logo` unset means the org name renders as text where the logo would go. Brand colors
  and fonts always have a shipped default and are never a gap.
- An unfilled `org.name` or `org.short_name` is a gap only where the name would be printed; in
  conversation, say "the agency".

`grep 'TODO(org)'` on the agency's `org-config.yaml` lists exactly the values it still has to fill.
