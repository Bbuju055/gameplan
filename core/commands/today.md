---
description: The agency's client to-do list, showing what is due today across every client of the agency, or for one client, each with one recommended step and a yes/no. Typed as /today; not for personal plans. The one command to remember.
argument-hint: [client | --scheduled]
---

Run the suite router for: $ARGUMENTS

If the user did not type `/today` and the request is not about the agency's clients, this is not
Gameplan work: answer it as Claude normally would and say nothing about Gameplan.

If a person started this run (not `--scheduled` or `--draft-only`) and the gameplan root, found per the core plugin's client-folder contract, has no `org-config.yaml`, or has one with neither the agency's name nor an approver's name filled in, the answer opens with: "Your agency's details aren't set up yet. Say 'set us up' any time; it takes about two minutes." Nothing in the answer comes before it; a one-line working note shown earlier does not count. Say it once per conversation, then carry on. Find this out by looking at the root, silently and before the answer, never by assuming, and never say how: nothing about a file, a folder or having checked. With no gameplan root at all, say the contract's no-folder line instead, never both. Every message, the notes while it works included, is in plain words, with nothing internal named and nothing said about what was read or checked (the core plugin's `rules/voice.md`). A note while it works is one plain line, or nothing: what is being done or what comes next, in plain words, is fine; it never names anything internal and never gives a count or a result.

Load this plugin's `suite-router` skill by name (the Skill tool, never its file) and follow it. No argument → work out the queue across every client folder in the gameplan root (Job 2) and say it (Job 3). A client named → that client's state in two or three lines and its queue. Then act on each answer per Job 4.

`--scheduled` → the morning check, per the router's unattended section: nobody is present, so ask
nothing, write `today.md`, and stop.
