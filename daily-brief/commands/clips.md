---
description: The coverage report for a client or keywords over a period, with verified clips, the approved messages they carry, agency-driven versus organic, approved once before the Word report is built.
argument-hint: <client or keywords> <period, e.g. "September" or "Q3">
---

Run the coverage report for: $ARGUMENTS

If a person started this run (not `--scheduled` or `--draft-only`) and the gameplan root, found per the core plugin's client-folder contract, has no `org-config.yaml`, or has one with neither the agency's name nor an approver's name filled in, the answer opens with: "Your agency's details aren't set up yet. Say 'set us up' any time; it takes about two minutes." Nothing in the answer comes before it; a one-line working note shown earlier does not count. Say it once per conversation, then carry on. Find this out by looking at the root, silently and before the answer, never by assuming, and never say how: nothing about a file, a folder or having checked. With no gameplan root at all, say the contract's no-folder line instead, never both. Every message, the notes while it works included, is in plain words, with nothing internal named and nothing said about what was read or checked (the core plugin's `rules/voice.md`). A note while it works is one plain line, or nothing: what is being done or what comes next, in plain words, is fine; it never names anything internal and never gives a count or a result.

Load this plugin's `clips-run` skill by name (the Skill tool, never its file) and run it end to end. The first argument is the client (or the keywords, when no client folder matches); the rest is the period. No period → ask once. The approval is never skipped: nothing renders without it, recorded under the approver name saved at setup.

Throughout: the user is a communications professional, not technical — plain business English, no internal machinery, no em dashes in user-facing prose, choices framed simply.
