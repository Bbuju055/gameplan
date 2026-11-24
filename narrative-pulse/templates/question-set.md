# Narrative Pulse — question set — {{CLIENT}}

Status: In use since {{YYYY-MM-DD}}
Class definition (from the {{landscape date}} landscape run): {{indication × mechanism, in the landscape's words}}
Source of competitor tiers: {{landscape run <date> | starter set from onboarding (say so in the report)}}

## Questions

Wording is fixed once a question is in use. To change a question, retire it (fill `retired_on`)
and add a new id; never edit a question in place. `confirmed` means in use: `yes` when the set is
written or a question is added; a dropped question keeps `yes` and gets its `retired_on` date.

| id | family | question | source_file | added_on | retired_on | confirmed |
|---|---|---|---|---|---|---|
| Q01 | direct | {{What is <Client>?}} | positioning.md | {{date}} | | {{yes/no}} |
| Q02 | direct | {{What does <asset> treat and how far along is it?}} | pipeline.md | {{date}} | | |
| Q03 | class | {{Which companies are developing <class>?}} | landscape | {{date}} | | |
| Q04 | class | {{What are the alternatives to <incumbent>?}} | landscape | {{date}} | | |
| Q05 | catalyst | {{What did <Client>'s <trial> show?}} | the calendar | {{date}} | | |

## Framing labels (one per answer; answer-score uses this list only)

- own-positioning — the answer tells the client's own story in substance
- third-party — a competitor's or analyst's framing of the space
- legacy:{{what}} — a superseded story, named
- absent — the client is not mentioned where it should be (class questions)
- {{client-specific label, if any}}

## Entities

One line per entity: role, then canonical name and every alias or asset code, separated by `|`.
Presence and share of voice are counted against these; missing aliases undercount.

- client: {{Client Inc}} | {{Client}} | {{ASSET-1}}
- tier1: {{Competitor A}} | {{alias}} | {{asset code}}
- tier2: {{Competitor B}} | {{alias}}
- incumbent: {{Approved comparator product}}

## Dropped

| id | question | reason (the user's words) |
|---|---|---|
| | | |
