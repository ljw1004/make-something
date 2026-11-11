#!/usr/bin/env python3
"""Enrich the saved timing snapshot without refreshing its messages or durations."""

import argparse
from collections import defaultdict
import csv
import hashlib
import io
import json
from pathlib import Path

from build_dataset import collect_turns, instant, read_events
from word_counts import AttachmentAudit, WORD_FIELDS, loop_word_counts, word_count_summary


def enrich(dataset, codex_home):
    attachment_audit = AttachmentAudit(dataset / "attachment-audit.json")
    source = dataset / "agentic-loops.csv"
    old_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    with source.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames
        rows = list(reader)
    metadata_path = dataset / "metadata.json"
    metadata = json.loads(metadata_path.read_text())
    classification_path = dataset / "classification-metadata.json"
    provenance = json.loads(classification_path.read_text()) if classification_path.exists() else None
    if provenance:
        if provenance["source_sha256"] != old_hash:
            raise ValueError("Timing dataset differs from the classified snapshot")
        label_hash = hashlib.sha256((dataset / "prompt-classifications.csv").read_bytes()).hexdigest()
        if label_hash != provenance["classifications_sha256"]:
            raise ValueError("Classifications differ from their recorded hash")
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["source_log"]].append(row)
    original = [{key: value for key, value in row.items() if key not in WORD_FIELDS} for row in rows]
    seen_messages = set()
    for relative, group in grouped.items():
        path = codex_home / relative
        events, _ = read_events(path, path.stat().st_size, instant(metadata["captured_at_utc"]))
        turns, _ = collect_turns(events)
        for row in group:
            users = [user for user in turns[row["turn_id"]]["users"]
                     if instant(user["at"]) <= instant(row["last_observed_at_utc"])
                     and (not row["end_line"] or user["line"] <= int(row["end_line"]))]
            if (not users or users[0]["id"] != row["prompt_id"] or users[0]["text"] != row["prompt_text"]
                    or len(users) != int(row["steer_count"]) + 1):
                raise ValueError(f"Source messages do not match the saved loop: {row['prompt_id']}")
            for user in users:
                if user["id"] in seen_messages:
                    raise ValueError(f"Repeated user message across saved loops: {user['id']}")
                seen_messages.add(user["id"])
            row.update(loop_word_counts(users, codex_home, attachment_audit))
    if len(rows) != metadata["initial_prompts"] or len(seen_messages) != metadata["user_messages"]:
        raise ValueError("Recovered message totals differ from the snapshot")
    if original != [{key: value for key, value in row.items() if key not in WORD_FIELDS} for row in rows]:
        raise ValueError("An existing snapshot value changed during enrichment")
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fields + [field for field in WORD_FIELDS if field not in fields])
    writer.writeheader()
    writer.writerows(rows)
    data = buffer.getvalue().encode("utf-8")
    metadata.update(schema_version=3, word_count=word_count_summary(rows, attachment_audit))
    if provenance:
        provenance.setdefault("source_enrichment", {
            "source_before_sha256": old_hash,
            "added_columns": WORD_FIELDS,
            "original_columns_verified_unchanged": True,
        })
        provenance["source_sha256"] = hashlib.sha256(data).hexdigest()
    # All source recovery and validation finish before any snapshot file is replaced.
    source.write_bytes(data)
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n")
    if provenance:
        classification_path.write_text(json.dumps(provenance, indent=2) + "\n")
    print(json.dumps({"loops": len(rows), "messages": len(seen_messages), **metadata["word_count"]}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--codex-home", type=Path, default=Path.home() / ".codex")
    args = parser.parse_args()
    enrich(args.dataset.resolve(), args.codex_home.resolve())
