# Hand-offs: what one step passes to the next

A hand-off is a short block of typed lines that one skill writes for the next step of the same
run to read. The skill that writes a block owns its fields. This file owns the rules every block
follows, and the list of blocks. Each producing skill points here.

The suite router's `NEXT` block is not a hand-off: its lines are words for a person, and its
rules are in the router.

## The rules

- **Every field is always written.** An empty one says `none` (`collisions: none`, `- none this
  run`), with the reason when there is one. A missing field cannot be told from a dropped one.
- **A block is written when another step will read it**: a skill or a command's chain called the
  producer, or the producer's own next step needs it. Asked directly by a person, with nothing
  following, the producer writes no block. A block the person attached does not change that: it is
  something to read, not a caller.
- **A block is for the next step, never for a person.** It is not in a message to a person, the
  word "hand-off" and a block's field names are never said (`voice.md`), and it is not in a file
  a person opens. The one exception is in the table: the brief's draft is what its reviewer reads.
- **A block lives inside one run.** A later run, or another plugin, reads the client folder
  instead: the tiered set and the class searched from `competitors.md`, dated events from `calendar.md`, claims from
  `approved-claims.md`. The two blocks saved for another plugin to read are in the table.
- **What a reader needs is in the block.** A reader uses only the block and the files it points
  to, so a basis, a caveat or a gap that is not in the block does not survive the step. When a
  reader needs something a block lacks, the field is added in the producer, never worked around
  in the reader.

## The blocks

| Block | Written by | Read by | Kept |
|---|---|---|---|
| `PROFILE` | any skill that loads a client folder (the client-folder contract defines it) | the skill that called the loader | the run only |
| `HAND-OFF: competitor set` | competitive-intel's competitor-discovery | landscape-report, catalyst-timeline | the run only; the confirmed set and its space definition reach the folder as `competitors.md` |
| `HAND-OFF: <entity name>` | competitive-intel's source-sweep | landscape-report, catalyst-timeline, scenario-planning | the run only |
| `HAND-OFF: catalysts` | competitive-intel's catalyst-timeline | landscape-report, scenario-planning | the run only; its events reach the folder as `calendar.md` |
| `GATHER` | daily-brief's signal-gather | story-curate | the run only |
| `BRIEF DRAFT` | daily-brief's story-curate | brief-run's review, then brief-render; the reviewer reads it as the draft | saved as the brief's draft in the client folder |
| `HAND-OFF: question-set` | narrative-pulse's question-set | pulse-run | the run only |
| `HAND-OFF: engine-query` | narrative-pulse's engine-query | pulse-run, answer-score | the run only |
| `HAND-OFF: scores` | narrative-pulse's answer-score | pulse-run, pulse-render | the run only |
| `HAND-OFF: cited-outlets` | narrative-pulse's pulse-render | media-targeting's media-list-run | saved in the run's `handoffs.md` in the client folder, for another plugin to read |
| `HAND-OFF: names` | narrative-pulse's pulse-render | competitive-intel's competitor-discovery, as candidates to check | saved beside it in `handoffs.md`, for another plugin to read |
