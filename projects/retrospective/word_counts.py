"""Count human words, trusting direct input and auditing text attachments."""

import hashlib
import json
from pathlib import Path
import re


WORD_FIELDS = ["prompt_word_count", "steer_word_counts", "steer_word_count", "total_word_count"]
WORD_PATTERN = re.compile(r"[^\W_]+(?:['’\-][^\W_]+)*")
QUESTION_OPEN = "<send_user_message_question_reply>"
QUESTION_CLOSE = "</send_user_message_question_reply>"
METHOD = {
    "policy": "human-authored-v1",
    "tokenization": "Unicode letter/number sequences; internal apostrophes and hyphens stay within a word",
    "includes": "Direct user input trusted as human-authored, plus audited human-written text-attachment content",
    "excludes": "Generated diagnostic attachments, unchanged source in mixed attachments, app-generated wrappers, attachment previews/paths, question-reply questions/IDs, selected assistant text in response annotations, images and non-text attachments",
    "question_replies": "Count only the answer strings",
    "steer_order": "Source-log order after message-ID deduplication",
}


class AttachmentAudit:
    """Content hashes bind manual attribution decisions to the reviewed bytes."""

    def __init__(self, path=None):
        self.path = path or Path(__file__).with_name("attachment-audit.json")
        data = self.path.read_bytes()
        self.sha256 = hashlib.sha256(data).hexdigest()
        manifest = json.loads(data)
        self.reviews = {review["sha256"]: review for review in manifest["reviews"]}
        if len(self.reviews) != len(manifest["reviews"]):
            raise ValueError("Repeated content hash in the attachment audit")

    def count(self, data):
        digest = hashlib.sha256(data).hexdigest()
        if digest not in self.reviews:
            raise ValueError(f"Text attachment has not been audited: sha256 {digest}")
        review = self.reviews[digest]
        text = data.decode("utf-8")
        raw_count = count_words(text)
        if raw_count != review["raw_word_count"]:
            raise ValueError("Attachment tokenization differs from the audited count")
        if review["decision"] == "include":
            result = raw_count
        elif review["decision"] == "exclude":
            result = 0
        elif review["decision"] == "partial":
            result, previous_end = 0, 0
            for span in review["included_spans"]:
                start, end = span["start"], span["end"]
                if not 0 <= previous_end <= start < end <= len(text):
                    raise ValueError("Invalid or overlapping human-authored attachment spans")
                result += count_words(text[start:end])
                previous_end = end
        else:
            raise ValueError(f"Unknown attachment audit decision: {review['decision']}")
        if result != review["counted_word_count"]:
            raise ValueError("Human-authored attachment count differs from its audit")
        return result


def count_words(text):
    return len(WORD_PATTERN.findall(text))


def message_word_count(text, codex_home, attachment_audit=None):
    text = text.strip()
    if text.startswith(QUESTION_OPEN):
        if not text.endswith(QUESTION_CLOSE):
            raise ValueError("Incomplete question-reply wrapper")
        replies = json.loads(text[len(QUESTION_OPEN):-len(QUESTION_CLOSE)])
        if not isinstance(replies, list) or any(not isinstance(reply.get("answer"), str) for reply in replies):
            raise ValueError("Expected a list of textual answers")
        return sum(count_words(reply["answer"]) for reply in replies)
    if text.startswith("# Response annotations:"):
        header, separator, request = text.partition("## My request:")
        match = re.search(r"<response-annotations>\s*(.*?)\s*</response-annotations>", header, flags=re.DOTALL)
        if not separator or not match:
            raise ValueError("Incomplete response-annotation wrapper")
        annotations = json.loads(match[1])
        if not isinstance(annotations, list) or any(not isinstance(item.get("comment", ""), str) for item in annotations):
            raise ValueError("Expected a list of response annotations with textual comments")
        return message_word_count(request, codex_home, attachment_audit) + sum(count_words(item.get("comment", "")) for item in annotations)
    if not text.startswith("# Files pasted by the user:"):
        return count_words(text)
    header, separator, request = text.partition("## My request:")
    if not separator:
        raise ValueError("Pasted-text wrapper lacks its request boundary")
    root = (Path(codex_home) / "attachments").resolve()
    references = re.findall(r"^## .*: (/[^\r\n]+)$", header, flags=re.MULTILINE)
    if not references:
        raise ValueError("Pasted-text wrapper has no attachment paths")
    total = count_words(request)
    attachment_audit = attachment_audit or AttachmentAudit()
    seen = set()
    for reference in references:
        path = Path(reference.strip()).resolve()
        if not path.is_relative_to(root):
            raise ValueError(f"Attachment outside the Codex attachment directory: {path}")
        if path not in seen:
            # Missing or unreadable pasted text is an error, never silently zero words.
            total += attachment_audit.count(path.read_bytes())
            seen.add(path)
    return total


def loop_word_counts(users, codex_home, attachment_audit=None):
    counts = [message_word_count(user["text"], codex_home, attachment_audit) for user in users]
    return {
        "prompt_word_count": counts[0],
        "steer_word_counts": json.dumps(counts[1:], separators=(",", ":")),
        "steer_word_count": sum(counts[1:]),
        "total_word_count": sum(counts),
    }


def word_count_summary(rows, attachment_audit=None):
    attachment_audit = attachment_audit or AttachmentAudit()
    return {
        **METHOD,
        "attachment_audit": {"file": attachment_audit.path.name, "sha256": attachment_audit.sha256},
        "prompt_words": sum(int(row["prompt_word_count"]) for row in rows),
        "steer_words": sum(int(row["steer_word_count"]) for row in rows),
        "total_words": sum(int(row["total_word_count"]) for row in rows),
        "ended_loop_words": sum(int(row["total_word_count"]) for row in rows if row["status"] != "open"),
    }
