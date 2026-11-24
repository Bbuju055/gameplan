---
description: Set a client up across all of Gameplan with two stops (client folder, competitive landscape, what AI engines say, daily brief, media list), or finish setting one up. Steps already done are skipped.
argument-hint: <client> [therapeutic space]
---

Set this client up across Gameplan: $ARGUMENTS

If a person started this run (not `--scheduled` or `--draft-only`) and the gameplan root, found per the core plugin's client-folder contract, has no `org-config.yaml`, or has one with neither the agency's name nor an approver's name filled in, the answer opens with: "Your agency's details aren't set up yet. Say 'set us up' any time; it takes about two minutes." Nothing in the answer comes before it; a one-line working note shown earlier does not count. Say it once per conversation, then carry on. Find this out by looking at the root, silently and before the answer, never by assuming, and never say how: nothing about a file, a folder or having checked. With no gameplan root at all, say the contract's no-folder line instead, never both. Every message, the notes while it works included, is in plain words, with nothing internal named and nothing said about what was read or checked (the core plugin's `rules/voice.md`). A note while it works is one plain line, or nothing: what is being done or what comes next, in plain words, is fine; it never names anything internal and never gives a count or a result.

This is the suite's master entry point. Hand it to the core plugin's suite router, its
set-up-a-client job (Job 5): it starts at once, stops twice (an early check, a closing approval), and runs every step still left, in order,
each run by its own plugin, ending with "<client> is fully set up" and what to do from here. Treat
the first argument as the client; remaining arguments as the therapeutic space, passed on to the
landscape step. If the core plugin is not installed, say so in plain words and stop.

A client already fully set up: say so in one line, show where things stand (the router's status
page), and offer the one thing most likely wanted, the landscape refreshed (/landscape).
