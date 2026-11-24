#!/usr/bin/env python3
"""
scoring.py — Narrative Pulse deterministic scoring.

Counts what can be counted; leaves judgment (accuracy, framing) to the answer-score skill.

  presence        client named? position among the companies named (class questions); the incumbent
                  product is not a company and is not counted in a position
  share of voice  mention counts per entity from the question set's Entities block
  citations       cited domains: wire / editorial / untiered, tier from an optional tiers file
  noise           baseline only: presence flips and share-of-voice spread between pass 1 and 2

Usage
  python scoring.py --answers <answers.jsonl> --question-set <question-set.md>
                    [--tiers <sources.md>] --out <scores-deterministic.md> [--json <path>]

Entities block format (in question-set.md):
  ## Entities
  - client: Veltrix Bio | Veltrix | VLX-401
  - tier1: Orvane Therapeutics | Orvane | OVN-112
  - incumbent: Ozempra
Tiers file: the client folder's monitoring/sources.md; see parse_tiers for the tables it reads.
Standard library only.
"""
import argparse, collections, json, re, sys
from urllib.parse import urlparse

WIRE = {"businesswire.com", "globenewswire.com", "prnewswire.com", "accesswire.com", "newsfilecorp.com",
        "einpresswire.com", "prweb.com"}
SOURCE_HEADERS = ("sources", "source", "domain")
WEB_ADDRESS = re.compile(r"(?<![a-z0-9@.-])(?:[a-z0-9-]+\.)+[a-z]{2,}(?![a-z0-9-])")


def parse_entities(path):
    ents = []  # (name, role, [aliases])
    in_block = False
    for line in open(path, encoding="utf-8"):
        if line.startswith("## "):
            in_block = line.strip().lower() == "## entities"; continue
        if in_block and line.strip().startswith("- ") and ":" in line:
            role, rest = line.strip()[2:].split(":", 1)
            aliases = [a.strip() for a in rest.split("|") if a.strip()]
            if aliases:
                ents.append({"name": aliases[0], "role": role.strip().lower(), "aliases": aliases})
    return ents


def parse_families(path):
    fam, in_q = {}, False
    for line in open(path, encoding="utf-8"):
        if line.startswith("## "):
            in_q = line.strip().lower() == "## questions"; continue
        if in_q and line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 3 and re.match(r"^Q\d{2,}$", cells[0]):
                fam[cells[0]] = cells[1].lower()
    return fam


def parse_tiers(path):
    """domain -> (tier, kind), from a client folder's monitoring/sources.md.

    Three tables are read, each known by its header. A later row replaces an earlier one for the
    same domain, so an override beats a house default:
      | Tier | Sources |         every web address written in the Sources cell gets that tier
      | Source | Tier | Why |    an override row whose Source cell holds a web address
      | domain | tier | kind |   one domain per row
    kind is the row's kind cell when the table has one (editorial/wire/company/blog), else
    'editorial'. A source written by name only gets no entry. Reading stops at the Proposed
    updates heading: nothing from there on is in force.
    """
    tiers = {}
    if not path:
        return tiers
    header = None
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    for line in lines:
        line = line.strip()
        if line.startswith("#"):
            header = None
            if line.lstrip("#").strip().lower() == "proposed updates":
                break
            continue
        if not line.startswith("|"):
            header = None
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if header is None:
            header = [c.lower() for c in cells]
            source_col = next((i for i, h in enumerate(header) if h in SOURCE_HEADERS), None)
            tier_col = header.index("tier") if "tier" in header else None
            kind_col = header.index("kind") if "kind" in header else None
            continue
        if source_col is None or tier_col is None or len(cells) <= max(source_col, tier_col):
            continue
        if not re.match(r"^[0-5]$", cells[tier_col]):
            continue
        kind = cells[kind_col].lower() if kind_col is not None and len(cells) > kind_col and cells[kind_col] else "editorial"
        for d in WEB_ADDRESS.findall(cells[source_col].lower()):
            tiers[d[4:] if d.startswith("www.") else d] = (int(cells[tier_col]), kind)
    return tiers


def kind_of(d, tiers):
    if d in WIRE:
        return "wire"
    if d in tiers:
        return tiers[d][1]
    return "untiered"


def tier_of(d, tiers):
    return tiers[d][0] if d in tiers else None


def domain(url):
    try:
        d = urlparse(url).netloc.lower()
    except Exception:
        return ""
    return d[4:] if d.startswith("www.") else d


def mentions(text, aliases):
    """Count and first position of an entity (case-insensitive, boundary-aware). Each place in the
    text counts once: the longest alias is matched first, so "Merrow Pharma" is not also "Merrow"."""
    count, first, taken = 0, None, []
    for a in sorted(aliases, key=len, reverse=True):
        for m in re.finditer(r"(?<![A-Za-z0-9])" + re.escape(a) + r"(?![A-Za-z0-9])", text, flags=re.I):
            if any(m.start() < end and start < m.end() for start, end in taken):
                continue
            taken.append((m.start(), m.end()))
            count += 1
            first = m.start() if first is None else min(first, m.start())
    return count, first


def skipped_line(header):
    """The line that says which questions were not asked. A run recorded before the field was renamed
    holds ids only, under skipped_unconfirmed, which covered retired questions as well."""
    skipped = header.get("skipped")
    if skipped:
        return "- skipped questions: " + ", ".join("%s (%s)" % (s["qid"], s["reason"]) for s in skipped)
    if header.get("skipped_unconfirmed"):
        return "- skipped questions (not in use or retired): " + ", ".join(header["skipped_unconfirmed"])
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--answers", required=True)
    ap.add_argument("--question-set", required=True)
    ap.add_argument("--tiers")
    ap.add_argument("--out", required=True)
    ap.add_argument("--json")
    args = ap.parse_args()

    ents = parse_entities(args.question_set)
    client = next((e for e in ents if e["role"] == "client"), None)
    if not client:
        sys.exit("question set has no '- client:' line in its ## Entities block")
    incumbents = {e["name"] for e in ents if e["role"] == "incumbent"}
    fam = parse_families(args.question_set)
    tiers = parse_tiers(args.tiers)

    header, answers = None, []
    for line in open(args.answers, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        obj = json.loads(line)
        if obj.get("header"):
            header = obj; continue
        answers.append(obj)

    rows, sov, cites, flags = [], collections.defaultdict(lambda: collections.Counter()), collections.Counter(), []
    cite_engines = collections.defaultdict(set)
    # a site that carried a planted instruction is at tier 0 wherever this run cites it
    flagged_sites = {domain(a.get("manipulation_source") or "") for a in answers if a.get("manipulation_flag")} - {"", None}
    for a in answers:
        if a.get("status") != "ok":
            rows.append({"qid": a["qid"], "engine": a["engine"], "pass": a.get("pass", 1), "family": a.get("family") or fam.get(a["qid"], "?"),
                         "status": a.get("status"), "presence": None, "position": None, "mentions": {}, "domains": []})
            continue
        text = a.get("answer", "")
        family = a.get("family") or fam.get(a["qid"], "?")
        firsts, counts = {}, {}
        for e in ents:
            c, f = mentions(text, e["aliases"])
            counts[e["name"]] = c
            if f is not None:
                firsts[e["name"]] = f
        order = [n for n, _ in sorted(firsts.items(), key=lambda kv: kv[1])]
        present = client["name"] in firsts
        companies = [n for n in order if n not in incumbents]
        position = (companies.index(client["name"]) + 1) if present else None
        for n, c in counts.items():
            if c:
                sov[(family, a["engine"])][n] += c
        doms = []
        flagged_dom = domain(a.get("manipulation_source") or "") if a.get("manipulation_flag") else None
        for u in a.get("citations") or []:
            d = domain(u)
            if not d:
                continue
            kind = kind_of(d, tiers)
            downgrade = d in flagged_sites or (a.get("manipulation_flag") and not flagged_dom)
            tier = 0 if downgrade else tier_of(d, tiers)
            doms.append({"domain": d, "kind": kind, "tier": tier})
            cites[d] += 1
            cite_engines[d].add(a["engine"])
        if a.get("manipulation_flag"):
            flags.append({"qid": a["qid"], "engine": a["engine"], "pass": a.get("pass", 1), "source": a.get("manipulation_source")})
        rows.append({"qid": a["qid"], "engine": a["engine"], "pass": a.get("pass", 1), "family": family, "status": "ok",
                     "presence": present, "position": position, "named_order": order, "mentions": counts, "domains": doms})

    # roll-ups
    class_rows = [r for r in rows if r["family"] == "class" and r["status"] == "ok"]
    presence_rate = collections.defaultdict(lambda: [0, 0])
    for r in class_rows:
        presence_rate[r["engine"]][1] += 1
        if r["presence"]:
            presence_rate[r["engine"]][0] += 1

    noise = {}
    by_key = collections.defaultdict(dict)
    for r in rows:
        if r["status"] == "ok":
            by_key[(r["qid"], r["engine"])][r["pass"]] = r
    for (qid, eng), passes in by_key.items():
        if 1 in passes and 2 in passes:
            p1, p2 = passes[1], passes[2]
            n = noise.setdefault(eng, {"pairs": 0, "presence_flips": 0, "sov_spread": []})
            n["pairs"] += 1
            if p1["presence"] != p2["presence"]:
                n["presence_flips"] += 1
            def share(r):
                tot = sum(r["mentions"].values()) or 1
                return r["mentions"].get(client["name"], 0) / tot
            n["sov_spread"].append(abs(share(p1) - share(p2)))
    for eng, n in noise.items():
        n["sov_spread_mean"] = round(sum(n["sov_spread"]) / len(n["sov_spread"]), 3) if n["sov_spread"] else 0
        del n["sov_spread"]

    # markdown
    L = []
    L.append(f"# Deterministic scores — run {header.get('run') if header else '?'} ({header.get('type') if header else '?'})\n")
    if header:
        L.append("## Engines ledger\n")
        for e, st in header.get("ledger", {}).items():
            L.append(f"- {e}: {st.get('status')}" + (f" ({st.get('reason')})" if st.get("reason") else "") + f" | model {st.get('model')}")
        if skipped_line(header):
            L.append(skipped_line(header))
        L.append("")
    L.append("## Per answer\n")
    L.append("| qid | family | engine | pass | status | client present | position | named (first-mention order) | citations (domain:kind:tier) |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        named = ", ".join(r.get("named_order", [])) if r["status"] == "ok" else ""
        doms = ", ".join(f"{d['domain']}:{d['kind']}:{d['tier'] if d['tier'] is not None else '-'}" for d in r.get("domains", []))
        pres = "" if r["presence"] is None else ("yes" if r["presence"] else "no")
        L.append(f"| {r['qid']} | {r['family']} | {r['engine']} | {r['pass']} | {r['status']} | {pres} | {r['position'] or ''} | {named} | {doms} |")
    L.append("\n## Presence in class questions (client named)\n")
    L.append("| engine | named in | of |")
    L.append("|---|---|---|")
    for e, (k, n) in sorted(presence_rate.items()):
        L.append(f"| {e} | {k} | {n} |")
    if not presence_rate:
        L.append("| (no class answers) | | |")
    L.append("\n## Share of voice (mentions, by family and engine)\n")
    L.append("| family | engine | " + " | ".join(e["name"] for e in ents) + " |")
    L.append("|---|---|" + "---|" * len(ents))
    for (family, eng), c in sorted(sov.items()):
        L.append(f"| {family} | {eng} | " + " | ".join(str(c.get(e["name"], 0)) for e in ents) + " |")
    L.append("\n## Citations\n")
    L.append("| domain | times cited | engines | kind | tier |")
    L.append("|---|---|---|---|---|")
    flagged_domains = {domain(f.get("source") or "") for f in flags}
    for d, n in cites.most_common():
        t = tier_of(d, tiers)
        L.append(f"| {d} | {n} | {', '.join(sorted(cite_engines[d]))} | {kind_of(d, tiers)} | {'0 (flagged)' if d in flagged_domains else (t if t is not None else '-')} |")
    multi = [d for d in cites if len(cite_engines[d]) >= 2]
    editorial_multi = [d for d in multi if kind_of(d, tiers) == "editorial" and d not in flagged_domains]
    L.append(f"\nCited by two or more engines: {', '.join(multi) if multi else 'none'}")
    L.append(f"Of which editorial and unflagged (candidates for the cited-outlets hand-off): {', '.join(editorial_multi) if editorial_multi else 'none'}")
    if flags:
        L.append("\n## Manipulation flags (citation downgraded to tier 0 for this run)\n")
        for f in flags:
            L.append(f"- {f['qid']} {f['engine']} pass {f['pass']}: {f.get('source') or 'source not recorded'}")
    if noise:
        L.append("\n## Noise (pass 1 vs pass 2)\n")
        L.append("| engine | pairs | presence flips | mean share-of-voice spread |")
        L.append("|---|---|---|---|")
        for e, n in sorted(noise.items()):
            L.append(f"| {e} | {n['pairs']} | {n['presence_flips']} | {n['sov_spread_mean']} |")
        L.append("\nMovement smaller than the spread above is 'no change' in any later comparison.")
    L.append("\n_Accuracy and framing are judged by answer-score against the client folder; this file carries only what can be counted._")
    open(args.out, "w", encoding="utf-8").write("\n".join(L) + "\n")
    if args.json:
        json.dump({"header": header, "rows": rows, "presence_rate": presence_rate, "share_of_voice": {f"{k[0]}|{k[1]}": dict(v) for k, v in sov.items()},
                   "citations": {d: {"count": n, "engines": sorted(cite_engines[d])} for d, n in cites.items()},
                   "multi_engine_domains": multi, "editorial_multi_unflagged": editorial_multi, "flags": flags, "noise": noise}, open(args.json, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"scored {len([r for r in rows if r['status']=='ok'])} answers ({len(rows)} lines) -> {args.out}")


if __name__ == "__main__":
    main()
