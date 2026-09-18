from __future__ import annotations
import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from .models import Book

def book_to_dict(book: Book) -> dict:
    data = asdict(book)
    data["tags"] = sorted(book.tags)
    data["added_at"] = book.added_at.isoformat()
    return data

def book_from_dict(data: dict) -> Book:
    payload = dict(data)
    payload["tags"] = set(payload.get("tags", []))
    payload["added_at"] = datetime.fromisoformat(payload["added_at"])
    return Book(**payload)

class JsonLibraryStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def save(self, books) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = [book_to_dict(book) for book in books]
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        temporary.replace(self.path)

    def load(self) -> list[Book]:
        if not self.path.exists():
            return []
        data = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError("library file must contain a JSON list")
        return [book_from_dict(item) for item in data]
