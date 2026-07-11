import json
import os
from typing import Any
from .. import constant


class Score:
    def __init__(self) -> None:
        self.score: int = 0


def sanitize_name_char(char: str) -> str:
    """Return the char if it is alphanumeric or a space, else ''."""
    if len(char) == 1 and (char.isalnum() or char == " "):
        return char
    return ""


def load_highscores(file_path: str) -> list[dict[str, Any]]:
    """Load highscores robustly.

    Returns a list of ``{'name': str, 'score': int}`` entries, sorted by
    score descending and capped at the top 10. Missing files, invalid JSON
    and malformed entries are ignored (never raises).
    """
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, "r") as f:
            raw = json.load(f)
    except (json.JSONDecodeError, ValueError, OSError):
        return []
    if not isinstance(raw, list):
        return []
    scores: list[dict[str, Any]] = []
    for entry in raw:
        if not isinstance(entry, dict):
            continue
        name = entry.get("name")
        value = entry.get("score")
        if not isinstance(name, str):
            continue
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            continue
        scores.append({"name": name, "score": value})
    scores.sort(key=lambda s: s["score"], reverse=True)
    return scores[:constant.MAX_HIGHSCORES]


def save_highscore(file_path: str, name: str, score: int) -> None:
    """Append a score, keep only the top 10, and persist to disk."""
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    scores = load_highscores(file_path)
    scores.append({"name": name, "score": max(0, score)})
    scores.sort(key=lambda s: s["score"], reverse=True)
    scores = scores[:constant.MAX_HIGHSCORES]
    with open(file_path, "w") as f:
        json.dump(scores, f, indent=4)
