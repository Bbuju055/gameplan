---
name: build-target-list
description: Read the agency's media log live (through reporter-list), filter candidates per segment, score them on weighted dimensions (deterministic arithmetic via scoring.py), dedupe across segments, and run the mandatory pitch-history check. Second stage of the /target chain; fires automatically after analyze-release. Cross-plugin requests route through core's suite-router.
---

# Build Target List

Every message, the notes while it works included, is in plain words, with nothing internal named and nothing said about what was read or checked (the core plugin's `rules/voice.md`). A note while it works is one plain line, or nothing: what is being done or what comes next, in plain words, is fine; it never names anything internal and never gives a count or a result.

Turn the segments plus the agency's own media log into a scored, history-checked candidate ranking. The log is the candidate pool; the archive is the memory.

## Config preflight

Load the suite's org config (the core plugin's `org-config` skill). This skill needs `scoring.weights` and `history_windows_days`; the media log's own settings are reporter-list's.

- reporter-list reports the log is not configured → **the chain stops here, plainly**, with reporter-list's sentence. Name the gap; do not improvise a candidate pool from the web. The stopped reply holds the lines any run opens with when they apply (the not-set-up line, the not-linked line), reporter-list's sentence, and at most one line on the groups the release calls for; it names no reporter.
- No gameplan root, or the archive script missing or failing → proceed, but the pitch-history check becomes a **named gap** stated in the results ("I couldn't check pitch history, so repeat-pitch flags are missing from this list"). Never silently skip it. Each row's pitch-history cell then reads "not checked". With no gameplan root past results cannot be read either, and track record is said as that: "I couldn't check past results, so track record is neutral for everyone.", never "No one here has a recorded result yet".

## Steps, in order

1. **Read the media log** through this plugin's `reporter-list` skill (loaded by name; its Read section), once per run: it returns the normalized rows and the parse-coverage line. **The main log is read-only to this plugin, permanently.**
2. **Keep the parse-coverage line** for the results and the export's summary file.
3. **Filter per segment** — match candidates on beat, geography, and tier *before* scoring. Only survivors get scored.
4. **Score survivors.** Claude assigns each candidate a 0–1 judgment score per dimension; arithmetic runs deterministically through `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/scoring.py" <payload file>` (weights from config, composite, cross-segment dedup, ranking); the payload is a temporary JSON file. Each candidate also carries `match_reason`, one plain-English sentence on why they fit this segment (beat, outlet, geography); the script refuses a candidate without one. If the script is missing or fails, say so and stop: scores are never added up by hand. Dimensions:
   - **beat_alignment** — how closely the reporter's beat matches the story
   - **outlet_fit** — right tier/type of outlet for this news. Outlets listed in `<gameplan root>/media/ai-cited-outlets.md` get a bump *within* this dimension, and so do outlets the client's latest approved Pulse run marks `add` or `keep` in its cited-outlets list (`narrative/runs/<date>/handoffs.md`; `drop` gets none, and nothing is written to either file from here); if `ai-cited-outlets.md` doesn't exist yet, score normally and note it once, quietly. When the operator names cited outlets, add them there, starting from the plugin's `config/ai-cited-outlets.md` the first time. Every outlet that got the bump says so where the operator sees it: in its reporters' match reasons ("an outlet AI engines cite") or in one note that names each such outlet, not only the one an angle uses.
   - **geographic_relevance**, **story_type_match**
   - **track_record** — from the archive's `performance --by reporter`, with `--client` for this client (see campaign-history's "Reading the archive"): has this reporter covered this client, or this vertical for the agency, before? **No outcome data → pass `null`, which scores neutral (0.5), never zero** — early campaigns must not be distorted. This dimension sharpens automatically as /outcomes runs accumulate. Say it once in plain words, about results, not pitches: "No one here has a recorded result yet, so track record is neutral for everyone." Never call a saved list's entries pitches.
5. **Dedupe across segments** — scoring.py keeps the highest score and lists every matching segment.
6. **Check pitch history — mandatory, never skippable** (except as the named gap above). Run the archive's `pitch-history` for every candidate against this client and cross-client, with `--max-days` set to the longest configured window, and bucket the `days_ago` by the configured windows (default 30/60/90 days). Give each candidate's `name` and `outlet` as the log has them. A hit is matched on the reporter's name: `outlet_match: same` is this reporter; `different` is a possible match, flagged with the outlet it was saved under for the operator to judge ("a Rosa Delgado is on the Series B list as Metro Business Journal (Austin)"), never dropped and never stated as certain. A hit under `older` is outside the windows: it carries no flag, and that reporter is "on a list saved 111 days ago, outside the 90 days checked". `same_client` already allows for a short or respelled client name; if the command refuses the name because it fits two saved clients, ask which one. Flags travel with the reporter through every later step, and wherever the results name them: a reporter mentioned among those the filters left out carries every flag too, this client's and other clients'. A saved list doesn't prove anything went out, so word a flag as what it is ("on the Series A list saved today"), never "was pitched" or "a repeat pitch". The one exception is a hit that carries a recorded `outcome`: covered or no coverage means that pitch went out and is said so ("pitched for the Series A 40 days ago, no coverage"), and not pitched is said as that. A reporter with no hit and nothing under `older` is "no pitch on record", never "never pitched". Say any `problems` per campaign-history's rule. **Whenever the check ran, the results carry this line, word for word, flags or no flags:** "This checks lists saved in this project's folder. Pitches made elsewhere won't show." When it could not run, they carry the named gap above instead.

## What the operator sees

Only a brief progress note, one plain line about the work. Full results are presented after discovery runs, with the parse-coverage line in them, so the operator gets one complete picture, once.

## Prohibitions

- Never write to the media log. Not a cell, not a tab, not ever.
- Never score a candidate that failed the segment filter.
- Never compute composites by hand — arithmetic goes through scoring.py.
- Never present a list whose pitch-history status is neither checked nor named as a gap.
