#!/usr/bin/env python3
"""Deterministic composite scoring for build-target-list.

Judgment is Claude's; arithmetic is this script's. Claude assigns each
candidate a 0-1 score per dimension, then pipes JSON here for weighted
composites, cross-segment dedup, and ranking. Never edit weights here —
they come from the suite's org-config.yaml (core plugin) via the input payload.

Input: the JSON file named as the first argument.
{
  "weights": {"beat_alignment": 0.35, "outlet_fit": 0.20,
              "geographic_relevance": 0.15, "story_type_match": 0.15,
              "track_record": 0.15},
  "candidates": [
    {"reporter_key": "name|outlet", "segment": "Fintech & lending",
     "match_reason": "Covers lending at a national business daily",
     "dimensions": {"beat_alignment": 0.9, "outlet_fit": 0.7,
                    "geographic_relevance": 0.5, "story_type_match": 0.8,
                    "track_record": null}}   // null = no data -> neutral 0.5
  ]
}

stdout:
{"ranked": [{reporter_key, segments: [...], best_segment, score, match_reason,
             dimension_scores, neutral_dimensions: [...]}, ...],
 "checks": {"weight_sum": 1.0, "candidate_count": N, "deduped": M}}

Rules encoded here (mirrors the SKILL.md):
- A null/missing dimension scores NEUTRAL (0.5), never zero — early campaigns
  with no outcome data must not be distorted. Which dimensions were neutral
  is reported per candidate so the skill can say so.
- Cross-segment dedup: a reporter in multiple segments keeps the highest
  composite, with every matching segment listed.
- Weights must sum to 1.0 (tolerance 0.001) or the script refuses to run.
- Every candidate carries a plain-English match_reason, or the script refuses to
  run; a deduped reporter keeps the reason of its best-scoring segment.
"""
import json
import sys

NEUTRAL = 0.5


def main() -> None:
    with open(sys.argv[1], encoding="utf-8") as handle:
        payload = json.load(handle)
    weights = payload["weights"]
    candidates = payload["candidates"]

    weight_sum = sum(weights.values())
    if abs(weight_sum - 1.0) > 0.001:
        raise SystemExit(f"weights sum to {weight_sum}, not 1.0 — fix org-config.yaml")

    scored = []
    for c in candidates:
        reason = c.get("match_reason")
        if not isinstance(reason, str) or not reason.strip():
            raise SystemExit(f"{c['reporter_key']}: no match_reason")
        dims = c.get("dimensions", {})
        resolved, neutral_dims = {}, []
        for dim in weights:
            v = dims.get(dim)
            if v is None:
                v = NEUTRAL
                neutral_dims.append(dim)
            if not (0.0 <= v <= 1.0):
                raise SystemExit(f"{c['reporter_key']}: {dim}={v} out of [0,1]")
            resolved[dim] = v
        composite = sum(weights[d] * resolved[d] for d in weights)
        scored.append({
            "reporter_key": c["reporter_key"],
            "segment": c["segment"],
            "score": round(composite, 4),
            "match_reason": reason.strip(),
            "dimension_scores": resolved,
            "neutral_dimensions": neutral_dims,
        })

    # cross-segment dedup: keep highest score, note all segments
    by_key: dict = {}
    for s in scored:
        k = s["reporter_key"]
        if k not in by_key:
            by_key[k] = {**s, "segments": [s["segment"]], "best_segment": s["segment"]}
        else:
            by_key[k]["segments"].append(s["segment"])
            if s["score"] > by_key[k]["score"]:
                by_key[k].update(score=s["score"], best_segment=s["segment"],
                                 match_reason=s["match_reason"],
                                 dimension_scores=s["dimension_scores"],
                                 neutral_dimensions=s["neutral_dimensions"])
    for v in by_key.values():
        v.pop("segment", None)

    ranked = sorted(by_key.values(), key=lambda x: x["score"], reverse=True)
    json.dump({"ranked": ranked,
               "checks": {"weight_sum": round(weight_sum, 4),
                          "candidate_count": len(candidates),
                          "deduped": len(candidates) - len(ranked)}},
              sys.stdout, indent=2)


if __name__ == "__main__":
    main()
