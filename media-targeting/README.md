# media-targeting

**Pitch the right reporters:** scored lists from a press release, beat lists, and what each campaign
landed. New here? Read [GUIDE.md](GUIDE.md). The [getting-started guide](../core/GUIDE.md) covers the whole suite: install, the first day, every command.

The operator knows exactly one thing: say "pitch this for" the client (or type `/target`) and
paste a press release. Everything else is Claude talking to them in plain English; they never see
JSON or skill names. The client's first media list is built when core sets the client up.

## The loop

```
/target + press release
  → analyze-release      (segments set and said in one sentence; no stop)
  → build-target-list    (media log read live · filter · score · pitch history)
  → discover-reporters   (Pass A: who's writing this · Pass B: who's asking, from
                          the digest inbox + open web; plus any journalist-database connector)
  → pitch-angle-notes    (automatic for the top reporters of each group: the angle to lead
                          with; research cards, never emails)
  → curate-and-archive   (plain-English editing → "use this list", the one stop: one new file in
                          the archive; approved discoveries go where the list keeps
                          new names, through reporter-list)
  → export-list          (the spreadsheet, with an Angle column, in Deliverables/<Client>/Pitch lists/)

/outcomes  (1–2 weeks later)  : confirm what landed, record it, coverage report;
                                feeds the track-record scoring dimension
/media-list <client or topic> : a beat list from scratch: who covers it now, compared with
                                your list, with the names already on that beat checked
ask in plain words           : anything about the archive, or re-export a saved list
```

## Org-agnostic by construction

**Every org-specific fact lives in the suite's `org-config.yaml`** (shipped by the core plugin, filled copy at the gameplan root): firm name,
media log location and column map, pending-review filename, digest mailbox,
branding. Skills read config first and treat any value still
marked `TODO(org)` as a **named gap**: they say what's missing in plain English
and degrade per their SKILL.md. Nothing is guessed, nothing is hardcoded.
To deploy at a new firm: fill that one file, run the setup checklist.

## Layout

```
.claude-plugin/         plugin.json + source-dependencies.json
commands/               /target /outcomes /media-list
skills/                 the ten skills (chain of six, two standalone, media-list-run, and reporter-list, the one reader and writer of the reporter list)
config/                 parsing-rules.md · ai-cited-outlets.md  (org-config.yaml and the untrusted-content rule live in the core plugin)
scripts/archive.py      the campaign archive: plain files in the project's folder, no database
scripts/scoring.py      deterministic composite scoring (judgment stays Claude's)
templates/              target-list spec · coverage-report spec · pending-review columns
```

## Changelog

- **1.1.0**: pitch lists build straight away with an angle per reporter and one stop ("use this
  list"); the quiet-period question is asked once when nothing is recorded; files in
  Deliverables/<Client>/; the media list ends core's set-up job without a pitch-list offer;
  journalist-database connectors are used when present.
- **1.0.0**: first public release.

## Data boundaries (the short version)

- **Media log: read-only, permanently.** No skill writes it, ever.
- **New names never go into the media log.** Approved discoveries (at finalize) and approved
  names from a media list go where the agency's list keeps new names: the separate
  pending-review file or sheet, or the suite's own list when the agency has none. Degrades to a
  for-review CSV in Deliverables if that cannot be written.
- **The archive is files in the project's folder** (`media/archive/`), written only by
  `scripts/archive.py`: one new file per finalized list and per outcomes pass, never changed
  afterwards. It covers lists saved in that folder; pitches made elsewhere won't show, and
  anything kept in an earlier database isn't imported.
- **Never sends anything.** Research and lists, not outreach. No monitoring
  daemons; everything is operator-summoned.
