---
name: client-profile
description: Load a client's folder (positioning, approved claims, voice, constraints, competitors, relationships) at the start of any client work so the chain runs on canonical client knowledge instead of interrogating the user. Use whenever a named client of the agency is the subject of competitive-intel, comms-planning, or drafting work, fired as Stage 0 of a landscape run, and directly for "load the [client] profile" or "what do we have on our client X". No client folder → offers the suite router's set-up job rather than guessing. Cross-plugin requests route through core's suite-router.
---

# Client Profile (Loader)

Every message, the notes while it works included, is in plain words, with nothing internal named and nothing said about what was read or checked (the core plugin's `rules/voice.md`). A note while it works is one plain line, or nothing: what is being done or what comes next, in plain words, is fine; it never names anything internal and never gives a count or a result.

Load the client folder and turn it into the chain's Stage-0 inputs. This skill retrieves and
summarizes; it never invents. A client folder is the canonical, approved record of what the
agency knows about its own client.

## Step 0 — Load the contract

Load the suite's client-folder contract (the core plugin's `client-folder-contract` skill). It
defines the folder's file set and trust rules, the provenance line on every fact, the
review-status rule, the proposed-updates flow, and the PROFILE block this skill emits; nothing
below restates them. **If the contract cannot be loaded, stop**: tell the user in plain words
that the suite's core plugin is not installed and client work cannot run without it. Do not
load the folder from memory.

## Resolving the client folder

1. Find the client as the core plugin's client-folder contract says (its Resolving the folder):
   by reading the folders under the **gameplan root** it finds and matching what the person
   typed against their names, never by working out a folder name from what was typed.
2. With no gameplan root, look via the SharePoint/OneDrive
   connector if one is connected, or files the user has attached to the session. If none of
   these resolve, ask.
3. **Found** → read every file in the folder (the file set the contract defines) and produce
   the PROFILE block.
4. **Not found** → tell the user in plain terms (the core plugin's `rules/voice.md` applies: no
   config-file names, no "filesystem" talk) and offer two paths: set the client up now
   (recommended: the core plugin's suite router sets it up across every step on one go-ahead,
   and every later run reuses it), or give what this run needs, for this run only: the skill that called says what that is, and nothing more is asked (for a landscape it is the client's positioning alone, never its competitors or the agency's relationships). In a cloud session, also offer the third path: attach the
   existing client folder files if the team has them elsewhere. A company that is only the subject of a question (a competitor, a company being looked up) is not a client: it is never said to be not set up, and no set-up is offered for it. Never fabricate a profile for
   an un-onboarded client. The only setup guidance is the contract's no-folder line, said
   once.

## The client folder schema (fixed, identical for every client)

The file set and each file's trust rule are the contract's; read them there, not from memory.
What the client cannot say, quiet periods and spokespeople are optional facts (the contract's
Optional facts): an unfilled `constraints.md` is never mentioned at the start of a run and never
becomes a banner. A run whose own output depends on one says so in one line with its result, and never stops for it.

## Output: the PROFILE block

When called by another skill (gameplan chain, landscape-report Stage 0, scenario-planning), emit
the PROFILE block exactly as the contract defines it — downstream stages read only this plus the
client folder files it points to. Its `conflict_inputs` line is what the conflict re-screen at Stop 1
checks.

## Staleness rule

A client folder is a snapshot. On load, compare the build/updated date against today: forward-looking
events (guided windows, hearing outcomes, pending INDs) older than one quarter are re-verified
by the chain's own sweeps rather than trusted — flag them in `staleness` so Stage 2 knows to
check. Static facts (identity, voice, history) don't expire this way.

On load, apply the calendar's lapse rule from the contract: a GUIDED row whose window has ended
with no outcome becomes LAPSED-GUIDED, with a dated change-log line. This is the only calendar
change made without a proposal; it is reported to the user as a finding, in plain words.

## Proposed-updates flow

This skill also carries updates back. When a chain run produces facts that belong in the client folder
(a newly discovered competitor, a new public claim, a changed status), show them with the
output they came from, in the message that asks for its approval. The approval of that output
writes them into the relevant file, dated and sourced, in the same act; nothing is written
before it (the contract's Proposed updates).
