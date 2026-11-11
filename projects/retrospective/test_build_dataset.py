"""Check timing boundaries and the two log formats without keeping real transcripts."""

from datetime import datetime, timezone
import json
from pathlib import Path
import tempfile
import unittest

from build_dataset import collect_turns, read_events, timing_row


class TimingTests(unittest.TestCase):
    def start(self, turn="t", time="2026-11-01T00:00:00.000Z", line=1):
        return (line, time, {"type": "task_started", "turn_id": turn, "root_turn_id": turn})

    def user(self, ident, turn="t", time="2026-11-01T00:00:01.000Z", line=2, paginated=False):
        if paginated:
            payload = {"type": "item_completed", "turn_id": turn, "item": {
                "type": "UserMessage", "client_id": ident, "content": [{"type": "text", "text": ident}]}}
        else:
            payload = {"type": "user_message", "client_id": ident, "message": ident}
        return (line, time, payload)

    def row(self, turn):
        return timing_row({"id": "c", "title": "Example", "archived": 0}, "t", turn,
                          "2026-11-01T00:00:05.000Z", "sessions/example.jsonl")

    def test_steers_and_duplicate_representation_do_not_start_rows(self):
        turns, duplicates = collect_turns([
            self.start(), self.user("initial"), self.user("initial", paginated=True),
            self.user("steer", time="2026-11-01T00:00:03.000Z", paginated=True),
            (5, "2026-11-01T00:00:10.000Z", {"type": "task_complete", "turn_id": "t", "duration_ms": 10200}),
        ])
        row = self.row(turns["t"])
        self.assertEqual((duplicates, len(turns), row["steer_count"]), (1, 1, 1))
        self.assertEqual((row["duration_seconds"], row["prompt_to_end_seconds"]), (10.2, 9.0))
        self.assertEqual(row["duration_source"], "reported_duration_ms")

    def test_interrupt_retry_and_failure_are_separate_turns(self):
        turns, _ = collect_turns([
            self.start(), self.user("initial"),
            (3, "2026-11-01T00:00:02.000Z", {"type": "turn_aborted", "turn_id": "t", "reason": "interrupted"}),
            self.start("retry", "2026-11-01T00:01:00.000Z", 4),
            self.user("retry", time="2026-11-01T00:01:01.000Z", line=5),
            (6, "2026-11-01T00:01:02.000Z", {"type": "task_complete", "turn_id": "retry", "error": {"message": "Unavailable"}}),
        ])
        self.assertEqual(self.row(turns["t"])["status"], "interrupted")
        self.assertEqual(self.row(turns["t"])["duration_seconds"], 2.0)
        self.assertEqual(self.row(turns["retry"])["status"], "failed")
        self.assertEqual(self.row(turns["retry"])["error_message"], "Unavailable")

    def test_missing_end_does_not_become_zero_or_completed(self):
        turns, _ = collect_turns([self.start(), self.user("initial")])
        row = self.row(turns["t"])
        self.assertEqual((row["status"], row["duration_seconds"], row["ended_at_utc"]), ("open", "", ""))
        self.assertEqual(row["observed_seconds"], 5.0)

    def test_snapshot_ignores_later_and_partial_records(self):
        events = [self.start(), self.user("initial")]
        lines = [json.dumps({"timestamp": at, **({"ordinal": i} if i else {}),
                             "type": "event_msg", "payload": payload}).encode() + b"\n"
                 for i, (_, at, payload) in enumerate(events)]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "log.jsonl"
            path.write_bytes(b"".join(lines))
            cutoff = datetime(2026, 11, 1, 0, 0, 0, 500000, tzinfo=timezone.utc)
            selected, _ = read_events(path, path.stat().st_size, cutoff)
            self.assertEqual(len(selected), 1)
            selected, _ = read_events(path, len(lines[0]) + 10, datetime(2027, 1, 1, tzinfo=timezone.utc))
            self.assertEqual(len(selected), 1)


if __name__ == "__main__":
    unittest.main()
