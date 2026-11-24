---
description: What AI engines say about a client, checked against its approved claims. The first run sets it up and measures straight away (the questions just run; they are listed in the report and changed by typing); one approval, then the report. Also the third step when the core plugin's suite router sets a client up.
argument-hint: <client> [--baseline]
---

Run Narrative Pulse for: $ARGUMENTS

If a person started this run (not `--scheduled` or `--draft-only`) and the gameplan root, found per the core plugin's client-folder contract, has no `org-config.yaml`, or has one with neither the agency's name nor an approver's name filled in, the answer opens with: "Your agency's details aren't set up yet. Say 'set us up' any time; it takes about two minutes." Nothing in the answer comes before it; a one-line working note shown earlier does not count. Say it once per conversation, then carry on. Find this out by looking at the root, silently and before the answer, never by assuming, and never say how: nothing about a file, a folder or having checked. With no gameplan root at all, say the contract's no-folder line instead, never both. Every message, the notes while it works included, is in plain words, with nothing internal named and nothing said about what was read or checked (the core plugin's `rules/voice.md`). A note while it works is one plain line, or nothing: what is being done or what comes next, in plain words, is fine; it never names anything internal and never gives a count or a result.

1. **Client folder and question set.** Resolve the client folder per the core plugin's
   client-folder contract (pulse-run's step 1 loads it; if core is not installed, stop and say
   so). No client folder → say so in plain terms and offer to set the client up (the core
   plugin's suite router); never build questions for a guessed client identity. If
   `narrative/question-set.md` does not exist, this is the first run: build the questions now
   (below) and go straight on to measuring. Nothing is asked first.

   **First run.** Load this plugin's `question-set` skill by name (the Skill tool, never its file) and run it: usually 12 to 20
   questions in three families from the client folder, the latest landscape, and the client's
   own questions (`own-terms.md`), written as in use, with no confirmation step. Create
   `narrative/` in the client folder from the templates: `question-set.md`, `engines.md`, and an
   empty `decisions.md`. Then run the chain below as the baseline (`--baseline`): the first
   measurement, kept so later runs can be compared with it once comparison exists.
2. **Chain.** Load this plugin's `pulse-run` skill by name (the Skill tool, never its file) and run it end to end.
   `--baseline` (and every first run) means the first measurement: every question is asked
   exactly twice per engine asked automatically (two passes, never one, never three) to estimate
   noise, the scores are saved as the baseline, and there is no comparison. Without
   `--baseline`, the run is scored on its own and is not compared with the baseline; say so once,
   in plain words ("This run isn't compared with the first one yet."), never as a version number.
3. **One stop: approving the findings.** Nothing renders without the approval recorded in the
   run's review file, under the approver name (the client-folder contract's Who approves). That
   one approval also approves the report; nothing asks again. A disputed finding is called
   "wrong" only when it traces to an approved claim or a filing.

**Changing the questions** at any time, in plain words ("add a question: is Pellamune a credible
partner?", "drop the one about kidney cancer"): question-set's Changes section. It applies from
the next run.

Throughout: plain business English, no internal machinery in conversation, no em dashes in
user-facing prose.
