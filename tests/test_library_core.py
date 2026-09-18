import tempfile
import unittest
from pathlib import Path
from library_core import Book, Library, JsonLibraryStore

class LibraryCoreTests(unittest.TestCase):
    def test_search_and_stats(self):
        library = Library([
            Book("Dune", "Frank Herbert", 1965, tags={"SciFi"}),
            Book("Clean Code", "Robert Martin", 2008),
        ])
        library.mark_read("Dune")
        self.assertEqual(len(library.find(author="herbert")), 1)
        self.assertEqual(library.stats().read_rate, 0.5)

    def test_json_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "library.json"
            books = [Book("Dune", "Frank Herbert", 1965, isbn="123", tags={"SciFi"})]
            JsonLibraryStore(path).save(books)
            loaded = JsonLibraryStore(path).load()
            self.assertEqual(loaded[0].title, "Dune")
            self.assertEqual(loaded[0].isbn, "123")

    def test_duplicate_isbn_is_rejected(self):
        library = Library()
        library.add(Book("A", "Author", isbn="123"))
        with self.assertRaises(ValueError):
            library.add(Book("B", "Other", isbn="123"))

if __name__ == "__main__":
    unittest.main()
