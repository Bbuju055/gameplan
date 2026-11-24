#!/usr/bin/env python3
"""media-targeting's campaign archive: plain files in the gameplan root, no database.

Layout, under <root>/media/archive/:
  lists/<id>.json     one finalized list version
  outcomes/<id>.json  one confirmed /outcomes pass

Files are never changed once written, so a folder kept in a synced drive has no shared file for
two people to overwrite. All counting happens here, never by hand.

Commands (every result is one JSON object on stdout, with "status" and, on reads, "problems"):
  save-list      --root R --today D --payload FILE
  save-outcomes  --root R --today D --list-id ID --payload FILE
  pitch-history  --root R --today D --client NAME --reporters FILE [--max-days 90]
  lists          --root R [--client NAME] [--release TEXT]
  show-list      --root R --list-id ID
  history        --root R [--client NAME] [--reporter TEXT] [--all-versions]
  performance    --root R --by reporter|segment|discovery [--client NAME]

Rules:
- A saved list is not a pitch. The archive knows who was on a list and when it was saved; it
  learns that a reporter was pitched only from a recorded outcome. Nothing it prints calls a
  saved entry "pitched".
- A list that a later list supersedes no longer counts, except an entry on it with a recorded
  outcome. Two people saving the same version from out-of-sync folders are both kept and both
  count, and each names the other under "conflict_with".
- The first recorded outcome for a reporter stands; only "correct": true replaces it.
- An outcome is "covered", "no_coverage" or "not_pitched". Hit rates are covered over covered plus
  no_coverage; a reporter who was not pitched, and one with no outcome yet, are counted apart.
- pitch-history finds a reporter by name and says whether the outlet is the same ("outlet_match"),
  so one outlet written two ways never hides a reporter. A list older than --max-days is returned
  under "older", not dropped.
- --client takes the saved name, its leading words ("Lumen" for "Lumen Credit, Inc.") or the name
  with no spaces, and says what it was read as under "client_matched". A name that fits two saved
  clients is refused with both named.
- A file the archive can't use (unreadable, damaged, a sync tool's copy) is never skipped quietly:
  it is named under "problems" on every read.
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import secrets
import sys
from pathlib import Path
from typing import Any, Callable

ADDED_BY = ("agent", "agent-discovery", "agent-reactive", "operator")
STATUSES = ("covered", "no_coverage", "not_pitched")
SYSTEM_FILES = ("desktop.ini", "thumbs.db")
Json = dict[str, Any]


class ArchiveError(Exception):
    """A refusal or failure the caller reports in plain words; nothing was written."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def normalize_name(name: str) -> str:
    """Lower, drop punctuation and a trailing company suffix: "Lumen Credit, Inc." = "lumen credit"."""
    cleaned = re.sub(r"[.,'\"]", "", name.lower())
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return re.sub(r"\s(inc|llc|ltd|corp|co|plc|gmbh|sa)$", "", cleaned)


def reporter_key(name: str, outlet: str) -> str:
    return f"{normalize_name(name)}|{normalize_name(outlet)}"


def outlet_core(outlet: str) -> str:
    """An outlet without its brackets, a leading "the" and punctuation, for comparing two spellings:
    "The Metro Business Journal (Austin)" = "metro business journal"."""
    cleaned = re.sub(r"\([^)]*\)", " ", outlet.lower())
    cleaned = re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", cleaned)).strip()
    return re.sub(r"^the\s", "", cleaned)


def client_core(name: str) -> str:
    """A client name without its brackets, punctuation and company suffix: "Lumen Credit Inc. (US)" = "lumen credit"."""
    return normalize_name(re.sub(r"\([^)]*\)", " ", name))


def _slug(text: str, limit: int) -> str:
    return re.sub(r"[^\w]+", "-", text).strip("-")[:limit].strip("-") or "untitled"


def _parse_date(value: Any, label: str) -> datetime.date:
    try:
        return datetime.date.fromisoformat(str(value))
    except ValueError as exc:
        raise ArchiveError("bad_date", f"{label} must be YYYY-MM-DD, got {value!r}") from exc


def _archive_dir(root: str) -> Path:
    path = Path(root)
    if not path.is_dir():
        raise ArchiveError("no_root", f"the gameplan root {root!r} is not a folder")
    return path / "media" / "archive"


def _read_payload(path: str) -> Any:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ArchiveError("bad_payload", f"could not read {path}: {exc}") from exc


def _write_new(folder: Path, record: Json) -> None:
    """Write a new file and read it back. No temp-and-rename: a linked folder may refuse a delete."""
    path = folder / f"{record['id']}.json"
    try:
        folder.mkdir(parents=True, exist_ok=True)
        with open(path, "x", encoding="utf-8") as handle:
            json.dump(record, handle, indent=2, sort_keys=True)
        written = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ArchiveError("write_failed", f"could not save {path.name}: {exc}") from exc
    if written != record:
        raise ArchiveError("write_failed", f"{path.name} did not read back as written")


def _new_id(*parts: str) -> str:
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return "--".join([*parts, f"{stamp}-{secrets.token_hex(2)}"])


def _is_date(value: Any) -> bool:
    try:
        datetime.date.fromisoformat(value)
    except (TypeError, ValueError):
        return False
    return True


def _is_list_record(data: Any) -> bool:
    """A file from a synced folder is outside data: check its whole shape before trusting it."""
    if not isinstance(data, dict):
        return False
    client, release, entries = data.get("client"), data.get("release"), data.get("entries")
    return (
        isinstance(data.get("id"), str)
        and isinstance(client, dict) and isinstance(client.get("key"), str) and "display_name" in client
        and isinstance(release, dict) and isinstance(release.get("key"), str) and "title" in release
        and isinstance(data.get("version"), int)
        and isinstance(data.get("supersedes"), list)
        and _is_date(data.get("finalized_on"))
        and isinstance(entries, list)
        and all(
            isinstance(e, dict) and isinstance(e.get("reporter_key"), str)
            and isinstance(e.get("reporter_snapshot"), dict) and "segment" in e and "added_by" in e
            for e in entries
        )
    )


def _is_outcome_record(data: Any) -> bool:
    return (
        isinstance(data, dict)
        and isinstance(data.get("id"), str)
        and isinstance(data.get("list_id"), str)
        and _is_date(data.get("recorded_on"))
        and isinstance(data.get("outcomes"), list)
        and all(isinstance(row, dict) for row in data["outcomes"])
    )


def _load_folder(folder: Path, is_valid: Callable[[Any], bool]) -> tuple[list[Json], list[Json]]:
    records: list[Json] = []
    problems: list[Json] = []
    if not folder.exists():
        return records, problems
    try:
        paths = sorted(folder.iterdir())
    except OSError as exc:
        return records, [{"file": folder.name, "reason": f"the folder could not be read: {exc}"}]
    for path in paths:
        name = path.name
        if name.startswith((".", "~$")) or name.lower() in SYSTEM_FILES:
            continue
        reason = None
        data: Any = None
        if path.suffix != ".json":
            reason = "not an archive file"
        else:
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except OSError as exc:
                reason = f"could not be read, it may not be downloaded to this computer: {exc}"
            except ValueError:
                reason = "damaged or incomplete, it may still be syncing"
        if reason is None and not is_valid(data):
            reason = "damaged or incomplete, it may still be syncing"
        if reason is None and data["id"] != path.stem:
            reason = "a copy made by a sync tool; compare it with the original"
        if reason is None:
            records.append(data)
        else:
            problems.append({"file": name, "reason": reason})
    return records, problems


class Archive:
    """The folder's lists with their outcomes merged in, and every file it could not use."""

    def __init__(self, root: str) -> None:
        base = _archive_dir(root)
        self.exists = base.exists()
        lists, self.problems = _load_folder(base / "lists", _is_list_record)
        self.lists: dict[str, Json] = {item["id"]: item for item in lists}
        self.superseded_by: dict[str, str] = {}
        for item in lists:
            for old in item["supersedes"]:
                self.superseded_by[old] = item["id"]
        passes, more = _load_folder(base / "outcomes", _is_outcome_record)
        self.problems += more
        self.outcomes: dict[str, dict[str, Json]] = {}
        for one_pass in sorted(passes, key=lambda p: (p["recorded_on"], p["id"])):
            self._merge(one_pass)

    def _merge(self, one_pass: Json) -> None:
        item = self.lists.get(one_pass["list_id"])
        file = f"{one_pass['id']}.json"
        if item is None:
            self.problems.append({"file": file, "reason": "outcomes for a list that isn't in this folder"})
            return
        keys = {entry["reporter_key"] for entry in item["entries"]}
        recorded = self.outcomes.setdefault(item["id"], {})
        for row in one_pass["outcomes"]:
            key = row.get("reporter_key")
            if key not in keys:
                self.problems.append({"file": file, "reason": f"outcome for a reporter not on the list: {key}"})
            elif key not in recorded or row.get("correct"):
                recorded[key] = {**row, "recorded_on": one_pass["recorded_on"]}
            elif recorded[key].get("status") != row.get("status"):
                self.problems.append({"file": file, "reason": f"two records disagree about {key}; the first stands"})

    def is_current(self, list_id: str) -> bool:
        return list_id not in self.superseded_by

    def conflict_with(self, item: Json) -> list[str]:
        return sorted(
            other["id"] for other in self.lists.values()
            if other["id"] != item["id"] and self.is_current(other["id"]) and self.is_current(item["id"])
            and other["client"]["key"] == item["client"]["key"]
            and other["release"]["key"] == item["release"]["key"]
        )

    def clients_named(self, asked: str) -> dict[str, str]:
        """The saved clients a name means, as {key: display name}: the same name, or, when none is the
        same, the one whose leading words it gives or whose name it is with the spaces left out. A name
        that fits two saved clients is refused, so nothing is counted for the wrong one."""
        saved = {item["client"]["key"]: item["client"]["display_name"] for item in self.lists.values()}
        cores = {key: client_core(str(name)) for key, name in saved.items()}
        wanted = client_core(asked)
        if not wanted:
            return {}
        same = {key: saved[key] for key, core in cores.items() if core == wanted}
        if same:
            return same
        short = {key: saved[key] for key, core in cores.items()
                 if core.startswith(wanted + " ") or core.replace(" ", "") == wanted.replace(" ", "")}
        if len({cores[key] for key in short}) > 1:
            names = ", ".join(sorted(str(name) for name in short.values()))
            raise ArchiveError("ambiguous_client", f"{asked!r} fits more than one saved client: {names}; say which one")
        return short

    def rows(self, all_versions: bool = False) -> list[Json]:
        """One row per entry on a list that counts, newest first."""
        rows = []
        for item in self.lists.values():
            current = self.is_current(item["id"])
            recorded = self.outcomes.get(item["id"], {})
            for entry in item["entries"]:
                outcome = recorded.get(entry["reporter_key"])
                if not (current or outcome or all_versions):
                    continue
                rows.append({
                    "client": item["client"]["display_name"],
                    "client_key": item["client"]["key"],
                    "release": item["release"]["title"],
                    "news_type": item["release"].get("news_type"),
                    "list_id": item["id"],
                    "version": item["version"],
                    "current": current,
                    "operator": item.get("operator"),
                    "finalized_on": item["finalized_on"],
                    "reporter_key": entry["reporter_key"],
                    "reporter": entry["reporter_snapshot"].get("name"),
                    "outlet": entry["reporter_snapshot"].get("outlet"),
                    "snapshot": entry["reporter_snapshot"],
                    "segment": entry["segment"],
                    "score": entry.get("score"),
                    "added_by": entry["added_by"],
                    "pitch_flags": entry.get("pitch_flags"),
                    "outcome": outcome,
                })
        return sorted(rows, key=lambda r: (r["finalized_on"], r["list_id"]), reverse=True)


def _validate_list(payload: Any) -> None:
    def refuse(message: str) -> None:
        raise ArchiveError("bad_payload", message)

    if not isinstance(payload, dict):
        refuse("the payload must be an object")
    if not (payload.get("client") or {}).get("display_name"):
        refuse("client.display_name is required")
    if not (payload.get("press_release") or {}).get("title"):
        refuse("press_release.title is required")
    for field in ("segments", "entries"):
        if not isinstance(payload.get(field), list) or not payload[field]:
            refuse(f"{field} must be a non-empty list")
    for entry in payload["entries"]:
        snapshot = entry.get("reporter_snapshot") if isinstance(entry, dict) else None
        if not isinstance(snapshot, dict) or not snapshot.get("name") or not entry.get("segment"):
            refuse(f"entry needs reporter_snapshot.name and segment: {entry}")
        if entry.get("added_by") not in ADDED_BY:
            refuse(f"entry added_by must be one of {ADDED_BY}: {entry}")


def save_list(args: argparse.Namespace) -> Json:
    payload = _read_payload(args.payload)
    _validate_list(payload)
    today = _parse_date(args.today, "--today").isoformat()
    archive = Archive(args.root)
    client_key = normalize_name(payload["client"]["display_name"])
    release_key = normalize_name(payload["press_release"]["title"])
    if not client_key or not release_key:
        raise ArchiveError("bad_payload", "the client name and release title need letters or numbers")

    entries = []
    seen = set()
    for entry in payload["entries"]:
        snapshot = entry["reporter_snapshot"]
        key = reporter_key(snapshot["name"], snapshot.get("outlet") or "")
        if key in seen:
            raise ArchiveError("bad_payload", f"{snapshot['name']} is on the list twice; a reporter appears once")
        seen.add(key)
        entries.append({**entry, "reporter_key": key})

    same_release = [
        item for item in archive.lists.values()
        if item["client"]["key"] == client_key and item["release"]["key"] == release_key
    ]
    version = max((item["version"] for item in same_release), default=0) + 1
    supersedes = sorted(item["id"] for item in same_release if archive.is_current(item["id"]))
    record = {
        "id": _new_id(_slug(client_key, 40), _slug(release_key, 50), f"v{version}"),
        "client": {"display_name": payload["client"]["display_name"], "key": client_key},
        "release": {**payload["press_release"], "key": release_key},
        "version": version,
        "supersedes": supersedes,
        "operator": payload.get("operator"),
        "finalized_on": today,
        "segments": payload["segments"],
        "entries": entries,
    }
    _write_new(_archive_dir(args.root) / "lists", record)
    return {"list_id": record["id"], "version": version, "superseded_list_ids": supersedes,
            "entry_count": len(entries), "problems": archive.problems}


def save_outcomes(args: argparse.Namespace) -> Json:
    payload = _read_payload(args.payload)
    today = _parse_date(args.today, "--today").isoformat()
    outcomes = payload.get("outcomes") if isinstance(payload, dict) else None
    if not isinstance(outcomes, list):
        raise ArchiveError("bad_payload", "outcomes must be a list")
    archive = Archive(args.root)
    item = archive.lists.get(args.list_id)
    if item is None:
        raise ArchiveError("list_not_found", f"no list {args.list_id} in this folder")
    if not archive.is_current(item["id"]):
        raise ArchiveError("list_superseded", "a later version of this list exists; record against that one")

    keys = {entry["reporter_key"] for entry in item["entries"]}
    existing = archive.outcomes.get(item["id"], {})
    applied, seen = [], set()
    counts = {"recorded": 0, "corrected": 0, "skipped_already_set": 0}
    for row in outcomes:
        key = row.get("reporter_key") if isinstance(row, dict) else None
        if key not in keys:
            raise ArchiveError("reporter_not_on_list", f"{key} is not on this list; nothing was recorded")
        if key in seen:
            raise ArchiveError("bad_payload", f"{key} appears twice; nothing was recorded")
        seen.add(key)
        if row.get("status") not in STATUSES:
            raise ArchiveError("bad_payload", f"{key}: status must be one of {STATUSES}; nothing was recorded")
        if row.get("date"):
            _parse_date(row["date"], f"{key} date")
        if key not in existing:
            counts["recorded"] += 1
        elif row.get("correct") is True:
            counts["corrected"] += 1
        else:
            counts["skipped_already_set"] += 1
            continue
        applied.append(row)
    if applied:
        record = {"id": _new_id(item["id"], "outcomes"), "list_id": item["id"], "recorded_on": today,
                  "operator": payload.get("operator"), "outcomes": applied}
        _write_new(_archive_dir(args.root) / "outcomes", record)
    return {**counts, "problems": archive.problems}


def pitch_history(args: argparse.Namespace) -> Json:
    reporters = _read_payload(args.reporters)
    if not isinstance(reporters, list) or not all(isinstance(r, dict) and r.get("name") for r in reporters):
        raise ArchiveError("bad_payload", "reporters must be a list of objects with a name and an outlet")
    today = _parse_date(args.today, "--today")
    archive = Archive(args.root)
    # A reporter is matched by name. The outlet is compared and reported, never required: the same
    # outlet written two ways must not hide a reporter, and a different outlet is for a person to judge.
    wanted: dict[str, set[str]] = {}
    for reporter in reporters:
        wanted.setdefault(normalize_name(reporter["name"]), set()).add(outlet_core(reporter.get("outlet") or ""))
    this_client = archive.clients_named(args.client)
    hits: list[Json] = []
    older: list[Json] = []
    for row in archive.rows():
        asked_outlets = wanted.get(row["reporter_key"].split("|")[0])
        if asked_outlets is None:
            continue
        days_ago = (today - _parse_date(row["finalized_on"], "finalized_on")).days
        hit = {
            "reporter_key": row["reporter_key"], "reporter": row["reporter"], "outlet": row["outlet"],
            "outlet_match": "same" if outlet_core(row["outlet"] or "") in asked_outlets else "different",
            "client": row["client"], "same_client": row["client_key"] in this_client,
            "release": row["release"], "saved_on": row["finalized_on"], "days_ago": days_ago,
            "list_id": row["list_id"], "segment": row["segment"],
            "outcome": row["outcome"].get("status") if row["outcome"] else None,
        }
        (hits if days_ago <= args.max_days else older).append(hit)
    return {"checked": sum(len(outlets) for outlets in wanted.values()),
            "reporters_with_history": len({h["reporter_key"] for h in hits}),
            "hits": hits, "older": older, "client_matched": sorted(str(name) for name in this_client.values()),
            "archive_exists": archive.exists, "problems": archive.problems}


def lists(args: argparse.Namespace) -> Json:
    archive = Archive(args.root)
    clients = archive.clients_named(args.client) if args.client else None
    rows = []
    for item in archive.lists.values():
        if clients is not None and item["client"]["key"] not in clients:
            continue
        if args.release and normalize_name(args.release) not in item["release"]["key"]:
            continue
        rows.append({
            "list_id": item["id"], "client": item["client"]["display_name"],
            "release": item["release"]["title"], "version": item["version"],
            "finalized_on": item["finalized_on"], "operator": item.get("operator"),
            "current": archive.is_current(item["id"]),
            "superseded_by": archive.superseded_by.get(item["id"]),
            "conflict_with": archive.conflict_with(item),
            "entry_count": len(item["entries"]),
            "outcomes_recorded": len(archive.outcomes.get(item["id"], {})),
        })
    rows.sort(key=lambda r: (r["finalized_on"], r["version"], r["list_id"]), reverse=True)
    return {"lists": rows, **_matched(clients), "archive_exists": archive.exists, "problems": archive.problems}


def show_list(args: argparse.Namespace) -> Json:
    archive = Archive(args.root)
    item = archive.lists.get(args.list_id)
    if item is None:
        raise ArchiveError("list_not_found", f"no list {args.list_id} in this folder")
    recorded = archive.outcomes.get(item["id"], {})
    entries = [{**entry, "outcome": recorded.get(entry["reporter_key"])} for entry in item["entries"]]
    return {"list": {**item, "entries": entries}, "current": archive.is_current(item["id"]),
            "conflict_with": archive.conflict_with(item), "problems": archive.problems}


def history(args: argparse.Namespace) -> Json:
    archive = Archive(args.root)
    rows = archive.rows(all_versions=args.all_versions)
    clients = archive.clients_named(args.client) if args.client else None
    if clients is not None:
        rows = [r for r in rows if r["client_key"] in clients]
    if args.reporter:
        wanted = normalize_name(args.reporter)
        rows = [r for r in rows if wanted in normalize_name(r["reporter"] or "")]
    return {"rows": rows, **_matched(clients), "archive_exists": archive.exists, "problems": archive.problems}


def _matched(clients: dict[str, str] | None) -> Json:
    """Which saved clients a --client name was read as, when one was given."""
    return {} if clients is None else {"client_matched": sorted(str(name) for name in clients.values())}


def _tally(rows: list[Json]) -> Json:
    def count(status: str) -> int:
        return sum(1 for r in rows if r["outcome"] and r["outcome"].get("status") == status)

    covered, missed, not_pitched = count("covered"), count("no_coverage"), count("not_pitched")
    recorded = covered + missed + not_pitched
    return {"times_listed": len(rows), "outcomes_recorded": recorded, "times_covered": covered,
            "no_coverage": missed, "not_pitched": not_pitched, "not_yet_tracked": len(rows) - recorded,
            "hit_rate": round(covered / (covered + missed), 2) if covered + missed else None}


def _group(rows: list[Json], *fields: str) -> list[list[Json]]:
    groups: dict[tuple[Any, ...], list[Json]] = {}
    for row in rows:
        groups.setdefault(tuple(row[f] for f in fields), []).append(row)
    return list(groups.values())


def performance(args: argparse.Namespace) -> Json:
    archive = Archive(args.root)
    rows = archive.rows()
    clients = archive.clients_named(args.client) if args.client else None
    if clients is not None:
        rows = [r for r in rows if r["client_key"] in clients]
    if args.by == "reporter":
        result = [{"reporter_key": g[0]["reporter_key"], "reporter": g[0]["reporter"], "outlet": g[0]["outlet"],
                   "last_listed": g[0]["finalized_on"], "clients_listed_for": len({r["client_key"] for r in g}),
                   **_tally(g)} for g in _group(rows, "reporter_key")]
    elif args.by == "segment":
        result = [{"client": g[0]["client"], "list_id": g[0]["list_id"], "release": g[0]["release"],
                   "segment": g[0]["segment"], **_tally(g)} for g in _group(rows, "list_id", "segment")]
    else:
        result = [{"added_by": g[0]["added_by"], **_tally(g)} for g in _group(rows, "added_by")]
    return {"by": args.by, "rows": result, **_matched(clients), "archive_exists": archive.exists, "problems": archive.problems}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="media-targeting's campaign archive")
    sub = parser.add_subparsers(dest="command", required=True)

    def command(name: str, handler: Any, *flags: tuple[str, dict[str, Any]]) -> None:
        one = sub.add_parser(name)
        one.add_argument("--root", required=True)
        for flag, options in flags:
            one.add_argument(flag, **options)
        one.set_defaults(handler=handler)

    needed: dict[str, Any] = {"required": True}
    command("save-list", save_list, ("--today", needed), ("--payload", needed))
    command("save-outcomes", save_outcomes, ("--today", needed), ("--list-id", needed), ("--payload", needed))
    command("pitch-history", pitch_history, ("--today", needed), ("--client", needed), ("--reporters", needed),
            ("--max-days", {"type": int, "default": 90}))
    command("lists", lists, ("--client", {}), ("--release", {}))
    command("show-list", show_list, ("--list-id", needed))
    command("history", history, ("--client", {}), ("--reporter", {}), ("--all-versions", {"action": "store_true"}))
    command("performance", performance, ("--by", {"required": True, "choices": ("reporter", "segment", "discovery")}),
            ("--client", {}))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = {"status": "ok", **args.handler(args)}
        code = 0
    except ArchiveError as exc:
        result = {"status": "error", "code": exc.code, "reason": str(exc)}
        code = 1
    print(json.dumps(result, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
