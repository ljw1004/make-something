#!/usr/bin/env python3
"""Validate Luna's per-prompt decisions and retain a keyed classification dataset."""

import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


CATEGORIES = ("art", "story", "game-engine", "other")
DECISION_FIELDS = {"prompt_id", "primary_category", "secondary_categories", "confidence", "evidence_basis", "rationale"}
OUTPUT_FIELDS = ["prompt_id", "conversation_id", "turn_id", "prompt_preview", "primary_category",
                 "secondary_categories", "confidence", "evidence_basis", "rationale", "classifier_model"]
MODEL = "gpt-6-luna"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(decision):
    if set(decision) != DECISION_FIELDS:
        raise ValueError(f"Unexpected decision fields: {decision.get('prompt_id')}")
    if decision["primary_category"] not in CATEGORIES:
        raise ValueError(f"Invalid primary category: {decision}")
    secondary = decision["secondary_categories"]
    if not isinstance(secondary, list) or len(secondary) != len(set(secondary)):
        raise ValueError(f"Secondary categories must be a distinct array: {decision}")
    if any(value not in CATEGORIES[:3] or value == decision["primary_category"] for value in secondary):
        raise ValueError(f"Invalid secondary category: {decision}")
    if decision["primary_category"] == "other" and secondary:
        raise ValueError(f"A substantive secondary category requires a substantive primary: {decision}")
    if decision["confidence"] not in ("high", "medium", "low"):
        raise ValueError(f"Invalid confidence: {decision}")
    if decision["evidence_basis"] not in ("prompt", "context", "unclear"):
        raise ValueError(f"Invalid evidence basis: {decision}")
    if not isinstance(decision["rationale"], str) or not 1 <= len(decision["rationale"].strip()) <= 200:
        raise ValueError(f"Invalid rationale length: {decision['prompt_id']}")


def merge(dataset, work):
    source = dataset / "agentic-loops.csv"
    manifest = json.loads((work / "manifest.json").read_text())
    if sha256(source) != manifest["source_sha256"]:
        raise ValueError("Timing dataset changed after the classification packets were prepared")
    with source.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    decisions = {}
    for worker in manifest["workers"]:
        expected = {json.loads(line)["prompt_id"] for line in Path(worker["input"]).read_text().splitlines()}
        path = work / f"worker-{worker['worker']}-output.jsonl"
        received = set()
        for line in path.read_text().splitlines():
            decision = json.loads(line)
            validate(decision)
            ident = decision["prompt_id"]
            if ident not in expected or ident in decisions:
                raise ValueError(f"Unexpected or duplicate prompt ID in {path}: {ident}")
            received.add(ident)
            decisions[ident] = decision
        if received != expected:
            raise ValueError(f"Incomplete worker {worker['worker']}: missing {sorted(expected - received)}")
    if set(decisions) != {row["prompt_id"] for row in rows}:
        raise ValueError("Classifications do not exactly cover the source dataset")
    output = []
    for row in rows:
        decision = decisions[row["prompt_id"]]
        output.append({
            "prompt_id": row["prompt_id"], "conversation_id": row["conversation_id"], "turn_id": row["turn_id"],
            "prompt_preview": " ".join(row["prompt_text"].replace("\\n", " ").split())[:180],
            "primary_category": decision["primary_category"],
            "secondary_categories": ";".join(decision["secondary_categories"]),
            "confidence": decision["confidence"], "evidence_basis": decision["evidence_basis"],
            "rationale": decision["rationale"].strip(), "classifier_model": MODEL,
        })
    target = dataset / "prompt-classifications.csv"
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(output)
    summary = {}
    for category in CATEGORIES:
        group = [row for row in rows if decisions[row["prompt_id"]]["primary_category"] == category]
        summary[category] = {
            "prompts": len(group), "steers": sum(int(row["steer_count"]) for row in group),
            "recorded_duration_hours": sum(float(row["duration_seconds"]) for row in group if row["duration_seconds"]) / 3600,
            "open_turns": sum(row["status"] == "open" for row in group),
        }
    metadata = {
        "schema_version": 1,
        "classified_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "classifier_model": MODEL, "reasoning_effort": "low",
        "method": "Model judgments by three Luna subagents, followed by schema and coverage validation",
        "source_dataset": "agentic-loops.csv", "source_sha256": sha256(source),
        "rubric": "classification-guide.md", "rubric_sha256": sha256(dataset / "classification-guide.md"),
        "classifications_sha256": sha256(target),
        "prompt_count": len(output), "category_summary": summary,
        "confidence_counts": dict(Counter(row["confidence"] for row in output)),
        "evidence_basis_counts": dict(Counter(row["evidence_basis"] for row in output)),
        "mixed_prompt_count": sum(bool(row["secondary_categories"]) for row in output),
        "context": {"full_initial_prompt": True, "conversation_title": True,
                    "preceding_user_messages": 2, "preceding_user_character_limit_each": 700,
                    "preceding_assistant_final_character_limit": 1800,
                    "referenced_plaintext_attachments": True, "attachment_character_limit": 16000},
        "workers": [{"task_name": f"luna_classify_{worker['worker']}", "prompts": worker["prompts"]}
                    for worker in manifest["workers"]],
        "validation": {"unique_prompt_ids": True, "exact_source_coverage": True,
                       "valid_categories_and_flags": True, "source_unchanged": True},
        "limits": ["Categories describe initial requests, not every later action or steer.",
                   "Mixed-loop hours are assigned entirely to the primary category in this summary.",
                   "Confidence labels are model assessments, not calibrated probabilities.",
                   "Context excerpts can be incomplete; prompt previews are for display only."],
    }
    review = work / "review-summary.json"
    if review.exists():
        metadata["review"] = json.loads(review.read_text())
    (dataset / "classification-metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(json.dumps({key: metadata[key] for key in
                      ("prompt_count", "category_summary", "confidence_counts", "mixed_prompt_count")}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--work", type=Path, default=Path(__file__).resolve().parents[2] / "runs/retrospective-classification")
    args = parser.parse_args()
    merge(args.dataset, args.work)
