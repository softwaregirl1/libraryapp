
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from book import PhysicalBook, DigitalBook
from member import Member
from library import Library


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.library = Library("Test Library")
        self.book = PhysicalBook("Clean Code", "Robert C. Martin", "978-0132350884", "A3-12")
        self.member = Member("Mancha Nerat", "M001")

    def test_add_book(self):
        self.library.add_book(self.book)
        self.assertIn(self.book, self.library.books)

    def test_remove_book(self):
        self.library.add_book(self.book)
        result = self.library.remove_book("978-0132350884")
        self.assertTrue(result)
        self.assertNotIn(self.book, self.library.books)

    def test_remove_nonexistent_book_fails(self):
        result = self.library.remove_book("does-not-exist")
        self.assertFalse(result)

    def test_search_by_title(self):
        self.library.add_book(self.book)
        results = self.library.search_by_title("clean")  # case-insensitive
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Clean Code")

    def test_search_by_title_no_match(self):
        self.library.add_book(self.book)
        results = self.library.search_by_title("nonexistent")
        self.assertEqual(results, [])

    def test_find_book_by_isbn(self):
        self.library.add_book(self.book)
        found = self.library.find_book_by_isbn("978-0132350884")
        self.assertEqual(found, self.book)

    def test_add_and_find_member(self):
        self.library.add_member(self.member)
        found = self.library.find_member("M001")
        self.assertEqual(found, self.member)

    def test_borrow_book_end_to_end(self):
        self.library.add_book(self.book)
        self.library.add_member(self.member)
        result = self.library.borrow_book("M001", "978-0132350884")
        self.assertTrue(result)
        self.assertFalse(self.book.is_available)
        self.assertIn(self.book, self.member.borrowed_books)

    def test_borrow_with_invalid_member_fails(self):
        self.library.add_book(self.book)
        result = self.library.borrow_book("NOT_REAL", "978-0132350884")
        self.assertFalse(result)

    def test_borrow_with_invalid_isbn_fails(self):
        self.library.add_member(self.member)
        result = self.library.borrow_book("M001", "NOT_REAL")
        self.assertFalse(result)

    def test_return_book_end_to_end(self):
        self.library.add_book(self.book)
        self.library.add_member(self.member)
        self.library.borrow_book("M001", "978-0132350884")
        result = self.library.return_book("M001", "978-0132350884")
        self.assertTrue(result)
        self.assertTrue(self.book.is_available)


if __name__ == "__main__":
    unittest.main()