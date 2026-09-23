
from datetime import date, timedelta

DEFAULT_LOAN_DAYS = 14


class Member:
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []
        self.due_dates = {}  # isbn -> due date string (YYYY-MM-DD)

    def borrow_book(self, book, loan_days=DEFAULT_LOAN_DAYS):
        if book.borrow():
            self.borrowed_books.append(book)
            due = date.today() + timedelta(days=loan_days)
            self.due_dates[book.isbn] = due.isoformat()
            return True
        return False

    def return_book(self, book):
        if book in self.borrowed_books:
            book.return_book()
            self.borrowed_books.remove(book)
            self.due_dates.pop(book.isbn, None)
            return True
        else:
            print(f"{self.name} doesn't have '{book.title}' borrowed.")
            return False

    def is_overdue(self, isbn):
        due_str = self.due_dates.get(isbn)
        if not due_str:
            return False
        return date.fromisoformat(due_str) < date.today()

    def list_borrowed(self):
        if not self.borrowed_books:
            print(f"{self.name} has no borrowed books.")
            return
        print(f"{self.name}'s borrowed books:")
        for book in self.borrowed_books:
            due = self.due_dates.get(book.isbn, "unknown")
            print(f"  - {book.title} (due {due})")

    def __str__(self):
        return f"Member: {self.name} (ID: {self.member_id}) | {len(self.borrowed_books)} book(s) borrowed"