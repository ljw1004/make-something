"""Count user-supplied words, including complete pasted-text attachments."""

import json
from pathlib import Path
import re


WORD_FIELDS = ["prompt_word_count", "steer_word_counts", "steer_word_count", "total_word_count"]
WORD_PATTERN = re.compile(r"[^\W_]+(?:['’\-][^\W_]+)*")
QUESTION_OPEN = "<send_user_message_question_reply>"
QUESTION_CLOSE = "</send_user_message_question_reply>"
METHOD = {
    "tokenization": "Unicode letter/number sequences; internal apostrophes and hyphens stay within a word",
    "includes": "User message text and full pasted-text attachments, including quoted text, code and debug logs",
    "excludes": "App-generated wrappers, attachment previews/paths, question-reply questions/IDs, selected assistant text in response annotations, images and non-text attachments",
    "question_replies": "Count only the answer strings",
    "steer_order": "Source-log order after message-ID deduplication",
}


def count_words(text):
    return len(WORD_PATTERN.findall(text))


def message_word_count(text, codex_home):
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
        return message_word_count(request, codex_home) + sum(count_words(item.get("comment", "")) for item in annotations)
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
    seen = set()
    for reference in references:
        path = Path(reference.strip()).resolve()
        if not path.is_relative_to(root):
            raise ValueError(f"Attachment outside the Codex attachment directory: {path}")
        if path not in seen:
            # Missing or unreadable pasted text is an error, never silently zero words.
            total += count_words(path.read_text(encoding="utf-8"))
            seen.add(path)
    return total


def loop_word_counts(users, codex_home):
    counts = [message_word_count(user["text"], codex_home) for user in users]
    return {
        "prompt_word_count": counts[0],
        "steer_word_counts": json.dumps(counts[1:], separators=(",", ":")),
        "steer_word_count": sum(counts[1:]),
        "total_word_count": sum(counts),
    }


def word_count_summary(rows):
    return {
        **METHOD,
        "prompt_words": sum(int(row["prompt_word_count"]) for row in rows),
        "steer_words": sum(int(row["steer_word_count"]) for row in rows),
        "total_words": sum(int(row["total_word_count"]) for row in rows),
        "ended_loop_words": sum(int(row["total_word_count"]) for row in rows if row["status"] != "open"),
    }
