"""
member.py - Member class
"""


class Member:
    def __init__(self, name: str, member_id: str):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []  # list of Book objects currently borrowed

    def borrow_book(self, book):
        if book.borrow():  # Book/PhysicalBook/DigitalBook all support .borrow()
            self.borrowed_books.append(book)
            return True
        return False

    def return_book(self, book):
        if book in self.borrowed_books:
            book.return_book()
            self.borrowed_books.remove(book)
            return True
        else:
            print(f"{self.name} doesn't have '{book.title}' borrowed.")
            return False

    def list_borrowed(self):
        if not self.borrowed_books:
            print(f"{self.name} has no borrowed books.")
            return
        print(f"{self.name}'s borrowed books:")
        for book in self.borrowed_books:
            print(f"  - {book.title}")

    def __str__(self):
        return f"Member: {self.name} (ID: {self.member_id}) | {len(self.borrowed_books)} book(s) borrowed"


if __name__ == "__main__":
    from book import PhysicalBook, DigitalBook

    m = Member("Mancha Nerat", "M001")
    p = PhysicalBook("Clean Code", "Robert C. Martin", "978-0132350884", "A3-12")
    d = DigitalBook("The Pragmatic Programmer", "Andy Hunt", "978-0135957059", "PDF", "library.local/prag-prog.pdf")

    print(m)
    m.borrow_book(p)
    m.borrow_book(d)
    m.list_borrowed()
    print(m)

    m.return_book(p)
    m.list_borrowed()