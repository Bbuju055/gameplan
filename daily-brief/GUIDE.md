# The Daily Brief, in 10 minutes

For account staff. No technical background needed. (Operators and admins: your section is at
the end.)

## What this is

Each weekday morning, ask what's due and a draft media brief for your client is started (with the
optional morning check set up, it is already there when you arrive): the overnight
and early coverage that matters, sorted into the client's sections, each story with a short
summary and a "Signal" line explaining why it matters to *your* client. You review it the way
you would review a junior colleague's draft (keep, drop, reword, add), say "approved", and
the finished Word file appears, ready to attach to your morning email. Twenty minutes,
most of it judgment.

Nothing goes to a client without you. The system cannot produce the Word file until you
approve, and it keeps a record of every decision you make (that record is how the brief gets
smarter about what you want).

## Your morning

1. **Ask what's due and say yes to the brief** (with the morning check set up, the draft is
   already waiting). It opens with a two-line orientation: what window
   it covers, how many stories per section, and anything it could not check ("Scored mentions and
   alerts weren't available": you will always be told what it did not see).
2. **Read and direct, in plain English.** Examples of things you can say:
   - "Drop story 4, that is old news."
   - "Add the STAT piece from this morning" (paste the link; it will be read and verified
     before it goes in).
   - "Reword the Signal on story 2, we cannot imply we are safer than their drug."
   - "Move the Halden story to Capital Markets."
   A reason for a drop is optional ("old news"), but when you give one, the monthly tuning
   learns from it.
3. **Watch for flags.** A small ⚠ next to a Signal line means it leans on a claim the client
   has not approved for unqualified use. The approval question names them, so one answer
   accepts them (and they're never asked about again), or you fix the wording.
4. **Say "approved."** Your name from setup and the time go on the record, and the Word file is
   saved in `Deliverables`, then the client's name, then `Daily briefs`, named like
   *Acme - Daily brief - 25 Aug 2026*. The reply names it. Attach and send as usual.

## When news breaks mid-day

If radar (an optional external monitoring service) raises an alert, say a competitor drops topline data, you
can be sent an off-cycle addendum draft. If a landscape report already covers that event, the
holding statement drafted in it appears right next to the draft, so you are choosing and approving
words, not writing them from scratch, in the worst hour to be writing from scratch.

## What to type

| You want | Type |
|---|---|
| Today's brief for a client | `/brief Acme` |
| A specific day or range | `/brief Acme 2026-08-22` |
| React to a radar alert | `/brief Acme --alert` |
| The coverage report for a month or quarter | `/clips Acme September` (attach your monitoring export if you have one) |
| Change what it watches, sources, schedule | just ask: "also watch Brantley Bio for Acme", "stop showing me Fierce", "no brief on Fridays" |
| The monthly "make it smarter" pass | nothing to type: it is suggested each month as one short list with one yes, or say "tune Acme's brief" |

## Good to know

- **The brief never rewrites history.** A shipped brief stays exactly as approved, forever.
  Changing a source's ranking affects future briefs only.
- **Boring honesty is a feature.** A story with no real client angle says so in its Signal
  line. If every line sounds important, none is: clients learn to skim.
- **"Also seen" at the bottom of the draft** is everything below the cut. Skim it; if
  something belongs in the brief, say so and it moves up (and the monthly pass learns from
  that).
- **First time on a new client?** It's set up as part of *set up* and the client's name (or the
  first `/brief`). It builds the searches from the client's folder and shows you "here's what
  yesterday's brief would have looked like". One question: anything specific to watch, and keep
  it like this? Weekdays, a draft by 8:00 AM, US holidays off and you as the reviewer are the
  defaults; change any of them by saying so. If the firm already keeps its queries in a
  spreadsheet, hand it over; it imports cleanly.
- **Where it comes from.** In the Claude app the brief is built from web search, which can miss
  stories a paid news feed would catch; it says so once when it's set up. If a news-monitoring
  service such as Meltwater is connected in Claude, the briefs you start use it too.

## For operators and admins

- **Prereq**: the client has a client folder under the gameplan root (built when the client is
  set up). Monitoring files live inside it; the plugin ships no
  client data.
- **Sources**: in the Claude app the brief gathers from web search and says so; it has nowhere
  to keep a key. In Claude Code, two optional sources can be added through environment variables:
  `NEWSDATA_API_KEY` (the paid news feed, which makes coverage complete rather than best-effort)
  and `RADAR_API_BASE` + `RADAR_API_TOKEN` (radar's read-only handoff API, for scored mentions and
  alerts; the client must exist as a brand in radar). Without them, each run names what it missed.
- **Scheduling**: none needed. Each morning, open the project and ask what's due: on a publication
  day it offers each client's brief that hasn't started. For someone who asks for it, the suite's
  optional morning check runs every day (set, when it is created, to the time you name, or 30 minutes
  before the earliest draft-ready time across clients) and starts `/brief <client> --draft-only` for every client with monitoring set up,
  so a new client needs no setup. Each run checks the client's holiday calendar (`monitoring/cadence.md`) and skips
  with a record. The check runs on a machine where the gameplan root is a local or synced
  folder (OneDrive, SharePoint sync, or Google Drive for desktop): scheduled runs use only those
  files, the API keys above and web search, never a connector. The first time the check is set up it
  asks once which time zone to work in.
- **Moving a client from another monitoring tool**: export its query workbook and any strategy
  text, say "set up the brief for <client>" and hand both over. Run `/brief` alongside the old
  tool until the team is happy with it.
