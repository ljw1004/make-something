#!/usr/bin/env python3
"""Combine source messages and words, retaining only recorded run durations."""

import argparse
from collections import Counter
import csv
from datetime import datetime
import hashlib
import io
import json
import math
from pathlib import Path

from word_counts import count_words


FIELDS = [
    "record_id", "source", "source_record_id", "record_kind", "conversation_id",
    "prompt_at_utc", "prompt_text", "primary_category", "initial_prompt_count",
    "steer_count", "user_message_count", "prompt_word_count", "steer_word_count",
    "total_word_count", "source_prompt_word_count", "duration_seconds", "duration_evidence",
    "status", "source_file", "source_log", "first_visible_reply_utc",
    "seconds_to_first_visible_reply", "last_visible_reply_before_next_prompt_utc",
    "seconds_to_last_visible_reply_before_next_prompt", "timing_note",
]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def instant(value):
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError(f"Timestamp has no timezone: {value}")
    return result


def dot_records(rows):
    """Keep Dot reply intervals as observations, not agentic run durations."""
    if not rows:
        raise ValueError("Dot export has no messages")
    seen = set()
    result = []
    for index, row in enumerate(rows):
        ident = row["row"]
        if not ident or ident in seen:
            raise ValueError(f"Missing or duplicate Dot row ID: {ident}")
        seen.add(ident)
        sent = instant(row["prompt_sent_utc"])
        next_sent = instant(rows[index + 1]["prompt_sent_utc"]) if index + 1 < len(rows) else None
        if next_sent is not None and next_sent <= sent:
            raise ValueError(f"Dot messages are not strictly chronological at row {ident}")
        # A changed export with actual run information needs an explicit import
        # policy; do not silently discard new evidence or confuse it with replies.
        if any(row[key] for key in ("run_duration_seconds", "steer_count_within_run", "steer_word_count_within_run")):
            raise ValueError("Dot now supplies run/steer data; update the import policy")
        replies = []
        for timestamp, seconds in [
            ("first_visible_reply_utc", "seconds_to_first_visible_reply"),
            ("last_visible_reply_before_next_prompt_utc", "seconds_to_last_visible_reply_before_next_prompt"),
        ]:
            if bool(row[timestamp]) != bool(row[seconds]):
                raise ValueError(f"Incomplete Dot reply interval at row {ident}")
            if row[timestamp]:
                reply, interval = instant(row[timestamp]), float(row[seconds])
                if (not math.isfinite(interval) or interval < 0
                        or abs((reply - sent).total_seconds() - interval) > 0.001
                        or (next_sent is not None and reply >= next_sent)):
                    raise ValueError(f"Inconsistent Dot reply interval at row {ident}")
                replies.append(reply)
        if len(replies) not in (0, 2) or (replies and replies[0] > replies[1]):
            raise ValueError(f"Inconsistent first/last Dot replies at row {ident}")
        supplied_words = int(row["prompt_word_count"])
        if supplied_words < 0:
            raise ValueError(f"Negative Dot word count at row {ident}")
        words = count_words(row["prompt_text"])
        record = {key: "" for key in FIELDS}
        record.update(
            record_id=f"dot:message:{ident}", source="dot", source_record_id=ident,
            record_kind="message", prompt_at_utc=row["prompt_sent_utc"], prompt_text=row["prompt_text"],
            user_message_count=1, prompt_word_count=words, total_word_count=words,
            source_prompt_word_count=supplied_words,
            duration_seconds="", duration_evidence="unavailable",
            status="reply_observed" if replies else "unknown", source_file="dots-conversation-data.csv",
            timing_note=row["timing_note"],
        )
        for key in FIELDS:
            if key in row and key not in ("prompt_text", "prompt_word_count", "timing_note"):
                record[key] = row[key]
        result.append(record)
    return result


def codex_records(dataset):
    rows = read_csv(dataset / "agentic-loops.csv")
    metadata = json.loads((dataset / "metadata.json").read_text())
    provenance = json.loads((dataset / "classification-metadata.json").read_text())
    for name, expected in [("agentic-loops.csv", provenance["source_sha256"]),
                           ("prompt-classifications.csv", provenance["classifications_sha256"])]:
        if sha256(dataset / name) != expected:
            raise ValueError(f"Codex snapshot hash mismatch: {name}")
    audit = metadata["word_count"]["attachment_audit"]
    if sha256(dataset / audit["file"]) != audit["sha256"]:
        raise ValueError("Codex attachment audit hash mismatch")
    labels = read_csv(dataset / "prompt-classifications.csv")
    by_id = {row["prompt_id"]: row["primary_category"] for row in labels}
    if len(by_id) != len(labels) or set(by_id) != {row["prompt_id"] for row in rows}:
        raise ValueError("Codex classification coverage mismatch")
    result = []
    for row in rows:
        record = {key: row.get(key, "") for key in FIELDS}
        record.update(
            record_id=f"codex:loop:{row['prompt_id']}", source="codex", source_record_id=row["prompt_id"],
            record_kind="loop", initial_prompt_count=1, user_message_count=1 + int(row["steer_count"]),
            primary_category=by_id[row["prompt_id"]], source_file="agentic-loops.csv",
            duration_evidence=row["duration_source"] or "unavailable",
        )
        steer_words = json.loads(row["steer_word_counts"])
        if (len(steer_words) != int(row["steer_count"])
                or sum(steer_words) != int(row["steer_word_count"])
                or int(row["prompt_word_count"]) + sum(steer_words) != int(row["total_word_count"])):
            raise ValueError(f"Codex word/steer counts do not reconcile: {row['prompt_id']}")
        result.append(record)
    if (len(result) != metadata["initial_prompts"]
            or sum(row["user_message_count"] for row in result) != metadata["user_messages"]
            or sum(int(row["total_word_count"]) for row in result) != metadata["word_count"]["total_words"]):
        raise ValueError("Codex totals do not reconcile")
    return result, metadata


def summarize(rows):
    timed = [row for row in rows if row["duration_seconds"] != ""]
    return {
        "records": len(rows), "record_kinds": dict(Counter(row["record_kind"] for row in rows)),
        "user_messages": sum(int(row["user_message_count"]) for row in rows),
        "human_words": sum(int(row["total_word_count"]) for row in rows),
        "known_initial_prompts": sum(int(row["initial_prompt_count"] or 0) for row in rows),
        "known_steers": sum(int(row["steer_count"] or 0) for row in rows),
        "messages_without_initial_or_steer_classification": sum(
            int(row["user_message_count"]) for row in rows if row["initial_prompt_count"] == ""),
        "records_with_run_duration": len(timed),
        "recorded_duration_hours": sum(float(row["duration_seconds"]) for row in timed) / 3600,
        "messages_with_run_duration": sum(int(row["user_message_count"]) for row in timed),
        "words_with_run_duration": sum(int(row["total_word_count"]) for row in timed),
    }


def load_combined_snapshot(dataset):
    metadata = json.loads((dataset / "combined-metadata.json").read_text())
    if sha256(dataset / metadata["dataset"]) != metadata["dataset_sha256"]:
        raise ValueError("Combined dataset differs from its metadata")
    for name, expected in metadata["input_sha256"].items():
        if sha256(dataset / name) != expected:
            raise ValueError(f"Combined dataset input changed; rerun combine_sources.py: {name}")
    rows = read_csv(dataset / metadata["dataset"])
    if len({row["record_id"] for row in rows}) != len(rows):
        raise ValueError("Combined record IDs are not unique")
    if summarize(rows) != metadata["totals"]:
        raise ValueError("Combined dataset totals do not reconcile")
    return rows, metadata


def combine(dataset):
    codex, metadata = codex_records(dataset)
    dot = dot_records(read_csv(dataset / "dots-conversation-data.csv"))
    classification = json.loads((dataset / "dot-classification-metadata.json").read_text())
    if (classification["source_sha256"] != sha256(dataset / "dots-conversation-data.csv")
            or classification["classifications_sha256"] != sha256(dataset / "dot-classifications.csv")):
        raise ValueError("Dot classifications do not match their source snapshot")
    labels = read_csv(dataset / "dot-classifications.csv")
    by_id = {row["prompt_id"]: row["primary_category"] for row in labels}
    if len(by_id) != len(labels) or set(by_id) != {row["record_id"] for row in dot}:
        raise ValueError("Dot classification coverage mismatch")
    for row in dot:
        row["primary_category"] = by_id[row["record_id"]]
    rows = sorted(codex + dot, key=lambda row: (instant(row["prompt_at_utc"]), row["record_id"]))
    if len({row["record_id"] for row in rows}) != len(rows):
        raise ValueError("Combined record IDs are not unique")
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(rows)
    data = buffer.getvalue().encode("utf-8")
    summary = {
        "schema_version": 1, "dataset": "combined-conversations.csv",
        "dataset_sha256": hashlib.sha256(data).hexdigest(),
        "input_sha256": {name: sha256(dataset / name) for name in (
            "agentic-loops.csv", "metadata.json", "attachment-audit.json",
            "prompt-classifications.csv", "classification-metadata.json",
            "dots-conversation-data.csv", "dot-classifications.csv", "dot-classification-metadata.json")},
        "sources": {
            "codex": {"file": "agentic-loops.csv", "sha256": sha256(dataset / "agentic-loops.csv"),
                      "captured_at_utc": metadata["captured_at_utc"], **summarize(codex)},
            "dot": {"file": "dots-conversation-data.csv", "sha256": sha256(dataset / "dots-conversation-data.csv"),
                    "first_message_at_utc": dot[0]["prompt_at_utc"], "last_message_at_utc": dot[-1]["prompt_at_utc"],
                    "supplied_prompt_words": sum(row["source_prompt_word_count"] for row in dot),
                    "rows_with_recounted_words": sum(row["prompt_word_count"] != row["source_prompt_word_count"] for row in dot),
                    "messages_with_reply_intervals": sum(bool(row["first_visible_reply_utc"]) for row in dot),
                    **summarize(dot)},
        },
        "totals": summarize(rows),
        "word_count_policy": "Existing human-authored-v1 tokenizer; Dot prompt_text trusted as direct human input; supplied counts preserved separately.",
        "duration_policy": {
            "codex": "Recorded task duration from the frozen Codex snapshot.",
            "dot": "No recorded run durations. Visible-reply intervals are retained separately; all Dot messages are excluded from duration charts.",
        },
        "limits": [
            "Rows have mixed grain: a Codex loop includes its steers; a Dot row is one message with unknown initial/steer role.",
            "Use user_message_count for combined message totals; do not count records as initial prompts.",
            "Dot reply intervals can end in unrelated background updates and are not used as run durations. Dot steer counts remain unknown.",
            "Dot conversation IDs, attachment bodies and outcomes are not supplied; conversation totals cannot be combined.",
            "The two sources have different capture cutoffs. Their original snapshots remain unchanged.",
        ],
    }
    (dataset / "combined-conversations.csv").write_bytes(data)
    (dataset / "combined-metadata.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    print(json.dumps(combine(args.dataset)["totals"], indent=2))
