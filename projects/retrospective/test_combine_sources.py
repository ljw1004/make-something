import csv
import json
from pathlib import Path
import tempfile
import unittest

from combine_sources import FIELDS, dot_records, load_combined_snapshot, sha256, summarize


def message(**overrides):
    row = {
        "row": "1", "prompt_sent_utc": "2026-10-26T00:00:00+00:00", "prompt_text": "Please continue",
        "prompt_word_count": "2", "run_duration_seconds": "", "steer_count_within_run": "",
        "steer_word_count_within_run": "", "first_visible_reply_utc": "2026-10-26T00:00:10+00:00",
        "seconds_to_first_visible_reply": "10", "last_visible_reply_before_next_prompt_utc": "2026-10-26T01:00:00+00:00",
        "seconds_to_last_visible_reply_before_next_prompt": "3600", "timing_note": "Observed replies only.",
    }
    row.update(overrides)
    return row


class CombinedSourcesTests(unittest.TestCase):
    def test_changed_source_invalidates_combined_snapshot(self):
        rows = dot_records([message()])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.csv"
            source.write_text("original source")
            combined = root / "combined-conversations.csv"
            with combined.open("w", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(rows)
            metadata = {"dataset": combined.name, "dataset_sha256": sha256(combined),
                        "input_sha256": {source.name: sha256(source)}, "totals": summarize(rows)}
            (root / "combined-metadata.json").write_text(json.dumps(metadata))
            self.assertEqual(len(load_combined_snapshot(root)[0]), 1)
            source.write_text("changed source")
            with self.assertRaisesRegex(ValueError, "input changed"):
                load_combined_snapshot(root)

    def test_last_reply_interval_does_not_supply_run_duration_or_steers(self):
        row = dot_records([message()])[0]
        self.assertEqual(row["seconds_to_last_visible_reply_before_next_prompt"], "3600")
        self.assertEqual(row["duration_seconds"], "")
        self.assertEqual(row["duration_evidence"], "unavailable")
        for field in ("initial_prompt_count", "steer_count", "steer_word_count"):
            self.assertEqual(row[field], "")
        totals = summarize([row])
        self.assertEqual(totals["user_messages"], 1)
        self.assertEqual(totals["messages_without_initial_or_steer_classification"], 1)
        self.assertEqual(totals["records_with_run_duration"], 0)
        self.assertEqual(totals["recorded_duration_hours"], 0)

    def test_missing_replies_stay_untimed(self):
        row = dot_records([message(first_visible_reply_utc="", seconds_to_first_visible_reply="",
                                  last_visible_reply_before_next_prompt_utc="",
                                  seconds_to_last_visible_reply_before_next_prompt="")])[0]
        self.assertEqual(row["duration_seconds"], "")
        self.assertEqual(summarize([row])["records_with_run_duration"], 0)

    def test_empty_message_counts_once_and_supplied_words_are_preserved(self):
        row = dot_records([message(prompt_text="", prompt_word_count="7")])[0]
        self.assertEqual(row["user_message_count"], 1)
        self.assertEqual(row["source_prompt_word_count"], 7)
        self.assertEqual(row["total_word_count"], 0)

    def test_mixed_grain_totals_count_codex_steers_once(self):
        dot = dot_records([message()])[0]
        codex = {**dot, "record_kind": "loop", "source": "codex", "initial_prompt_count": "1",
                 "steer_count": "2", "user_message_count": "3", "total_word_count": "100", "duration_seconds": "60"}
        totals = summarize([codex, dot])
        self.assertEqual((totals["records"], totals["user_messages"], totals["human_words"]), (2, 4, 102))
        self.assertEqual((totals["known_initial_prompts"], totals["known_steers"]), (1, 2))
        self.assertEqual((totals["messages_with_run_duration"], totals["words_with_run_duration"]), (3, 100))
        self.assertAlmostEqual(totals["recorded_duration_hours"], 1 / 60)

    def test_new_execution_evidence_is_not_silently_discarded(self):
        with self.assertRaisesRegex(ValueError, "update the import policy"):
            dot_records([message(run_duration_seconds="180")])
        with self.assertRaisesRegex(ValueError, "update the import policy"):
            dot_records([message(steer_count_within_run="0")])

    def test_bad_or_cross_message_reply_intervals_are_rejected(self):
        for changes in ({"seconds_to_first_visible_reply": "11"},
                        {"first_visible_reply_utc": ""},
                        {"seconds_to_first_visible_reply": "nan"}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                dot_records([message(**changes)])
        with self.assertRaisesRegex(ValueError, "Inconsistent Dot reply"):
            dot_records([message(), message(row="2", prompt_sent_utc="2026-10-26T00:30:00+00:00")])

    def test_duplicate_ids_and_reversed_timestamps_are_rejected(self):
        missing = dict(first_visible_reply_utc="", seconds_to_first_visible_reply="",
                       last_visible_reply_before_next_prompt_utc="", seconds_to_last_visible_reply_before_next_prompt="")
        with self.assertRaisesRegex(ValueError, "duplicate Dot row"):
            dot_records([message(**missing), message(prompt_sent_utc="2026-10-26T02:00:00+00:00", **missing)])
        with self.assertRaisesRegex(ValueError, "not strictly chronological"):
            dot_records([message(**missing), message(row="2", prompt_sent_utc="2026-10-25T23:00:00+00:00", **missing)])


if __name__ == "__main__":
    unittest.main()
