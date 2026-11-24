#!/usr/bin/env python3
"""
engine_query.py — Narrative Pulse collector for the HTTP engines (OpenAI, Perplexity).

Asks ONLY the questions in use (confirmed: yes, not retired) from a question-set.md, under fixed conditions, and appends one JSON
line per question x engine x pass to answers.jsonl, verbatim. Probes each engine first and writes
the live/unavailable ledger into the run header. Never drops a failure: unavailable engines and
errored calls are recorded as lines with status != "ok".

The Claude engine is NOT handled here (it runs as a fresh subagent in the session; see the
engine-query skill). Keys come from the environment only:
  OPENAI_API_KEY        PULSE_OPENAI_MODEL      (default: gpt-5)
  PERPLEXITY_API_KEY    PULSE_PERPLEXITY_MODEL  (default: sonar)

Usage
  python engine_query.py --question-set <path> --out <answers.jsonl> --run 2026-09-04
                         [--engines openai,perplexity] [--passes 1|2] [--region US] [--dry-run]

Two passes is a baseline and one is a standing run; the header's "type" follows --passes.
An answers file that already holds this run is picked up, not started again: its header stands,
every question, engine and pass that already has a line is left alone, and only the rest are
asked. A file that holds another run (another date or pass count) is refused.

--dry-run performs no network calls: it parses the question set, writes the header with every
engine marked "dry-run", and exits. Use it to check a question set before spending anything.
The header's "ca" names the certificates TLS is verified against. When Python's own store is
empty (a python.org build on macOS before its "Install Certificates" step), the OS bundle is used
instead; verification is never turned off.
Standard library only.
"""
import argparse, datetime, json, os, re, ssl, sys, time, urllib.request, urllib.error

DEFAULTS = {"openai": "gpt-5", "perplexity": "sonar"}
KEY_ENV = {"openai": "OPENAI_API_KEY", "perplexity": "PERPLEXITY_API_KEY"}
TIMEOUT = 90
OS_CA_BUNDLE = "/etc/ssl/cert.pem"


def die(msg, code=2):
    sys.stderr.write(msg.rstrip("\n") + "\n"); sys.exit(code)


def parse_question_set(path):
    """Return (all_rows, confirmed_rows). Rows are dicts with id, family, question, confirmed."""
    rows, in_q = [], False
    for line in open(path, encoding="utf-8"):
        if line.startswith("## "):
            in_q = line.strip().lower() == "## questions"; continue
        if not in_q or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3 or not re.match(r"^Q\d{2,}$", cells[0]):
            continue
        # | id | family | question | source_file | added_on | retired_on | confirmed |
        row = {"qid": cells[0], "family": cells[1].lower(), "question": cells[2],
               "confirmed": (cells[6].lower() == "yes") if len(cells) > 6 else False,
               "retired": bool(cells[5]) if len(cells) > 5 else False}
        rows.append(row)
    confirmed = [r for r in rows if r["confirmed"] and not r["retired"]]
    return rows, confirmed


def ssl_context(make=ssl.create_default_context, exists=os.path.exists):
    """Return (context, what it trusts): Python's default store, else the OS bundle when that is empty."""
    ctx = make()
    if ctx.cert_store_stats()["x509_ca"]:
        return ctx, "python default"
    if exists(OS_CA_BUNDLE):
        return make(cafile=OS_CA_BUNDLE), OS_CA_BUNDLE
    return ctx, "none: Python's store is empty and no OS bundle was found"


SSL_CONTEXT, CA = ssl_context()


def http_json(url, payload, headers):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST",
                                 headers={"Content-Type": "application/json", **headers})
    with urllib.request.urlopen(req, timeout=TIMEOUT, context=SSL_CONTEXT) as resp:
        return json.loads(resp.read().decode("utf-8"))


# ---- engines ---------------------------------------------------------------------------------

def ask_openai(question, model, key):
    body = {"model": model, "input": question, "tools": [{"type": "web_search"}]}
    r = http_json("https://api.openai.com/v1/responses", body, {"Authorization": f"Bearer {key}"})
    text, cites = [], []
    for item in r.get("output", []):
        if item.get("type") != "message":
            continue
        for part in item.get("content", []):
            if part.get("type") == "output_text":
                text.append(part.get("text", ""))
                for a in part.get("annotations", []) or []:
                    if a.get("type") == "url_citation" and a.get("url"):
                        cites.append(a["url"])
    if not text and r.get("output_text"):
        text = [r["output_text"]]
    seen, ordered = set(), []
    for u in cites:
        if u not in seen:
            seen.add(u); ordered.append(u)
    return "\n".join(text).strip(), ordered, r.get("model", model)


def ask_perplexity(question, model, key):
    body = {"model": model, "messages": [{"role": "user", "content": question}]}
    r = http_json("https://api.perplexity.ai/chat/completions", body, {"Authorization": f"Bearer {key}"})
    text = (r.get("choices") or [{}])[0].get("message", {}).get("content", "") or ""
    cites = list(r.get("citations") or [])
    if not cites:
        cites = [s.get("url") for s in (r.get("search_results") or []) if s.get("url")]
    return text.strip(), cites, r.get("model", model)


ASK = {"openai": ask_openai, "perplexity": ask_perplexity}


def probe(engine, model, key):
    """One cheap call. Returns (ok, detail)."""
    try:
        if engine == "openai":
            r = http_json("https://api.openai.com/v1/responses",
                          {"model": model, "input": "Reply with the single word OK.", "max_output_tokens": 16},
                          {"Authorization": f"Bearer {key}"})
            return True, r.get("model", model)
        if engine == "perplexity":
            r = http_json("https://api.perplexity.ai/chat/completions",
                          {"model": model, "messages": [{"role": "user", "content": "Reply with the single word OK."}],
                           "max_tokens": 8},
                          {"Authorization": f"Bearer {key}"})
            return True, r.get("model", model)
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except Exception as e:  # network, timeout, parse
        return False, type(e).__name__
    return False, "unknown engine"


def read_run(path):
    """An existing answers file: (its first header, the (qid, engine, pass) that already have a line)."""
    header, recorded = None, set()
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except ValueError:
                die(f"Line {n} of {path} is damaged, so the run cannot be picked up. Remove that line and run again.")
            if obj.get("header"):
                header = header or obj
            else:
                recorded.add((obj.get("qid"), obj.get("engine"), obj.get("pass")))
    if header is None:
        die(f"{path} has answers but no run header, so the run cannot be picked up.")
    return header, recorded


# ---- main -------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--question-set", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--run", required=True, help="run date, YYYY-MM-DD (folder name)")
    ap.add_argument("--engines", default="openai,perplexity")
    ap.add_argument("--passes", type=int, default=1, choices=[1, 2])
    ap.add_argument("--type", choices=["baseline", "standing"], help="optional; must agree with --passes")
    ap.add_argument("--region", default="US")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    for a in sys.argv[1:]:
        if re.match(r"^(sk-|pplx-)", a):
            die("Refusing to run: an API key was passed as an argument. Keys come from the environment only.")

    run_type = "baseline" if args.passes == 2 else "standing"
    if args.type and args.type != run_type:
        die(f"--type {args.type} does not go with --passes {args.passes}: a baseline has two passes, a standing run one.")

    recorded = set()
    resumed = os.path.exists(args.out) and os.path.getsize(args.out) > 0
    if resumed:
        first, recorded = read_run(args.out)
        if first.get("run") != args.run or first.get("passes") != args.passes:
            die(f"{args.out} holds run {first.get('run')} with {first.get('passes')} pass(es); this is run {args.run} "
                f"with {args.passes}. Nothing was asked.")

    engines = [e.strip().lower() for e in args.engines.split(",") if e.strip()]
    for e in engines:
        if e not in ASK:
            die(f"Unknown engine '{e}'. This script handles: {', '.join(ASK)}. Claude runs in the session.")

    all_rows, confirmed = parse_question_set(args.question_set)
    skipped = [{"qid": r["qid"], "reason": "retired" if r["retired"] else "not in use"}
               for r in all_rows if r not in confirmed]
    if not confirmed:
        die("No questions in use in the question set. Run /pulse on this client first; its first run writes the questions.")

    conditions = {"system_prompt": None, "history": False, "region": args.region, "language": "en",
                  "one_question_per_call": True}
    ledger = {}
    models = {}
    for e in engines:
        model = os.environ.get(f"PULSE_{e.upper()}_MODEL", DEFAULTS[e])
        models[e] = model
        key = os.environ.get(KEY_ENV[e], "").strip()
        if args.dry_run:
            ledger[e] = {"status": "dry-run", "model": model}
        elif not key:
            ledger[e] = {"status": "unavailable", "reason": "no key set", "model": model}
        else:
            ok, detail = probe(e, model, key)
            ledger[e] = {"status": "live" if ok else "unavailable", "model": detail if ok else model,
                         **({} if ok else {"reason": detail})}

    header = {"header": True, "run": args.run, "type": run_type, "passes": args.passes,
              "conditions": conditions, "ledger": ledger, "ca": CA, "skipped": skipped,
              "confirmed_count": len(confirmed), "written_at": datetime.datetime.now(datetime.timezone.utc).isoformat()}

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "a" if resumed else "w", encoding="utf-8") as out:
        if resumed:
            print(f"picking up run {args.run}: {len(recorded)} answers already recorded | confirmed {len(confirmed)}")
        else:
            out.write(json.dumps(header, ensure_ascii=False) + "\n")
            print(f"header written | confirmed {len(confirmed)} | skipped {len(skipped)} {', '.join(s['qid'] for s in skipped)}")
        for e, st in ledger.items():
            print(f"  {e}: {st['status']}" + (f" ({st.get('reason')})" if st.get('reason') else ""))
        if args.dry_run:
            print("dry run: no engine called."); return
        n = 0
        for e in engines:
            if ledger[e]["status"] != "live":
                for r in confirmed:
                    for p in range(1, args.passes + 1):
                        if (r["qid"], e, p) in recorded:
                            continue
                        out.write(json.dumps({"run": args.run, "pass": p, "qid": r["qid"], "family": r["family"],
                                              "question": r["question"], "engine": e, "model": models[e],
                                              "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                                              "answer": "", "citations": [], "status": "unavailable",
                                              "error": ledger[e].get("reason"), "collection": "api"},
                                             ensure_ascii=False) + "\n")
                continue
            key = os.environ[KEY_ENV[e]].strip()
            for p in range(1, args.passes + 1):
                for r in confirmed:
                    if (r["qid"], e, p) in recorded:
                        continue
                    line = {"run": args.run, "pass": p, "qid": r["qid"], "family": r["family"],
                            "question": r["question"], "engine": e, "model": models[e],
                            "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                            "answer": "", "citations": [], "status": "ok", "error": None, "collection": "api"}
                    try:
                        text, cites, model = ASK[e](r["question"], models[e], key)
                        line.update(answer=text, citations=cites, model=model)
                    except urllib.error.HTTPError as ex:
                        line.update(status="error", error=f"HTTP {ex.code}")
                    except Exception as ex:
                        line.update(status="error", error=type(ex).__name__)
                    out.write(json.dumps(line, ensure_ascii=False) + "\n"); out.flush(); n += 1
                    print(f"  {e} pass {p} {r['qid']}: {line['status']}")
                    time.sleep(0.5)
        print(f"done: {n} answers recorded" + (f", {len(recorded)} kept from before" if resumed else "") + f" -> {args.out}")


if __name__ == "__main__":
    main()
