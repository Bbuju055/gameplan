---
description: Track what a campaign actually landed. Find published coverage, record human-confirmed results, and produce the client-ready coverage report. Run 1–2 weeks after a campaign. Every run makes future targeting smarter.
argument-hint: <client or campaign, e.g. "Lumen Credit Series B">
---

Run the track-outcomes skill for: $ARGUMENTS

If a person started this run (not `--scheduled` or `--draft-only`) and the memory folder (the core plugin's client-folder contract) has no `org-config.yaml`, or has one with neither the agency's name nor an approver's name filled in, the answer opens with: "Your agency's details aren't set up yet. Say 'set us up' any time; it takes about two minutes." Nothing in the answer comes before it; a one-line working note shown earlier does not count. Say it once per conversation, then carry on. Find this out by looking at the root, silently and before the answer, never by assuming, and never say how: nothing about a file, a folder or having checked. With no gameplan root at all, say the contract's no-folder line instead, never both. Every message, the notes while it works included, is in plain words, with nothing internal named and nothing said about what was read or checked (the core plugin's `rules/voice.md`). A note while it works is one plain line, or nothing: what is being done or what comes next, in plain words, is fine; it never names anything internal and never gives a count or a result.

Load the suite's org config (the core plugin's `org-config` skill), then follow this plugin's `track-outcomes` skill (loaded by name). If the arguments don't identify a single finalized list, show the recent candidates and ask which one. Nothing is written until the operator confirms the findings — the archive records human-verified outcomes, not raw search results.
