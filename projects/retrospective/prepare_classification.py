#!/usr/bin/env python3
"""Prepare bounded preceding context and balanced Luna work packets from local logs."""

import argparse
from collections import defaultdict
import csv
import hashlib
import json
from pathlib import Path
import re


def excerpt(value, limit):
    if len(value) <= limit:
        return value
    head = limit * 2 // 3
    return value[:head] + "\n[context truncated]\n" + value[-(limit - head):]


def attachments(text, codex_home):
    root = (codex_home / "attachments").resolve()
    evidence = []
    for match in re.finditer(re.escape(str(root)) + r"/[^\r\n]+", text):
        path = Path(match.group(0).strip()).resolve()
        if not path.is_relative_to(root) or path.suffix.lower() not in (".txt", ".md", ".json"):
            continue
        if not path.is_file():
            evidence.append({"path": str(path), "available": False})
            continue
        content = path.read_text(encoding="utf-8")
        evidence.append({"path": str(path), "available": True,
                         "truncated": len(content) > 16000, "text": excerpt(content, 16000)})
    return evidence


def prepare(dataset, codex_home, output, workers):
    source = dataset / "agentic-loops.csv"
    with source.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    conversations = defaultdict(list)
    for row in rows:
        conversations[row["conversation_id"]].append(row)
    packets = []
    for conversation_rows in conversations.values():
        wanted = {row["prompt_id"]: row for row in conversation_rows}
        path = codex_home / conversation_rows[0]["source_log"]
        previous_users = []
        previous_final = ""
        found = set()
        packet = []
        seen = set()
        with path.open("rb") as handle:
            for line in handle:
                prefix = line[:900].replace(b" ", b"")
                if b'"type":"event_msg"' not in prefix[:140]:
                    continue
                if b'"type":"task_complete"' in prefix[:200]:
                    final = json.loads(line)["payload"].get("last_agent_message")
                    if isinstance(final, str) and final:
                        previous_final = final
                    continue
                if not (b'"type":"user_message"' in prefix[:200] or (
                        b'"type":"item_completed"' in prefix[:200] and b'"type":"UserMessage"' in prefix)):
                    continue
                payload = json.loads(line)["payload"]
                item = payload["item"] if payload["type"] == "item_completed" else payload
                ident = item.get("client_id")
                if ident in seen:
                    continue
                seen.add(ident)
                text = item.get("message", "") if payload["type"] == "user_message" else "\n".join(
                    block.get("text", "") for block in item["content"] if block.get("type") == "text")
                if ident in wanted:
                    row = wanted[ident]
                    if row["prompt_text"] != text:
                        raise ValueError(f"Saved prompt differs from source log: {ident}")
                    packet.append({
                        "prompt_id": ident,
                        "conversation_id": row["conversation_id"],
                        "conversation_title": row["conversation_title"],
                        "prompt_text": text,
                        "attachment_texts": attachments(text, codex_home),
                        "preceding_user_messages": [excerpt(value, 700) for value in previous_users[-2:]],
                        "preceding_assistant_final": excerpt(previous_final, 1800),
                    })
                    found.add(ident)
                    if found == set(wanted):
                        break
                previous_users.append(text)
        if found != set(wanted):
            raise ValueError(f"Missing source messages in {path}: {set(wanted) - found}")
        packets.append(packet)
    output.mkdir(parents=True, exist_ok=True)
    assignments = [[] for _ in range(workers)]
    lengths = [0] * workers
    # Keep conversations intact, distributing the largest input packets first.
    for packet in sorted(packets, key=lambda value: len(json.dumps(value)), reverse=True):
        worker = min(range(workers), key=lambda index: lengths[index])
        assignments[worker].extend(packet)
        lengths[worker] += len(json.dumps(packet))
    manifest = {"source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "prompt_count": len(rows), "workers": []}
    for worker, records in enumerate(assignments, 1):
        path = output / f"worker-{worker}-input.jsonl"
        with path.open("w", encoding="utf-8") as handle:
            for record in records:
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        manifest["workers"].append({"worker": worker, "prompts": len(records),
                                    "input_bytes": path.stat().st_size, "input": str(path)})
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--codex-home", type=Path, default=Path.home() / ".codex")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[2] / "runs/retrospective-classification")
    parser.add_argument("--workers", type=int, default=3)
    args = parser.parse_args()
    if args.workers < 1:
        parser.error("--workers must be positive")
    prepare(args.dataset, args.codex_home, args.output, args.workers)
