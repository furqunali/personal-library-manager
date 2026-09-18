from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Book:
    title: str
    author: str
    year: Optional[int] = None
    isbn: Optional[str] = None
    tags: set[str] = field(default_factory=set)
    added_at: datetime = field(default_factory=datetime.utcnow)
    read: bool = False

    def __post_init__(self):
        self.title = self.title.strip()
        self.author = self.author.strip()
        if not self.title or not self.author:
            raise ValueError("title and author are required")
        if self.year is not None and (self.year < 0 or self.year > datetime.utcnow().year + 1):
            raise ValueError("year is outside the supported range")
        self.tags = {tag.strip().lower() for tag in self.tags if tag.strip()}

    def mark_read(self, value: bool = True):
        self.read = bool(value)
        return self

@dataclass
class LibraryStats:
    total: int
    read: int
    unread: int
    authors: int
    tagged: int

    @property
    def read_rate(self) -> float:
        return self.read / self.total if self.total else 0.0
