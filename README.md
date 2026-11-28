# Gameplan

Gameplan runs a life-sciences communications firm's client work inside Claude: know the field,
watch the news, pitch the right reporters, and measure what landed, including what AI engines say
about your client and how to fix it. You approve what goes out, once, and it all builds on one
client folder. Say *set up* and a client's name, and Gameplan runs the whole loop for that client
on one go-ahead.

**New here? Start with the [getting-started guide](core/GUIDE.md).**

## One loop

1. **Take on the client.** A client folder built from public sources, with what only the firm knows (all optional).
2. **Know the field.** Competitors, the dates that will make news, and messages for each outcome.
3. **Watch the news.** A daily media brief, reviewed and approved before it becomes a Word file.
4. **Pitch.** A scored reporter list from a press release and the firm's own media list.
5. **Measure.** The coverage a campaign landed, and what AI engines say about the client.

What landed sharpens the next pitch list, what the AI engines get wrong becomes the next pitch
angle, and the client's calendar tells Gameplan what is due next. Everything a person opens is in a folder under the client's own name, with plain names.

## The five plugins

| Plugin | What it does for the firm | Commands |
|---|---|---|
| **core** | Start here: the firm's setup, setting each client up across every plugin on one go-ahead, each client's page of where things stand, and what's due next. | `/today` |
| **competitive-intel** | The client folder, competitor discovery, the calendar of upcoming news, and wargames with ready messages, as a Word landscape. | `/gameplan`, `/landscape`, `/triggers`, `/wargame` |
| **daily-brief** | The daily client media brief and coverage reports, each approved once before it goes out. | `/brief`, `/clips` |
| **media-targeting** | Pitch lists from a press release with an angle per reporter, beat lists, and what a campaign landed. | `/target`, `/media-list`, `/outcomes` |
| **narrative-pulse** | What AI engines say about a client, checked against its approved claims, with what to fix. | `/pulse` |

Install core with any of the others. Every command can also be asked in plain words.

## Requirements

- The Claude desktop app on a paid plan, with a project that has the firm's folder added. The app
  must be open while Gameplan works, because it keeps everything in that folder.
- Optional connectors: Clinical Trials and PubMed (free, for research), and Microsoft 365 or Google
  Drive if the firm's media list lives there.

## Install

In the Claude app: **Customize**, then **Plugins**, then **Add**, then **Add marketplace**, and enter
`Bbuju055/gameplan`. Install core and the other four plugins it lists. On a Team or Enterprise
plan, an owner can do this for everyone under **Organization settings**, then **Plugins & skills**.
If you were sent the plugin files instead, choose **Upload plugin** for each file. Then
follow the [getting-started guide](core/GUIDE.md): say *set us up*, then *set up* and a client's
name, and each morning ask *what's due for our clients?*

## Guides

- [Getting started](core/GUIDE.md): install, the first day, every command.
- [Competitive intel](competitive-intel/GUIDE.md), [Daily brief](daily-brief/GUIDE.md),
  [Media targeting](media-targeting/GUIDE.md), [Narrative Pulse](narrative-pulse/GUIDE.md).

## For Claude Code users

Gameplan also runs in Claude Code. Add it with `/plugin marketplace add Bbuju055/gameplan`, then
`/plugin install core@gameplan` and the same for the others. To work from a copy of this repository
instead, load the plugins for a session with
`claude --plugin-dir core --plugin-dir competitive-intel` (and the others), from a folder that will
hold the firm's work. Claude Code adds what the app can't hold:

- API keys in the environment: `NEWSDATA_API_KEY` (the news feed for briefs), `RADAR_API_BASE` and
  `RADAR_API_TOKEN` (an optional monitoring service), `OPENAI_API_KEY` and `PERPLEXITY_API_KEY`
  (ChatGPT and Perplexity in Narrative Pulse). All are optional; without them each run says what it
  could not reach.
- Python 3 for the scripts.

## What's never stored here

Client folders, the firm's filled settings and finished deliverables stay in the firm's own
folder and are never part of this repository.

## Known limits in 1.2.0

- **The media list is thin on web search alone.** With no news feed or reporter database
  connected, most names rest on one article and few come with a way to reach them. The page says
  so. A connected reporter database or media-monitoring service improves it.
- **In the Claude app, only Claude is measured** for what AI engines say. ChatGPT and Perplexity
  need their own keys, which the app has nowhere to keep.
- **Two runs on the same client can find different things.** The research is a live search, so
  the claims and competitors it finds vary. Everything found is shown for approval before it is
  used.
- **Replies sometimes run longer than they should:** the landscape's approval summary can run a
  sentence long. The short lines shown while a run works can name something internal.
- **The suite keeps its records as files in your folder,** in one folder named `Gameplan memory - DO NOT DELETE`. It is everything Gameplan knows about your clients: back it up with the rest and never delete it. Each client's own folder is the one meant to be opened.
- **In the Claude app, moving a folder from 1.0.0 or 1.1.0 leaves one old folder behind,
  empty.** Gameplan names it when the move is done; delete it yourself.
- **Tried by hand in the Claude app:** installing from the plugin files, moving a folder from
  1.1.0, setting the agency up and setting a client up. Everything after that (the daily brief,
  pitch lists, wargames, timelines, clips and coverage reports) has been checked by automated
  sessions only.

## Names in examples

Every company, person, article and figure in the examples is made up. Names of real
news outlets, data sources and tools appear only to show the kinds of sources Gameplan reads;
nothing here quotes or describes their actual reporting or staff.

## License

MIT, see [LICENSE](LICENSE).
