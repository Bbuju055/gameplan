# Routing — which skill answers which request

One canonical statement of routing precedence for this plugin. Across plugins, the core
plugin's `ROUTING.md` decides first and hands competitive-intel requests here to pick the stage.
Skill descriptions carry a one-line pointer here so they stay short (every description loads
into every session); the full logic lives in this file and is loaded by the orchestrator when
it needs to decide.

## The rule

**The orchestrator wins whenever a request spans more than one stage.** Single-stage requests
go to the stage skill. Retrieval questions go to the retrieval primitive.

| The user wants… | Route to | Typical phrasings |
|---|---|---|
| Setting a client up across everything | the core plugin's suite router (via /gameplan), which runs client-onboard and landscape-report as its first two steps | "set up X", "onboard X", "new client" |
| The full chained product: set + timeline + wargame + document | **landscape-report** (via /landscape) | "competitive landscape", "the works on X", "map the field and tell us what's coming and what we should prep" |
| The competitor **set** itself | **competitor-discovery** | "who else is in this space", "are we missing anyone", "map the field" (alone) |
| Background on **one known entity** or one question | **source-sweep** | "catch me up on X", "what do we know about X", "can we say this", "how has X been covered" |
| A fresh forward calendar: for a space with no client folder, or when a refresh is asked for | **catalyst-timeline** (via /triggers) | "refresh the timeline", "upcoming catalysts in <space>", "news triggers". For a client with a folder, "what's coming" is a read of its calendar (the core plugin's routing), not a run |
| Messaging for **one** upcoming event | **scenario-planning** (via /wargame) | "wargame X", "what do we say if", "prep messaging for" |
| The client's canonical knowledge | **client-profile** → setting the client up (core's suite router) if none exists | "load the X profile", any named client before other work |
| Formatting a finished analysis | **client-deliverable** | "format this for the client", "put this in our template" |

## Tie-breakers

- "Map the field" alone → competitor-discovery. "Map the field **and**…" → landscape-report.
- A named source ("check EDGAR for…") does not change the route; source-sweep decides its own
  routing internally and runs the union of what the question needs.
- A request that names a client but no task → the core plugin's suite router: the client's state
  and its queue (core's routing, A client named).
- When two readings are plausible and lead to materially different work, ask one question;
  never start the multi-stage chain on an ambiguous single-stage request.

## Stage order inside the chain

client-profile → competitor-discovery → **Stop 1: the competitor check** → source-sweep (per
competitor) → catalyst-timeline → scenario-planning → client-deliverable → **Stop 2: one approval**.
Stage skills called by the chain reuse the chain's preflight ledger (see source-sweep Step 2).
