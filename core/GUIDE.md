# Getting started with Gameplan

Gameplan runs a life-sciences communications firm's client work inside Claude: know the field,
watch the news, pitch the right reporters, and measure what landed, including what AI engines say
about your client and how to fix it. You approve what goes out, once, and it all builds on one
client folder.

This guide is everything you need to start: about ten minutes to read and fifteen to install and
set up, plus the time to set up each client.

**Who it's for.** Client onboarding, the competitor research and the AI-engine checks assume a
biotech or pharma client. The daily brief, reporter lists and coverage reports work for any client.

**About the examples.** Veltrix Bio, Lumen Credit, Orvane, CORAL and the reporters named here are
made up. Use your own clients' names.

## Two words first

- A **plugin** is an add-on for the Claude app. Gameplan is five of them.
- A **connector** links Claude to another service, such as Microsoft 365 or a clinical-trials
  database. You add one under **Customize**, then **Connectors**, and sign in if it asks.

## How it works: one loop

1. **Take on the client.** Gameplan builds a client folder from public sources, then asks you what
   only the firm knows: what the client may and may not say, approved claims, spokespeople.
2. **Know the field.** It finds the competitors, maps the dates that will make news, and drafts
   what to say for each outcome before the news breaks.
3. **Watch the news.** When you ask, it drafts the client's media brief for the day. You review it,
   approve it, and get a Word file to send.
4. **Pitch.** Paste a press release and it builds a scored list of the right reporters from your
   own media list, checked against the lists you saved recently.
5. **Measure.** It finds the coverage a campaign landed, and checks what AI engines such as Claude
   say about the client: what is wrong, why, and what to fix.

Then the loop starts again, smarter. What landed sharpens the next reporter list. What the AI
engines get wrong becomes the next pitch angle. The calendar from step 2 tells Gameplan what is
due next.

You start it once per client: *set up* and the client's name runs the whole loop above, and stops
for you twice. After that, whenever you ask what's due, it suggests the next step for each client and
waits for your yes. It never sends anything to anyone: you do the sending, and nothing it makes
is final until you approve it.

## What you need

- **The Claude desktop app** on a paid Claude plan, on your computer. It has been tested on a Mac.
  Windows hasn't been tested yet. The app must be open while you work: Gameplan keeps everything
  in a folder on your computer.
- **The Gameplan link**, `Bbuju055/gameplan`, which you type into the app when you install (below).
  If your Gameplan contact sent you the five plugin files instead (they end in `.zip`), leave them
  zipped.
- **Optional:** the free Clinical Trials and PubMed connectors (better research), and the
  Microsoft 365 or Google Drive connector if your media list lives there.

Long jobs, such as setting a client up or a competitive landscape, use more of your Claude plan's
usage than a quick question.

## Install (about five minutes)

1. In the Claude app, open **Customize** (in the left sidebar), then **Plugins**.
2. Click **Add**, then **Add marketplace**, and type `Bbuju055/gameplan`.
3. Install core, then the other four plugins it lists.

On a Team or Enterprise plan, an owner can install Gameplan for everyone instead, under
**Organization settings**, then **Plugins & skills**.

If you were sent the five plugin files instead, click **Add**, then **Upload plugin**, once for
each file. To install a newer version later, upload the new file the same way. The app asks
"Replace existing plugin?"; say yes.

## Set up your workspace

1. Make a folder on your computer for the firm's Gameplan work. If colleagues will share it, put
   it in a drive your team already syncs, such as OneDrive or Google Drive, kept on your computer.
2. In the Claude app, create a project, and add that folder to it from your computer.
3. Always work in that project. That is where Gameplan finds your clients.

Your client folders are ordinary files in that folder. Claude reads them to do the work; your
company's Claude plan terms cover what Claude sees.

## Your first day: two steps

**1. Say "set us up".** Claude asks once, in one message: your name (it goes on
everything you approve), the firm's name as it should appear on reports, and where your media
list lives if you keep one. It then says what it saved and what it assumed, such as no logo and
just you; tell it if any of that is wrong. It takes about two minutes, and it ends by
offering to set up your first client.

**2. Set up your first client.** Say *set up* and the client's name, for example *set up Veltrix
Bio* (typing `/gameplan Veltrix Bio` does the same). Claude starts at once. It stops for you twice:

1. **After a few minutes**, one message: what is still to run and how long it takes, the client's
   claims to approve, the competitors it found to check, and whether any of them is a client of
   the firm. One answer covers all three.
2. **At the end**, one message: everything it made, each with the one thing that matters most in
   it, for one approval. Say what to hold or change, or approve it all.

In between it works through every step without asking:

| Step | What you get, in `Deliverables`, then the client's name |
|---|---|
| Client folder | The client's folder, approved under your name with its claims |
| Competitive landscape | *Veltrix Bio - Competitive landscape - 12 Nov 2026 - approved*, a Word file: one page of bullets, then the evidence |
| What Claude says about the client | A page: is the client mentioned, what's wrong, what to fix and where |
| Daily brief | The news watch set up; the first brief comes the first morning you ask for it |
| Media list | *Veltrix Bio - Media list - 12 Nov 2026*, a page |

It never asks what the client can't say, its quiet periods or its spokespeople: tell it any time
and it keeps them.

Say *skip* for any step you don't want now. If it stops partway (you close the app, or your plan's
usage runs out), say *continue setting up Veltrix Bio* and it picks up where it left off.

It ends with **"Veltrix Bio is fully set up"** and what to do from here. Say *where are we with
Veltrix Bio?* at any time for the client's page of where things stand: every step, its file, and
anything still missing.

To practise first, say *set up a made-up client called Acme Bio for practice*. Claude builds an
empty practice folder with no research. To remove it later, delete its folder (inside the `clients`
folder) like any other folder.

## Every day after that

Open the project and say *what's due today?*, or type `/` and pick **Today**. Answer each suggestion
in plain words: *yes*, *no*, *not now*, or *stop suggesting that for Veltrix*.

One catch on day one: until you've said "set us up", *what's due today?* on its own reads as your
personal to-do list, and Gameplan stays out of it. Say *what's due for our clients?* instead, and
Gameplan answers that it isn't set up yet.

## Commands, or plain words

Every job below can be asked in plain words. Commands are shortcuts: type `/`, pick the command from
the list, then type the client's name after it and press Enter (for example, pick **Brief**, then
type *Veltrix*). If you type words straight after the `/` without picking, the list disappears and
Claude reads it as an ordinary message. In the tables below, `/brief Veltrix` means: pick **Brief**,
then type *Veltrix*. To stop a long job, stop it the way you stop any Claude reply, and say
*continue* later.

## The work, step by step

### Know the field

| You want | Type or say | What you get |
|---|---|---|
| The competitive landscape again (set up already did the first) | `/landscape Veltrix Bio` | A Word file in the client's folder under `Deliverables`: one page of bullets (where the client stands, the dates that matter, the biggest risk and opportunity, what to do by when), then the evidence. It stops twice: to confirm the competitors, and to approve the result. |
| Only the dates that will make news | `/triggers` and a company or field | A dated calendar, every date marked by how certain it is. |
| What to say if an event goes either way | `/wargame` and the event | The possible outcomes, with key messages and a holding statement for each, to adapt and approve. |
| A quick background check | *catch me up on Orvane before the call* | A short answer, with its sources. |

### Watch the news

| You want | Type or say | What you get |
|---|---|---|
| Today's media brief | `/brief Veltrix`, or *what's due today?* | A draft to review: drop, reword or add stories in plain words, then say *approved*. You get the Word file in `Deliverables`, then the client's name, then `Daily briefs`; attach it to your email as usual. |
| A coverage report for a period | `/clips Veltrix September` | The coverage, the messages it carried, and which pieces the firm drove (from the pitches you told Claude about), reviewed by you before the Word report is made. |

### Pitch

| You want | Type or say | What you get |
|---|---|---|
| Reporters for a press release | *pitch this for Veltrix* (or `/target Veltrix`) and paste the release | A ranked list, built straight away, with the reason each reporter fits, the angle to lead with, and a warning on anyone on a list saved recently. Change it in plain words, then say *use this list* for the spreadsheet. |
| A fresh list of who covers a topic (set up builds the client's first one) | `/media-list` and a client or topic | Reporters writing about it now, compared with your list, on a page to review. What you approve goes to a separate review file for whoever owns your media list (or into Gameplan's own list, if you have none). |

Your media list can be any spreadsheet with one reporter per row. The first time, Claude says how it
read the columns and asks you to confirm. No list yet is fine: your first media list starts one that
Gameplan keeps in your folder. Gameplan only ever reads your own list; it never changes it.

When the pitches go out, tell Claude (*the pitches went out to everyone except Tomas*) so the
client's record shows them.

### Measure

| You want | Type or say | What you get |
|---|---|---|
| What a campaign landed | `/outcomes` and the campaign, one to two weeks after | The coverage found, confirmed by you, and a report for the client. Every run makes future reporter lists smarter. |
| What AI engines say about the client (set up runs the first check) | `/pulse Veltrix` | Claude's answers to the questions a buyer might ask, checked against what the client has approved, for you to approve, and a page: what is wrong, why, and what to fix (a page on the client's own site to update, another site to ask for a correction, or news the engines haven't caught up with yet). The questions are listed in the page; say *add a question…* or *drop the one about…* to change them. |

In the Claude app only Claude can be asked, so the page is called "What Claude says about" the
client. ChatGPT and Perplexity are measured too when Gameplan runs in Claude Code with their access
keys.

## All eleven commands

| Command | What it does | Or just say |
|---|---|---|
| `/today` | What's due across your clients, or for one | *what's due for our clients?* |
| `/gameplan` | Set a client up across everything, or finish setting one up | *set up Veltrix* |
| `/landscape` | The competitive landscape on its own | *build the landscape for Veltrix* |
| `/triggers` | The dated calendar of upcoming news | *what's coming up in oral GLP-1s?* |
| `/wargame` | Messages for each outcome of one event | *what do we say if CORAL succeeds?* |
| `/brief` | Today's media brief for a client | *run the Veltrix brief* |
| `/clips` | A coverage report for a period | *the coverage report for September* |
| `/target` | Reporters for a press release | *pitch this for Veltrix* |
| `/media-list` | A list of who covers a topic | *who covers obesity drugs?* |
| `/outcomes` | What a campaign landed | *what did the Series B campaign land?* |
| `/pulse` | What AI engines say about a client | *run the pulse for Veltrix* |

You can also ask *what can Gameplan do?* or *which commands are there?* at any time.

## What you can count on

- **Gameplan sends nothing.** Everything it makes is a draft until you approve it, once. Your name
  from setup goes on the approval with the time, so it never asks who you are. When several
  people approve work here, give it their names and it asks once in each conversation who is approving.
- **A claim the client hasn't approved is flagged.** You approve the client's claims once, when
  the client is set up. A ⚠ mark means a message leans on one that isn't approved. Accept it once
  and it is never asked about again; or fix the wording.
- **It doesn't fill gaps with guesses.** A source it couldn't reach is named, and a missing fact
  stays marked as missing.
- **You can change your mind.** Say *not now* or *stop suggesting that*, and it remembers.

## Good to know

- **Where things are saved.** Everything you open is in the `Deliverables` folder inside your
  project's folder, one folder per client, with plain names such as *Veltrix Bio - Competitive
  landscape - 12 Nov 2026*. Word files for the landscape, briefs and coverage reports; spreadsheets
  for pitch lists; pages for the media list, the AI check, and the client's page of where things
  stand. Double-click a page to open it in your browser. Every reply that saves something names it.
  You never need to open the `clients` folder: that is where Gameplan keeps its records.
- **Your own search terms.** Say *also watch "borrowed immunity" for Veltrix* (or *also look at*
  a company) and every search for that client includes it from then on.
- **Services you already use.** If a news-monitoring or journalist database service is connected
  in Claude (under Customize, then Connectors), Gameplan uses it and says so.
- **The app must be open.** Gameplan can only reach your folder while the desktop app is running.
- **An automatic morning check is optional.** Asking what's due each morning is the routine and
  needs no setup. If you'd like drafts started before you arrive, say yes when it is offered at the end of
  setting a client up, or say *set up a morning check*. It runs only while your computer is awake and the app is open.
- **Working as a team.** Each person links their own project to the same synced folder. Everyone
  then sees every client, and repeat-pitch warnings cover the lists anyone has saved there. Have one
  person work on a client at a time.

## When something looks off

| You see | Do this |
|---|---|
| "Your agency's details aren't set up yet" | Say *set us up*. |
| Claude talks about your own calendar or tasks | Say *for our clients*, or type `/` and pick **Today**. |
| "I couldn't reach…" a source | Nothing to fix: it worked with what it had and says what's missing. If a connector would help, it names it. |
| A job stopped partway | Say *continue* in the same conversation. In a new one, say what to continue (*continue setting up Veltrix*). |
| A question you can't answer yet | Say *skip*. Nothing stops for it; the client's page shows it as not given yet. |

## Words you'll see

| Word | Means |
|---|---|
| **Wargame** | Planning what to say for each way an upcoming event could go. |
| **Holding statement** | A short reply prepared in advance, to adapt and approve when news breaks. |
| **Catalyst** | An event that will make news for the client or a competitor, such as trial results or an approval decision. |
| **Beat** | The topic a reporter covers. |
| **Draft** | Not yet approved. |

## More detail

Each part also has a short guide of its own (competitive intel, the daily brief, media targeting and
Narrative Pulse), sent with this one.
