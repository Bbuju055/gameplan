---
description: The competitive landscape for a client on its own, a Word document with a bullet page one (where the client stands, the dates that matter, the biggest risk and opportunity, what to do by when) and the evidence after it. Two stops, the competitor check and one approval.
argument-hint: <client> [therapeutic space]
---

Build the competitive landscape for: $ARGUMENTS

If a person started this run (not `--scheduled` or `--draft-only`) and the gameplan root, found per the core plugin's client-folder contract, has no `org-config.yaml`, or has one with neither the agency's name nor an approver's name filled in, the answer opens with: "Your agency's details aren't set up yet. Say 'set us up' any time; it takes about two minutes." Nothing in the answer comes before it; a one-line working note shown earlier does not count. Say it once per conversation, then carry on. Find this out by looking at the root, silently and before the answer, never by assuming, and never say how: nothing about a file, a folder or having checked. With no gameplan root at all, say the contract's no-folder line instead, never both. Every message, the notes while it works included, is in plain words, with nothing internal named and nothing said about what was read or checked (the core plugin's `rules/voice.md`). A note while it works is one plain line, or nothing: what is being done or what comes next, in plain words, is fine; it never names anything internal and never gives a count or a result.

1. **Profile.** Load this plugin's `client-profile` skill by name (the Skill tool, never its file) and resolve the
   client's folder. If none exists, offer to set the client up first (the core plugin's suite
   router, recommended) or proceed with what the user can give for this run only.
2. **The landscape.** Load this plugin's `landscape-report` skill by name (the Skill tool, never its file) and run it from
   Stage 0, feeding it the PROFILE block. Treat the first argument as the client; remaining
   arguments as the therapeutic space. Its two stops are the competitor check (with the conflict
   check, never skipped) and the one approval; nothing else stops the run except the trial
   registry not being live (the core plugin's `rules/sources.md`, When a source is missing).
3. **The document.** client-deliverable renders the Word landscape for approval and, on approval,
   the approved copy, applying the folder updates in the same act.

Throughout: the user is a communications professional, not technical; every message follows
the core plugin's `rules/voice.md`, and landscape-report's "Talking to the user" section for this run's words.

If the user asked for less than the full landscape ("just the timeline", "just the wargame"),
point them to /triggers or /wargame instead.
