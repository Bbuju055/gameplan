# Media targeting, in five minutes

For account staff. No technical background needed. The [getting-started guide](../core/GUIDE.md)
covers installing Gameplan and the first day.

## What this is

Three jobs. **The media list:** who covers your client's field right now, built when the client
is set up. **The pitch list:** when you have news, paste the release and get the right reporters
for it, ranked from the firm's own media list, each with the reason they fit and the angle to lead
with. **What it landed:** two weeks later, the coverage it won. Each campaign makes the next list
better.

You don't need a pitch list until there's news. After setup, nothing is waiting on you here.

Nothing is ever sent. Media targeting builds lists and reports; you do the pitching.

## Before your first list

Gameplan needs to know where the firm's media list lives. "Set us up" asks: a spreadsheet in
Microsoft 365, a Google Sheet, a file in your project's folder, or no list at all (then your first
media list starts one for you). The first time it reads your list, it shows how it read the columns
and asks you to confirm. Your media list is only ever read, never changed.

## A pitch list

1. **Say *pitch this for* and the client's name, and paste the release** (or attach it, or type
   `/target` and the name). A rough brief works too.
2. **It builds straight away.** Claude says in one sentence which groups of reporters it's building,
   for example "fintech and lending trade press" and "Austin local", and goes on. If nothing is on
   record about a quiet period, it asks once whether the client is in one.
3. **Read the ranked list.** Each reporter has a score, a one-line reason they fit, the angle to lead
   with, and a warning if they are on a list saved in the last three months, for this client or
   another. Reporters found outside your media list are shown separately, never mixed in. If the
   client has an approved AI check, you may also see one angle that corrects something AI engines
   get wrong.
4. **Edit in plain words.** *Drop Omar*, *add Grace*, *drop the regional group*, *lead with the
   hiring angle for Tomas*.
5. **Say *use this list*.** The list is saved and the spreadsheet goes in `Deliverables`, then the
   client's name, then `Pitch lists`; the reply names it. New reporters you approved go to a
   separate file for whoever owns the firm's media list to review.
6. **When the pitches go out, say so** (*the pitches went out to everyone except Tomas*). The
   client's record then shows who was pitched, with which angle.

## What a campaign landed

One to two weeks later, type `/outcomes` and the campaign. Claude looks for the coverage, shows you
what it found to confirm, and builds a Word report for the client in `Deliverables`, then the
client's name, then `Coverage reports`. Gameplan suggests this when you ask what's due. Confirmed results feed the reporters'
track record, so future lists favour the reporters who actually cover the client.

## Who covers a beat

The client's first one is built when the client is set up. To refresh it, or for a topic, type
`/media-list` and a client or topic. Claude finds who has written about it in the last three
months, compares them with your list, and checks the names you already have on that beat: moved,
changed beat, or left. You review it all on one page (*Acme - Media list - 12 Nov 2026*, in the client's
`Deliverables` folder), and only what you approve is added. If a journalist database such as Muck
Rack or Cision is connected in Claude, it's used too.

## Good to know

- **Repeat-pitch warnings only see this folder.** A list saved by someone working in a different
  folder won't show. The getting-started guide explains how a team shares one folder.
- **"No pitch on record" means none saved here,** not "never pitched".
- **Ask anything about past campaigns in plain words:** *who have we pitched for Lumen?*, *what's
  our hit rate with trade press?*
