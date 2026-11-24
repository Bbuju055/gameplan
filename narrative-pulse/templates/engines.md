# Narrative Pulse — engines — {{CLIENT}}

Engines for all clients: Claude (labelled {{ORG_SHORT_NAME}}'s own engine), asked on every run;
OpenAI and Perplexity, asked when they can be reached and otherwise not measured.
Gemini and Google AI Overviews are not measured; the Pulse report says so in one line.

## Engines

| engine | reached via | model (default, override by environment) | label in report |
|---|---|---|---|
| openai | scripts/engine_query.py, Responses API with web search; or pasted by the agency | gpt-5 (`PULSE_OPENAI_MODEL`) | ChatGPT (OpenAI) |
| perplexity | scripts/engine_query.py, Sonar; or pasted by the agency | sonar (`PULSE_PERPLEXITY_MODEL`) | Perplexity |
| claude | fresh subagent on the agency's account, web search only | the session's model | Claude ({{ORG_SHORT_NAME}}'s own engine) |

## Conditions (identical every run; change only with a decisions.md entry)

- The confirmed question and, for Claude, its fixed helper prompt; nothing else. No conversation
  history. One question per call. Account settings may still shape Claude's answers.
- Region US, English.
- Baseline: two passes per question per engine asked automatically. Standing: one pass.
- Pasted answers (ChatGPT, Perplexity, optional at the review): one pass, a new chat per
  question, asked on the agency's own account; personalisation not controlled.

## Ledger history

| run | openai | perplexity | claude | note |
|---|---|---|---|---|
| {{date}} | live / pasted / unavailable (reason) | | | |
