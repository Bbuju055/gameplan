# How to use Competitive Intel: a 10-minute guide

For anyone at the firm using this plugin. It knows the field for a client: who competes, which
dates will make news, and what to say either way. This guide tells you what to expect at each
step so nothing surprises you.

## How it starts

You don't need to start it yourself. When you say *set up* and a client's name (or type
`/gameplan` and the name), Gameplan sets the client up across everything, and the first two steps
are this plugin's: the client folder, then the competitive landscape.

To build the landscape again later, on its own:

```
/landscape <client> [therapeutic space]
```

Example: `/landscape "Veltrix Bio" "oral incretin therapeutics for obesity"`

## The client folder (step 1 of setting a client up)

- The tool drafts everything public sources can establish: positioning, pipeline, a claims
  ledger, voice profile, a starter competitor list.
- **Then one short list of questions only the firm can answer:** what the client can't say,
  quiet periods, spokespeople, retired claims, the firm's relationships with companies in this
  field. Every one is optional. Say *skip* for any you don't know; nothing waits on them and
  nothing warns you about them later. The client's page of where things stand shows what's
  still missing.
- **The claims, approved once.** You see the client's claims in a short list, grouped by whether
  they can be used as is. Approve them in one answer, or name the ones not to. "All" covers only the claims that can
  be used as they are or with their caveat.
- **Then "Approve the Veltrix Bio folder?"** One yes, under your name from setup. That's it.

## The landscape: two stops

**1. Research (automatic).** It checks which data sources this session has (registry, SEC via
EDGAR, PubMed, BioCentury, web, and any research service you've connected) and finds the
competitors. The horizon is 18 months and the depth is full unless you say otherwise.

**2. Stop 1: the competitor check (your highest-value two minutes).**
- You get the competitors in three groups: direct, adjacent, horizon, with **newly found**
  companies highlighted. Finding companies the client doesn't know about is the point.
- In the same message: **is any of these a client of the firm, or a company we work with?** The
  tool can't read the firm's client list, so this one is on you. If we represent one, it's left
  out of the research until someone decides.
- Add, remove or move anyone, or say *looks right*.

**3. The long part (grab a coffee).** Every direct competitor and your client get researched
across registry, filings, literature and press. Then the timeline of every date that will make
news, each marked by how sure it is, and a scenario plan for every high-stakes event: the
possible outcomes, the messages, and a holding statement for each. No questions in between.

**4. Stop 2: approve the landscape.**
- You get page one in the chat and the Word file in the client's own folder, under `Drafts` until you approve it:
  *Veltrix Bio - Competitive landscape - 12 Nov 2026*.
- **Page one is bullets:** where the client stands, the three dates that matter, the biggest risk
  and opportunity, and what to do by when. The evidence follows: competitors, the timeline, the
  scenarios, and the sources and gaps.
- The same message lists what the run adds to the client's folder (new competitors, new dates)
  and any claim the document leans on that isn't approved yet.
- **One answer approves it all:** "Approve as J. Alvarez, accepting those claims?" The approved copy
  is saved with "approved" added to its name; claims you accept are never asked about again.
- **To change something,** say it in plain words. Wording and cuts are applied straight away.
  Changes to facts (add a competitor, disagree with a date, another scenario) go back through
  the research that owns them, so the document stays as verified as the original.

**One thing stops the run on its own:** if the clinical trials registry can't be searched directly, because
the competitor list depends on it. You can retry, add the free Clinical Trials connector, or go
ahead knowing the list may miss companies. Every other missing source is just listed in the
document's sources and gaps.

## The smaller commands (when you don't need everything)

| You want | Use |
|---|---|
| A fresh forward calendar | `/triggers <company or space> [horizon]` |
| The dates already on a client's calendar | ask *what's coming up for Veltrix?* (to rebuild them, say *refresh the timeline*) |
| Just messaging for one event | `/wargame <event> [client]`, or ask *what do we say if CORAL fails?* |
| Quick background on one company | just ask: "catch me up on X before the call" |
| "Who else is working on X?" | just ask; discovery fires on its own |
| Fact-check a sentence before it ships | just ask: "can we say this: …" |
| Look at another company too | *also look at Tavory Bio for Veltrix*: it joins every later search |

Plain language works for all of it; the commands are just the explicit door.

## Reading the output: mini glossary

| Mark | Means |
|---|---|
| **FIRM** | Externally fixed date (PDUFA, conference). Plan on it. |
| **GUIDED** | Company promised a window. Real but slippable; slip history shown alongside. |
| **ESTIMATED** | Derived, not stated. Always a window, never a single date. |
| **SPECULATIVE** | Plausible, unanchored. Watch, don't plan. |
| **LAPSED-GUIDED** | The promised window passed with no news. That silence is a finding. |
| **primary / analysis / company-only** | Who's behind a fact: registry-or-filing / editorial-or-peer-review / the company's own say-so. Company-only never supports an efficacy or "is this good" claim. |
| **⚠ needs-support** | This message rests on a claim that isn't backed up yet. Accept it once, or fix the wording. |
| **INHERITED-RISK** | Competitor-owned event that will change how your client's own data is read. Mitigation must be published BEFORE it, hence the pre-positioning deadline. |
| **Draft for review** | On the copy you're asked to approve. The approved copy names who approved it and when. |

## Things the plugin will refuse to do (on purpose)

- Certify a competitor set as complete when a source was unavailable; it says "N of 4 passes"
  instead.
- Invent a fact to fill a gap; gaps are listed, never papered over.
- Research or plan against a company you've told it the firm works with, until someone decides.
- Mark the landscape approved before someone has seen it.
