"""
book.py - Book, PhysicalBook, and DigitalBook classes
"""


class Book:
    def __init__(self, title: str, author: str, isbn: str):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_available = True

    def borrow(self):
        if not self.is_available:
            print(f"'{self.title}' is already borrowed.")
            return False
        self.is_available = False
        print(f"You borrowed '{self.title}'.")
        return True

    def return_book(self):
        self.is_available = True
        print(f"'{self.title}' has been returned.")

    def __str__(self):
        status = "Available" if self.is_available else "Borrowed"
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - {status}"


class PhysicalBook(Book):
    def __init__(self, title: str, author: str, isbn: str, shelf_location: str, condition: str = "Good"):
        super().__init__(title, author, isbn)
        self.shelf_location = shelf_location
        self.condition = condition

    def __str__(self):
        base = super().__str__()
        return f"{base} | Shelf: {self.shelf_location} | Condition: {self.condition}"


class DigitalBook(Book):
    def __init__(self, title: str, author: str, isbn: str, file_format: str, download_link: str):
        super().__init__(title, author, isbn)
        self.file_format = file_format
        self.download_link = download_link
        self.is_available = True  # digital copies are never "checked out" physically

    def borrow(self):
        # Digital books can always be "borrowed" — no scarcity
        print(f"You accessed '{self.title}' ({self.file_format}) at {self.download_link}")
        return True

    def return_book(self):
        # Nothing to return for a digital copy
        print(f"'{self.title}' doesn't need to be returned — it's digital.")

    def __str__(self):
        base = super().__str__()
        return f"{base} | Format: {self.file_format}"


if __name__ == "__main__":
    p = PhysicalBook("Clean Code", "Robert C. Martin", "978-0132350884", "A3-12")
    d = DigitalBook("The Pragmatic Programmer", "Andy Hunt", "978-0135957059", "PDF", "library.local/prag-prog.pdf")

    print(p)
    p.borrow()
    print(p)

    print()
    print(d)
    d.borrow()
    d.borrow()  # should work again, no restriction