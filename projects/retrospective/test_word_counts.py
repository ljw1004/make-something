"""Check authored text boundaries and enrichment of a frozen timing snapshot."""

from contextlib import redirect_stdout
import csv
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from add_word_counts import enrich
from build_dataset import collect_turns, timing_row
from word_counts import AttachmentAudit, WORD_FIELDS, count_words, loop_word_counts, message_word_count


class WordCountTests(unittest.TestCase):
    def test_words_keep_contractions_and_ignore_punctuation(self):
        self.assertEqual(count_words("Don't re-count naïve words — 42."), 5)
        self.assertEqual(count_words("# Title\n\n**two** words."), 3)
        self.assertEqual(count_words(" --- ** … "), 0)

    def test_clarification_counts_answers_without_questions_or_ids(self):
        reply = '<send_user_message_question_reply>\n' + json.dumps([
            {"questionItemId": "a long generated identifier", "question": "Many words in the question do not count.",
             "answer": "Yes, do that."},
            {"question": "Second question", "answer": ""},
        ]) + '\n</send_user_message_question_reply>'
        self.assertEqual(message_word_count(reply, Path('/unused')), 3)
        fields = loop_word_counts([{"text": "Initial request."}, {"text": reply}, {"text": "One"}], Path('/unused'))
        self.assertEqual(fields["prompt_word_count"], 2)
        self.assertEqual(json.loads(fields["steer_word_counts"]), [3, 1])
        self.assertEqual((fields["steer_word_count"], fields["total_word_count"]), (4, 6))

    def test_pasted_text_counts_full_content_without_preview_or_wrapper(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            attachment = home / 'attachments' / 'example' / 'Pasted text.txt'
            attachment.parent.mkdir(parents=True)
            attachment.write_text('pasted body\nwith five words')
            audit_path = home / 'attachment-audit.json'
            audit_path.write_text(json.dumps({"reviews": [{
                "sha256": hashlib.sha256(attachment.read_bytes()).hexdigest(), "decision": "include",
                "raw_word_count": 5, "counted_word_count": 5,
            }]}))
            audit = AttachmentAudit(audit_path)
            message = (f'# Files pasted by the user:\n\n## "pasted body with five words…": {attachment}\n'
                       '\nPasted text contains the user\'s request.\n\n## My request:\nAlso this.')
            self.assertEqual(message_word_count(message, home, audit), 7)
            attachment.unlink()
            with self.assertRaises(FileNotFoundError):
                message_word_count(message, home, audit)

    def test_attachment_audit_excludes_generated_text_and_selects_human_edits(self):
        mixed = 'Inherited material.\nMy new request.\n'
        generated = b'Generated diagnostic payload 123'
        start = mixed.index('My new request.')
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'attachment-audit.json'
            path.write_text(json.dumps({"reviews": [
                {"sha256": hashlib.sha256(mixed.encode()).hexdigest(), "decision": "partial",
                 "raw_word_count": 5, "counted_word_count": 3,
                 "included_spans": [{"start": start, "end": len(mixed)}]},
                {"sha256": hashlib.sha256(generated).hexdigest(), "decision": "exclude",
                 "raw_word_count": 4, "counted_word_count": 0},
            ]}))
            audit = AttachmentAudit(path)
            self.assertEqual(audit.count(mixed.encode()), 3)
            self.assertEqual(audit.count(generated), 0)
            # The user's explicit trust rule applies to direct input, regardless of its appearance.
            self.assertEqual(message_word_count(generated.decode(), Path(directory), audit), 4)
            with self.assertRaisesRegex(ValueError, 'has not been audited'):
                audit.count((mixed + 'New content.').encode())

    def test_image_blocks_do_not_contribute_words(self):
        turns, _ = collect_turns([
            (1, '2026-11-01T00:00:00Z', {"type": "task_started", "turn_id": "t"}),
            (2, '2026-11-01T00:00:01Z', {"type": "item_completed", "turn_id": "t", "item": {
                "type": "UserMessage", "client_id": "p", "content": [
                    {"type": "text", "text": "Use my sketch"},
                    {"type": "image", "text": "Image metadata must never count", "url": "data:image/png;base64,abc"},
                ]}}),
        ])
        self.assertEqual(loop_word_counts(turns['t']['users'], Path('/unused'))['total_word_count'], 3)

    def test_response_annotations_count_comments_and_request_only(self):
        message = ('# Response annotations:\nGenerated instructions do not count.\n<response-annotations>\n'
                   + json.dumps([{"text": "An earlier assistant response selected in the UI", "comment": "Too vague.",
                                  "source": {"messageId": "generated-id", "startOffset": 12}}])
                   + '\n</response-annotations>\n\n## My request:\nUse plain language.')
        self.assertEqual(message_word_count(message, Path('/unused')), 5)

    def test_enrichment_preserves_snapshot_and_excludes_later_steers(self):
        def event(second, payload):
            return {"timestamp": f"2026-11-01T00:00:0{second}.000Z", "type": "event_msg", "payload": payload}

        records = [
            event(0, {"type": "task_started", "turn_id": "t"}),
            event(1, {"type": "user_message", "client_id": "p", "message": "Initial request"}),
            event(1, {"type": "item_completed", "turn_id": "t", "item": {
                "type": "UserMessage", "client_id": "p", "content": [{"type": "text", "text": "Initial request"}]}}),
            event(2, {"type": "user_message", "client_id": "s", "message": "Add three words"}),
            event(3, {"type": "user_message", "client_id": "later", "message": "Not in the frozen row"}),
            event(5, {"type": "task_complete", "turn_id": "t", "duration_ms": 5000}),
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            home, dataset = root / 'codex', root / 'dataset'
            home.mkdir()
            dataset.mkdir()
            (dataset / 'attachment-audit.json').write_text(json.dumps({"reviews": []}))
            (home / 'source.jsonl').write_text(''.join(json.dumps(record) + '\n' for record in records))
            turns, _ = collect_turns([(i + 1, record["timestamp"], record["payload"])
                                      for i, record in enumerate(records[:4])])
            row = timing_row({"id": "c", "title": "Example", "archived": 0}, "t", turns["t"],
                             records[3]["timestamp"], 'source.jsonl', home)
            original = {key: str(value) for key, value in row.items() if key not in WORD_FIELDS}
            source = dataset / 'agentic-loops.csv'
            with source.open('w', newline='') as handle:
                writer = csv.DictWriter(handle, fieldnames=list(original))
                writer.writeheader()
                writer.writerow(original)
            metadata = {"captured_at_utc": "2026-11-01T00:00:04.000Z", "initial_prompts": 1, "user_messages": 2}
            (dataset / 'metadata.json').write_text(json.dumps(metadata))
            original_hash = hashlib.sha256(source.read_bytes()).hexdigest()
            labels = b'unchanged classifications\n'
            (dataset / 'prompt-classifications.csv').write_bytes(labels)
            (dataset / 'classification-metadata.json').write_text(json.dumps({
                "source_sha256": original_hash, "classifications_sha256": hashlib.sha256(labels).hexdigest(),
            }))
            with redirect_stdout(io.StringIO()):
                enrich(dataset, home)
            with source.open(newline='') as handle:
                enriched = next(csv.DictReader(handle))
            self.assertEqual({key: enriched[key] for key in original}, original)
            self.assertEqual(json.loads(enriched['steer_word_counts']), [3])
            self.assertEqual(enriched['total_word_count'], '5')
            provenance = json.loads((dataset / 'classification-metadata.json').read_text())
            self.assertEqual(provenance['source_enrichment']['source_before_sha256'], original_hash)
            self.assertEqual(provenance['source_sha256'], hashlib.sha256(source.read_bytes()).hexdigest())
            before = {path.name: path.read_bytes() for path in dataset.iterdir()}
            with redirect_stdout(io.StringIO()):
                enrich(dataset, home)
            self.assertEqual({path.name: path.read_bytes() for path in dataset.iterdir()}, before)


if __name__ == '__main__':
    unittest.main()
