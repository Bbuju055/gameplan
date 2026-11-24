# core

**Start here.** Say *set us up*, then *set up* and a client's name: core sets the client up across
every plugin on one go-ahead, keeps a page of where things stand for each client, and says what's
due whenever you ask. Underneath, it is the base every Gameplan plugin needs: client folders, the
firm's setup, Word and PowerPoint files. New here? Start with the [getting-started guide](GUIDE.md).

The shared foundation of the suite and its front door. These live here and nowhere else:

| What | Where | Who reads it |
|---|---|---|
| The client-folder contract | `skills/client-folder-contract/SKILL.md` | competitive-intel (client-profile, client-onboard), daily-brief (brief-run), narrative-pulse (pulse-run), media-targeting (/target, curate-and-archive, track-outcomes) |
| The untrusted-content rule | `rules/untrusted-content.md` | every plugin; each skill keeps its own short inline version and points here for the full rule |
| The org config | `config/org-config.yaml`, resolved by `skills/org-config/SKILL.md` | every plugin for name, footer, brand, and the approver's name; media-targeting for the media-log, inbox, and archive sections; the suite router for the next-action thresholds |
| The suite router | `skills/suite-router/SKILL.md`, with `ROUTING.md` (which plugin answers what) and `rules/next-actions.md` (what each client needs next) | every session: plain-language requests, setting a client up across every plugin (`/gameplan`, "set up <client>"), each client's status page, "what's next", and the close of every run |
| The source rules | `rules/sources.md` | every search step: the client's own terms, and any fitting connector the user has |
| The voice rule | `rules/voice.md` | every message a run shows, the notes while it works included; each command and each skill carry a one-line version and point here |
| The status page | `templates/status-page.html` and its `.md` spec | the suite router: `Deliverables/<Client>/<Client> - Where things stand.html` |
| `/today` | `commands/today.md` | the user: the next actions across every client, or for one |

core's one command is `/today`; every other request can be made in plain words and the router
sends it on. The daily routine is to open the project and ask what's due: `/today` gives the queue,
what's coming up, and the day's briefs, each started on a yes. No schedule is needed. For someone who
asks, one optional scheduled job per gameplan root, the morning check, runs `/today --scheduled`
every day: it starts each client's brief draft and writes what is due for every client into
`today.md` at the root. Install core with the plugins; a plugin that
needs the contract and cannot load it stops and tells the user core is not installed, in plain
words.

## The contract, in two parts

Part one is **structure**: the file names, the provenance line on every fact, who approves and
how, the optional facts, the Deliverables folder, the proposed-updates flow, the PROFILE block. Someone reading part one alone could build a
client folder for a law firm; they could not fill it in, but they would know its shape.

Part two is **field semantics**: what the pipeline file holds, what a catalyst grade is, what the
evidence tiers mean, how competitors are tiered. Today that is life sciences. A domain pack
replaces only part two.

media-targeting reads a client folder only when a release is for a client: claims, constraints,
and calendar, and it appends pitches and placements to the activity log. A release with no client
runs without one.

## Changelog

- **1.1.0**: setting the agency up asks once; a client is set up in two stops; one approval per output by the person running it, under the name saved at setup;
  the folder approved at onboarding; optional facts never a warning or banner; claims approved
  once and written back; everything people open in `Deliverables/<Client>/` with plain names;
  the set-up-a-client job, the status page, the source rules, and the Word landscape layout.
- **1.0.0**: first public release.
