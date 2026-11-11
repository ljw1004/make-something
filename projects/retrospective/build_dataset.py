#!/usr/bin/env python3
"""Export one timing row per user-initiated Codex turn, using local logs read-only."""

import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sqlite3


FIELDS = [
    "conversation_id", "conversation_title", "archived", "turn_id", "root_turn_id",
    "turn_trigger", "prompt_id", "prompt_kind", "prompt_text", "prompt_at_utc",
    "started_at_utc", "ended_at_utc", "status", "duration_seconds", "duration_source",
    "prompt_to_end_seconds", "steer_count", "last_observed_at_utc", "observed_seconds",
    "end_reason", "error_message", "source_log", "start_line", "prompt_line", "end_line",
]
# Only inspect the envelope before decoding: image/tool records can be very large.
ENVELOPE = re.compile(
    rb'^\{"timestamp":\s*"([^"]+)"(?:,\s*"ordinal":\s*\d+)?,\s*"type":\s*"([^"]+)"'
)
EVENT_TYPE = re.compile(rb'"payload":\s*\{"type":\s*"([^"]+)"')


def instant(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def seconds(start, end):
    return round((instant(end) - instant(start)).total_seconds(), 3)


def read_events(path, byte_limit, cutoff):
    """Read a fixed prefix; return lifecycle/user events and the last log timestamp."""
    events = []
    last_observed = None
    with path.open("rb") as handle:
        line_number = 0
        while handle.tell() < byte_limit:
            line = handle.readline()
            line_number += 1
            if handle.tell() > byte_limit or not line.endswith(b"\n"):
                break  # A record still being written at capture time is not evidence.
            envelope = ENVELOPE.match(line[:180])
            if not envelope:
                raise ValueError(f"Unrecognized log envelope: {path}:{line_number}")
            timestamp = envelope[1].decode()
            if instant(timestamp) > cutoff:
                continue
            last_observed = timestamp
            if envelope[2] != b"event_msg":
                continue
            event_type = EVENT_TYPE.search(line[:300])
            if not event_type:
                raise ValueError(f"Unrecognized event: {path}:{line_number}")
            kind = event_type[1]
            if kind == b"item_completed":
                if not re.search(rb'"type":\s*"UserMessage"', line[:900]):
                    continue
            elif kind not in (b"task_started", b"task_complete", b"turn_aborted", b"user_message"):
                continue
            record = json.loads(line)
            events.append((line_number, timestamp, record["payload"]))
    return events, last_observed


def collect_turns(events):
    turns = {}
    current = None
    seen_messages = set()
    duplicate_messages = 0
    for line, timestamp, payload in events:
        kind = payload["type"]
        if kind == "task_started":
            if current is not None and turns[current]["end"] is None:
                raise ValueError(f"New turn before {current} ended; inspect the missing boundary")
            current = payload["turn_id"]
            if current in turns:
                raise ValueError(f"Repeated task_started for {current}; inspect before exporting")
            attribution = payload.get("turn_attribution", {})
            root = payload.get("root_turn_id") or attribution.get("root_turn_id") or current
            if root != current:
                raise ValueError(f"Continuation turn {current} belongs to {root}; inspect grouping")
            turns[current] = {
                "start": timestamp, "start_line": line, "start_payload": payload,
                "root": root, "users": [], "end": None,
            }
        elif kind in ("task_complete", "turn_aborted"):
            turn = turns[payload["turn_id"]]
            if turn["end"] is not None:
                raise ValueError(f"Multiple terminal events for {payload['turn_id']}")
            turn.update(end=timestamp, end_line=line, end_payload=payload)
        else:
            item = payload["item"] if kind == "item_completed" else payload
            client_id = item.get("client_id")
            if not client_id:
                raise ValueError(f"User message lacks a client ID at line {line}")
            if client_id in seen_messages:
                duplicate_messages += 1
                continue
            seen_messages.add(client_id)
            turn_id = payload.get("turn_id", current)
            turn = turns[turn_id]
            if turn["end"] is not None:
                raise ValueError(f"User message after terminal event in {turn_id}")
            text = item.get("message", "") if kind == "user_message" else "\n".join(
                part.get("text", "") for part in item["content"] if part.get("type") == "text"
            )
            turn["users"].append({"id": client_id, "at": timestamp, "text": text, "line": line})
    return turns, duplicate_messages


def timing_row(thread, turn_id, turn, last_observed, source_log):
    prompt = turn["users"][0]
    end = turn["end"]
    terminal = turn.get("end_payload", {})
    error = terminal.get("error")
    status = "open"
    duration = ""
    duration_source = ""
    if end:
        status = "interrupted" if terminal["type"] == "turn_aborted" else "failed" if error else "completed"
        if terminal.get("duration_ms") is not None:
            duration = round(terminal["duration_ms"] / 1000, 3)
            duration_source = "reported_duration_ms"
        else:
            duration = seconds(turn["start"], end)
            duration_source = "event_timestamps"
    observed_end = end or last_observed or prompt["at"]
    row = {
        "conversation_id": thread["id"],
        "conversation_title": " ".join(thread["title"].split())[:160],
        "archived": int(thread["archived"]),
        "turn_id": turn_id,
        "root_turn_id": turn["root"],
        "turn_trigger": turn["start_payload"].get("turn_attribution", {}).get("turn_trigger", ""),
        "prompt_id": prompt["id"],
        "prompt_kind": "question_reply" if prompt["text"].startswith("<send_user_message_question_reply>") else "text",
        "prompt_text": prompt["text"],
        "prompt_at_utc": prompt["at"],
        "started_at_utc": turn["start"],
        "ended_at_utc": end or "",
        "status": status,
        "duration_seconds": duration,
        "duration_source": duration_source,
        "prompt_to_end_seconds": seconds(prompt["at"], end) if end else "",
        "steer_count": len(turn["users"]) - 1,
        "last_observed_at_utc": observed_end,
        "observed_seconds": seconds(turn["start"], observed_end),
        "end_reason": terminal.get("reason", ""),
        "error_message": error.get("message", "") if isinstance(error, dict) else str(error or ""),
        "source_log": source_log,
        "start_line": turn["start_line"],
        "prompt_line": prompt["line"],
        "end_line": turn.get("end_line", ""),
    }
    for field in ("duration_seconds", "prompt_to_end_seconds", "observed_seconds"):
        if row[field] != "" and row[field] < 0:
            raise ValueError(f"Negative {field} in {turn_id}")
    return row


def build(codex_home, repository, output):
    cutoff = datetime.now(timezone.utc)
    state_path = codex_home / "state_5.sqlite"
    with sqlite3.connect(state_path.as_uri() + "?mode=ro", uri=True) as db:
        db.row_factory = sqlite3.Row
        threads = [dict(row) for row in db.execute(
            "SELECT id, title, archived, rollout_path, history_mode FROM threads "
            "WHERE cwd = ? AND source NOT LIKE '%subagent%' ORDER BY created_at, id",
            (str(repository),),
        )]
    # Snapshot sizes before scanning, since the active conversations keep growing.
    sources = [(thread, Path(thread["rollout_path"]), Path(thread["rollout_path"]).stat().st_size)
               for thread in threads]
    rows = []
    excluded = []
    duplicates = 0
    all_prompt_ids = set()
    all_message_ids = set()
    for thread, path, size in sources:
        events, last_observed = read_events(path, size, cutoff)
        turns, duplicate_count = collect_turns(events)
        duplicates += duplicate_count
        source_log = str(path.relative_to(codex_home))
        for turn_id, turn in turns.items():
            if not turn["users"]:
                excluded.append({"conversation_id": thread["id"], "turn_id": turn_id,
                                 "reason": "no_user_message", "source_log": source_log,
                                 "start_line": turn["start_line"]})
                continue
            for message in turn["users"]:
                if message["id"] in all_message_ids:
                    raise ValueError(f"Copied user history across conversations: {message['id']}")
                all_message_ids.add(message["id"])
            row = timing_row(thread, turn_id, turn, last_observed, source_log)
            all_prompt_ids.add(row["prompt_id"])
            rows.append(row)
    rows.sort(key=lambda row: (row["prompt_at_utc"], row["conversation_id"], row["turn_id"]))
    if len(all_prompt_ids) != len(rows):
        raise ValueError("Non-unique initial prompt IDs")
    metadata = {
        "schema_version": 1,
        "captured_at_utc": cutoff.isoformat(timespec="milliseconds").replace("+00:00", "Z"),
        "display_timezone": "America/Los_Angeles",
        "repository": str(repository),
        "codex_home": str(codex_home),
        "selection": "Top-level threads with cwd exactly equal to repository; archived included",
        "conversations": len(threads),
        "conversations_with_rows": len({row["conversation_id"] for row in rows}),
        "archived_conversations": sum(thread["archived"] for thread in threads),
        "initial_prompts": len(rows),
        "steers": sum(row["steer_count"] for row in rows),
        "user_messages": len(all_message_ids),
        "status_counts": {status: sum(row["status"] == status for row in rows)
                          for status in ("completed", "failed", "interrupted", "open")},
        "duration_source_counts": {source: sum(row["duration_source"] == source for row in rows)
                                   for source in ("reported_duration_ms", "event_timestamps", "")},
        "first_prompt_at_utc": rows[0]["prompt_at_utc"] if rows else None,
        "last_prompt_at_utc": rows[-1]["prompt_at_utc"] if rows else None,
        "duplicate_message_events_ignored": duplicates,
        "excluded_turns": excluded,
    }
    output.mkdir(parents=True, exist_ok=True)
    with (output / "agentic-loops.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    (output / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: metadata[key] for key in
                      ("captured_at_utc", "conversations", "initial_prompts", "steers", "status_counts")}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-home", type=Path, default=Path.home() / ".codex")
    parser.add_argument("--repository", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    build(args.codex_home.resolve(), args.repository.resolve(), args.output.resolve())


if __name__ == "__main__":
    main()
