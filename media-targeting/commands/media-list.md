---
description: Build or refresh a beat media list for a client or a topic, with the reporters actually covering it compared with your list and the names you already have on that beat checked for moves. Reviewed on a page; only what you approve is added.
argument-hint: <client or topic>
---

Run the media list for: $ARGUMENTS

If a person started this run (not `--scheduled` or `--draft-only`) and the memory folder (the core plugin's client-folder contract) has no `org-config.yaml`, or has one with neither the agency's name nor an approver's name filled in, the answer opens with: "Your agency's details aren't set up yet. Say 'set us up' any time; it takes about two minutes." Nothing in the answer comes before it; a one-line working note shown earlier does not count. Say it once per conversation, then carry on. Find this out by looking at the root, silently and before the answer, never by assuming, and never say how: nothing about a file, a folder or having checked. With no gameplan root at all, say the contract's no-folder line instead, never both. Every message, the notes while it works included, is in plain words, with nothing internal named and nothing said about what was read or checked (the core plugin's `rules/voice.md`). A note while it works is one plain line, or nothing: what is being done or what comes next, in plain words, is fine; it never names anything internal and never gives a count or a result.

Load the suite's org config (the core plugin's `org-config` skill), then follow this plugin's `media-list-run` skill (loaded by name). No argument → ask one question: "Which client or topic?" The operator is non-technical. They never see JSON, file paths, column names, or skill names — plain English throughout.
