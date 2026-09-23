
import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from book import Book, PhysicalBook, DigitalBook


class TestBook(unittest.TestCase):
    def setUp(self):
        self.book = Book("Clean Code", "Robert C. Martin", "978-0132350884")

    def test_starts_available(self):
        self.assertTrue(self.book.is_available)

    def test_borrow_makes_unavailable(self):
        result = self.book.borrow()
        self.assertTrue(result)
        self.assertFalse(self.book.is_available)

    def test_cannot_borrow_twice(self):
        self.book.borrow()
        result = self.book.borrow()
        self.assertFalse(result) 
        self.assertFalse(self.book.is_available)

    def test_return_makes_available_again(self):
        self.book.borrow()
        self.book.return_book()
        self.assertTrue(self.book.is_available)

    def test_str_shows_available_status(self):
        self.assertIn("Available", str(self.book))
        self.book.borrow()
        self.assertIn("Borrowed", str(self.book))


class TestPhysicalBook(unittest.TestCase):
    def setUp(self):
        self.book = PhysicalBook("Clean Code", "Robert C. Martin", "978-0132350884", "A3-12")

    def test_has_shelf_location(self):
        self.assertEqual(self.book.shelf_location, "A3-12")

    def test_default_condition_is_good(self):
        self.assertEqual(self.book.condition, "Good")

    def test_borrow_return_still_works(self):
        self.book.borrow()
        self.assertFalse(self.book.is_available)
        self.book.return_book()
        self.assertTrue(self.book.is_available)

    def test_str_includes_shelf_info(self):
        self.assertIn("A3-12", str(self.book))


class TestDigitalBook(unittest.TestCase):
    def setUp(self):
        self.book = DigitalBook("The Pragmatic Programmer", "Andy Hunt", "978-0135957059",
                                 "PDF", "library.local/prag-prog.pdf")

    def test_never_becomes_unavailable(self):
        self.book.borrow()
        self.assertTrue(self.book.is_available)  # digital copies are unlimited

    def test_can_be_borrowed_multiple_times(self):
        result1 = self.book.borrow()
        result2 = self.book.borrow()
        self.assertTrue(result1)
        self.assertTrue(result2)

    def test_return_does_not_error(self):
        self.book.borrow()
        self.book.return_book()  # should not raise, and stays available
        self.assertTrue(self.book.is_available)

    def test_str_includes_format(self):
        self.assertIn("PDF", str(self.book))


if __name__ == "__main__":
    unittest.main()