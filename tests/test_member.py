
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from book import PhysicalBook
from member import Member


class TestMember(unittest.TestCase):
    def setUp(self):
        self.member = Member("Mancha Nerat", "M001")
        self.book = PhysicalBook("Clean Code", "Robert C. Martin", "978-0132350884", "A3-12")

    def test_starts_with_no_borrowed_books(self):
        self.assertEqual(self.member.borrowed_books, [])

    def test_borrow_book_adds_to_list(self):
        self.member.borrow_book(self.book)
        self.assertIn(self.book, self.member.borrowed_books)

    def test_borrow_unavailable_book_fails(self):
        other_member = Member("David Okafor", "M002")
        self.member.borrow_book(self.book)
        result = other_member.borrow_book(self.book)  # already borrowed by self.member
        self.assertFalse(result)
        self.assertNotIn(self.book, other_member.borrowed_books)

    def test_return_book_removes_from_list(self):
        self.member.borrow_book(self.book)
        self.member.return_book(self.book)
        self.assertNotIn(self.book, self.member.borrowed_books)
        self.assertTrue(self.book.is_available)

    def test_return_book_not_borrowed_fails_gracefully(self):
        result = self.member.return_book(self.book)  # never borrowed it
        self.assertFalse(result)

    def test_due_date_set_on_borrow(self):
        self.member.borrow_book(self.book)
        self.assertIn(self.book.isbn, self.member.due_dates)

    def test_due_date_cleared_on_return(self):
        self.member.borrow_book(self.book)
        self.member.return_book(self.book)
        self.assertNotIn(self.book.isbn, self.member.due_dates)


if __name__ == "__main__":
    unittest.main()