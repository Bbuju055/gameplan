---
description: The daily client media brief. Gather, curate, one approval, the Word file in the client's Deliverables folder, decisions logged. The first time, it saves what to watch from the client folder, with no question, and says it in one line. Also handles off-cycle alert briefs.
argument-hint: <client> [YYYY-MM-DD | date range] [--draft-only | --alert]
---

Run the daily media brief for: $ARGUMENTS

If a person started this run (not `--scheduled` or `--draft-only`) and the gameplan root, found per the core plugin's client-folder contract, has no `org-config.yaml`, or has one with neither the agency's name nor an approver's name filled in, the answer opens with: "Your agency's details aren't set up yet. Say 'set us up' any time; it takes about two minutes." Nothing in the answer comes before it; a one-line working note shown earlier does not count. Say it once per conversation, then carry on. Find this out by looking at the root, silently and before the answer, never by assuming, and never say how: nothing about a file, a folder or having checked. With no gameplan root at all, say the contract's no-folder line instead, never both. Every message, the notes while it works included, is in plain words, with nothing internal named and nothing said about what was read or checked (the core plugin's `rules/voice.md`). A note while it works is one plain line, or nothing: what is being done or what comes next, in plain words, is fine; it never names anything internal and never gives a count or a result.

This is the plugin's master entry point. Sequence:

1. **Profile.** Resolve the client folder per the core plugin's client-folder contract
   (brief-run's step 1 loads it; if core is not installed, stop and say so). If the folder exists but has
   no `monitoring/` files, run this plugin's `monitoring-config` skill (loaded by name)'s new
   setup straight away: it saves the watch terms and asks nothing, and today's brief goes on with them. If
   no client folder exists at all, stop and offer to set the client up (the core plugin's suite
   router); a brief must never run on a guessed client identity.
2. **Chain.** Load this plugin's `brief-run` skill by name (the Skill tool, never its file) and run it end to end.
   Treat the first argument as the client. A date argument sets the coverage window (the default is
   brief-run's, its step 4).
   `--draft-only` runs gather + curate and stops with the draft saved — this is the scheduled
   morning mode; the review gate then happens when a person opens the session.
   `--alert` runs the off-cycle path: consume the triggering radar alert, gather only around it,
   and surface any wargamed holding language the client folder carries for this event.
3. **One approval, never skipped.** Nothing renders and nothing is marked send-ready without the
   approval recorded in the decisions log, under the approver (the client-folder contract's Who approves). `--draft-only` defers the approval; it does not waive it.

Throughout: the user is a communications professional, not technical — plain business English,
no internal machinery, no em dashes in user-facing prose, choices framed simply.

If the user asked for configuration ("change the queries", "add a source"), run
this plugin's `monitoring-config` skill (loaded by name) instead; for the monthly learning pass,
this plugin's `brief-tune` skill (loaded by name).
