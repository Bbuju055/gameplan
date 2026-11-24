# Routing — which plugin answers which request

The suite-wide statement of routing. The suite router (`skills/suite-router`) loads it when a
request could go to more than one plugin, names a client without a task, or asks what to do next.
Each plugin's skill descriptions carry a one-line pointer here so they stay short. Inside
competitive-intel, its own `ROUTING.md` then picks the stage; this file never overrides it.

## The order

1. **An explicit command wins.** `/pulse`, `/target`, and the rest go where they say. The router
   does not second-guess them.
2. **Resolve the name before the intent.**
   - A client (a folder resolves per the client-folder contract): work in that client's context.
   - A company in some client's `competitors.md`: answer in that client's context and say which
     client in one line. If it sits in several clients' fields, ask which.
   - Anything else: a question about it alone goes to competitive-intel's source-sweep with no
     client context. "Set up X", "onboard X", "we just signed X" or `/gameplan X` go straight to
     the suite router's set-up-a-client job (Job 5), which starts at once;
     nothing asks first whether X is a new client. Only a bare mention that might
     be a new client ("what about X?") gets the one question "Is X a new client?" "Set us up", "set up Gameplan" and
     the like name the agency, not a client: they go to core's setup skill. "Set up Pulse for X"
     names a part, not a client: it goes to that part (the table below).
3. **Route by what the user wants back**, not by the words used:

| The user wants back | Goes to |
|---|---|
| Today's news, "anything new on X" | daily-brief: today's brief if one exists, otherwise a signal pass without the full brief |
| Background, "what do we know", "can we say this", "how has X been covered" | competitive-intel source-sweep |
| Dates, "what's coming" | a read of the client's calendar (the suite router's "What's coming for a client"); competitive-intel's timeline only when a refresh is asked for, or for a space with no client folder |
| Messaging for one event, "what do we say if" | competitive-intel wargame |
| A new client, "set up X", "onboard X", "continue setting up X", `/gameplan X` | the suite router's set-up-a-client job (Job 5): every step, with two stops; steps already done are skipped |
| One part set up for a client, "set up Pulse for X", "set up the brief for X" | that part, never the set-up-a-client job: `/pulse`; `/brief`, whose first run saves the watch terms and drafts the first brief |
| The competitive landscape alone, "the works on X" for a client already set up | `/landscape` |
| "Where are we with X", "what's been done for X" | the client's status page (the suite router's Job 6) |
| "Approve X's folder", for a client folder not approved when it was built | competitive-intel's client-onboard, its folder approval only: the request is the yes, and nothing else in that skill runs |
| "Also watch …", "also look at …", "add a question …", "stop watching …" for a client | the client's own terms (the core plugin's `rules/sources.md`) |
| How AI answer engines describe the client | narrative-pulse |
| Reporters for a release, a pitch | `/target` |
| "The pitches went out" for a saved list, in any later session | media-targeting curate-and-archive's pitch logging: one pitch row per reporter pitched, nothing else runs |
| "Did we get coverage" on a list that was pitched | `/outcomes` |
| "It went to the client" for an approved document, coverage report, or Pulse report | the suite router's own answer (Job 4): the activity-log row and the `sent` row |
| Reporters on a beat, a media list, "who covers X" | `/media-list` |
| Coverage over a period, "what did we get in September" | `/clips` |
| "What's next", "what should I do today" | the queue (the suite router's own job) |
| Setting up the agency, or changing your name, its name, media list location or logo | core's setup skill |
| Re-export a saved list; a question about past pitches or hit rates | media-targeting's export and campaign-history skills |
| Change a client's brief: searches, sources, schedule | daily-brief monitoring-config |

4. **Inside a plugin**, that plugin's own routing decides the stage (competitive-intel's
   `ROUTING.md`; each command's chain elsewhere). A command or skill that hands over to another
   skill loads it by name with the Skill tool and never opens its file: a skill's own paths are
   filled in only when it is loaded.

## When two readings are plausible

- If they lead to work of materially different cost or length, ask one question with the
  recommended reading first: "A quick catch-up on Halden, or the full landscape? I'd do the
  catch-up."
- If the cost is about the same, take the cheaper reading and say so in one line.
- Never start a multi-stage chain on an ambiguous request.

## A client named

- **With a task:** route the task; no queue line goes in front of it. The next step comes at the
  close of the run the task starts.
- **With no task:** the client's state as the suite router says it (how far setting it up has
  got and the one thing that matters most now; never its review status, and dates go in the
  lines after the items) and the queue, then stop.

## A plugin that is not installed

Say in one line what the request needs ("That needs the media-targeting plugin, which isn't
installed here"). Never answer it with a different plugin standing in.
