#!/usr/bin/env python3
"""Prepare Dot messages for Luna, or validate and merge its returned decisions."""

import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import json
from pathlib import Path

from combine_sources import dot_records, read_csv, sha256
from merge_classifications import validate


def prepare(dataset, work):
    rows = read_csv(dataset / "dots-conversation-data.csv")
    dot_records(rows)
    packets = []
    for index, row in enumerate(rows):
        packets.append({
            "prompt_id": f"dot:message:{row['row']}", "source_row": row["row"], "prompt_text": row["prompt_text"],
            "preceding_user_messages": [r["prompt_text"][:1000] for r in rows[max(0, index - 2):index]],
            "preceding_visible_reply": rows[index - 1]["last_reply_text"][:2000] if index else "",
            "first_visible_reply_to_this_message": row["first_reply_text"][:1600],
            "last_visible_reply_before_next_message": row["last_reply_text"][:2000],
            "context_note": "Reply intervals are asynchronous; the last reply can be unrelated background work. Classify the actual requested work. An empty prompt may have contained an image absent from this export.",
        })
    work.mkdir(parents=True, exist_ok=True)
    workers = []
    size = (len(packets) + 2) // 3
    for worker, low in enumerate(range(0, len(packets), size), 1):
        subset = packets[low:low + size]
        path = work / f"worker-{worker}-input.jsonl"
        path.write_text("".join(json.dumps(packet, ensure_ascii=False) + "\n" for packet in subset))
        workers.append({"worker": worker, "input": str(path), "prompts": len(subset)})
    (work / "manifest.json").write_text(json.dumps({
        "source_sha256": sha256(dataset / "dots-conversation-data.csv"), "workers": workers,
    }, indent=2) + "\n")


def merge(dataset, work):
    manifest = json.loads((work / "manifest.json").read_text())
    source = dataset / "dots-conversation-data.csv"
    if sha256(source) != manifest["source_sha256"]:
        raise ValueError("Dot source changed after preparing classification packets")
    rows = dot_records(read_csv(source))
    decisions = {}
    for worker in manifest["workers"]:
        expected = {json.loads(line)["prompt_id"] for line in Path(worker["input"]).read_text().splitlines()}
        received = set()
        for line in (work / f"worker-{worker['worker']}-output.jsonl").read_text().splitlines():
            decision = json.loads(line)
            validate(decision)
            ident = decision["prompt_id"]
            if ident not in expected or ident in decisions:
                raise ValueError(f"Unexpected or repeated Dot decision: {ident}")
            decisions[ident] = decision
            received.add(ident)
        if received != expected:
            raise ValueError(f"Incomplete Dot worker {worker['worker']}")
    if set(decisions) != {row["record_id"] for row in rows}:
        raise ValueError("Dot decisions do not exactly cover the source")
    output = [{
        **decisions[row["record_id"]], "source_row": row["source_record_id"],
        "prompt_preview": " ".join(row["prompt_text"].split())[:180],
        "secondary_categories": ";".join(decisions[row["record_id"]]["secondary_categories"]),
        "classifier_model": "gpt-6-luna",
    } for row in rows]
    target = dataset / "dot-classifications.csv"
    fields = ["prompt_id", "source_row", "prompt_preview", "primary_category", "secondary_categories",
              "confidence", "evidence_basis", "rationale", "classifier_model"]
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(output)
    metadata = {
        "schema_version": 1, "classifier_model": "gpt-6-luna", "reasoning_effort": "low",
        "classified_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "method": "Three Luna workers classify each Dot message using the existing category rubric and supplied conversation context.",
        "source_file": source.name, "source_sha256": sha256(source), "classifications_sha256": sha256(target),
        "rubric": "classification-guide.md", "rubric_sha256": sha256(dataset / "classification-guide.md"),
        "messages": len(rows), "category_counts": dict(Counter(row["primary_category"] for row in output)),
        "confidence_counts": dict(Counter(row["confidence"] for row in output)),
        "mixed_messages": sum(bool(row["secondary_categories"]) for row in output),
        "workers": [{"task_name": f"luna_classify_{w['worker']}", "messages": w["prompts"]} for w in manifest["workers"]],
        "context": {"full_message": True, "preceding_user_messages": 2, "preceding_user_character_limit_each": 1000,
                    "preceding_reply_character_limit": 2000, "current_first_reply_character_limit": 1600,
                    "current_last_reply_character_limit": 2000},
        "review": "Reviewed low-confidence, Other and long-duration cases against prompt/context evidence. Primary categories describe the requested work.",
        "validation": {"exact_source_coverage": True, "unique_ids": True, "valid_decision_schema": True},
    }
    review_path = work / "review-summary.json"
    if review_path.exists():
        metadata["review_evidence"] = json.loads(review_path.read_text())
    (dataset / "dot-classification-metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(json.dumps(metadata["category_counts"], indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "merge"))
    parser.add_argument("--dataset", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--work", type=Path, default=Path(__file__).resolve().parents[2] / "runs/retrospective-dot-classification")
    args = parser.parse_args()
    (prepare if args.action == "prepare" else merge)(args.dataset, args.work)
