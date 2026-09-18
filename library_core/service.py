from __future__ import annotations
from .models import Book, LibraryStats

class Library:
    def __init__(self, books=None):
        self._books: list[Book] = list(books or [])

    @property
    def books(self) -> tuple[Book, ...]:
        return tuple(self._books)

    def add(self, book: Book) -> Book:
        if not isinstance(book, Book):
            raise TypeError("book must be a Book")
        if self.find(isbn=book.isbn) if book.isbn else False:
            raise ValueError("a book with this ISBN already exists")
        self._books.append(book)
        return book

    def remove(self, title: str) -> Book:
        for index, book in enumerate(self._books):
            if book.title.casefold() == title.casefold():
                return self._books.pop(index)
        raise KeyError(title)

    def find(self, *, title=None, author=None, isbn=None, tag=None):
        result = self._books
        if title: result = [b for b in result if title.casefold() in b.title.casefold()]
        if author: result = [b for b in result if author.casefold() in b.author.casefold()]
        if isbn: result = [b for b in result if b.isbn == isbn]
        if tag: result = [b for b in result if tag.casefold() in b.tags]
        return list(result)

    def mark_read(self, title: str, value=True) -> Book:
        matches = self.find(title=title)
        if not matches: raise KeyError(title)
        return matches[0].mark_read(value)

    def stats(self) -> LibraryStats:
        total = len(self._books)
        return LibraryStats(
            total=total,
            read=sum(b.read for b in self._books),
            unread=sum(not b.read for b in self._books),
            authors=len({b.author.casefold() for b in self._books}),
            tagged=sum(bool(b.tags) for b in self._books),
        )

    def sort_by(self, field: str = "title", reverse=False):
        allowed = {"title","author","year","added_at"}
        if field not in allowed: raise ValueError(f"unsupported sort field: {field}")
        return sorted(self._books, key=lambda b: getattr(b, field) or 0, reverse=reverse)
