---
description: Build a graded catalyst timeline of upcoming news triggers for a competitive set or single company. No wargaming, just the dated forward map.
argument-hint: <company or space> [horizon, e.g. "12 months"]
---

Run the catalyst-timeline skill for: $ARGUMENTS

If a person started this run (not `--scheduled` or `--draft-only`) and the memory folder (the core plugin's client-folder contract) has no `org-config.yaml`, or has one with neither the agency's name nor an approver's name filled in, the answer opens with: "Your agency's details aren't set up yet. Say 'set us up' any time; it takes about two minutes." Nothing in the answer comes before it; a one-line working note shown earlier does not count. Say it once per conversation, then carry on. Find this out by looking at the root, silently and before the answer, never by assuming, and never say how: nothing about a file, a folder or having checked. With no gameplan root at all, say the contract's no-folder line instead, never both. Every message, the notes while it works included, is in plain words, with nothing internal named and nothing said about what was read or checked (the core plugin's `rules/voice.md`). A note while it works is one plain line, or nothing: what is being done or what comes next, in plain words, is fine; it never names anything internal and never gives a count or a result.

Load this plugin's `catalyst-timeline` skill by name (the Skill tool, never its file) and follow it. If the arguments name a single company, build the timeline for that company plus its immediate tier-1 context (a quick discovery pass per this plugin's `competitor-discovery` skill (loaded by name) is warranted if the competitive set is unknown — confirm the set with the user before sweeping). Default horizon 18 months unless the arguments say otherwise. Every date carries its confidence grade; collision windows are mandatory, not optional.
