---
name: pitch-angle-notes
description: Per-reporter personalization research cards for the top targets, showing which angle to lead with and which to avoid, from each reporter's recent bylines, every claim linked. Runs automatically in the /target chain for the top reporters of each group (their angle goes on the list), or by name ("give me angle notes", "how should I pitch these people"). Research, never outreach. Cross-plugin requests route through core's suite-router.
---

# Pitch Angle Notes

Every message, the notes while it works included, is in plain words, with nothing internal named and nothing said about what was read or checked (the core plugin's `rules/voice.md`). A note while it works is one plain line, or nothing: what is being done or what comes next, in plain words, is fine; it never names anything internal and never gives a count or a result.

Per-pitch research for the top targets: the same search-with-receipts discovery uses, pointed at personalization.

## Fires

Automatically in the /target chain, after discovery and before the list is shown, for the top reporters of each group; and by name ("angle notes for Torres", "more angle notes"). The "Lead with" line goes on the reporter's row as the angle to lead with (the archive entry's `angle` field); the full card is shown with the list.

## Does

For the top 5 log reporters of each segment by score, plus every reporter with a live source request (the operator can ask for more; an accepted discovery gets a card only when asked), web-search each reporter's recent bylines and produce one **personalization research card** per reporter:

> **M. Torres, Fintech Current**
> Lead with: the AI-underwriting angle, not the funding amount. Her last two pieces [link] [link] focused on model risk in lending decisions, so the release's bias-audit paragraph is her hook.
> Avoid: the founder-story angle; she doesn't write profiles.

- Two to four lines per reporter, maximum.
- **Every claim about a reporter's recent work carries a link.**
- If recent work can't be verified for a reporter, the card says exactly that ("couldn't verify recent bylines: pitch on the beat match alone") rather than inventing a hook.

## Hard boundaries, as prohibitions

- **Produces research notes, never full pitch emails.** The publicist writes the pitch; this skill supplies the homework.
- **Never sends anything, never offers to.** No email drafting into Outlook/Gmail, no "shall I send this?" Automated sending is the line where the tool would start damaging the reporter relationships it exists to serve.
- Never pad a card with generic advice ("keep it short!") — subject-specific hooks or nothing.
- For a client-linked list, a hook that rests on something the client claims uses only claims
  approved in the client's claims ledger; a claim still awaiting support is named as such, and
  nothing the client's constraints rule out is suggested.
