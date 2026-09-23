
class Library:
    def __init__(self, name: str):
        self.name = name
        self.books = []      # all Book/PhysicalBook/DigitalBook objects
        self.members = []    # all Member objects

    # ---- Book management ----
    def add_book(self, book):
        self.books.append(book)
        print(f"Added '{book.title}' to {self.name}.")

    def remove_book(self, isbn: str):
        for book in self.books:
            if book.isbn == isbn:
                self.books.remove(book)
                print(f"Removed '{book.title}' from {self.name}.")
                return True
        print(f"No book found with ISBN {isbn}.")
        return False

    def search_by_title(self, keyword: str):
        results = [b for b in self.books if keyword.lower() in b.title.lower()]
        return results

    def search_by_author(self, keyword: str):
        results = [b for b in self.books if keyword.lower() in b.author.lower()]
        return results

    # ---- Member management ----
    def add_member(self, member):
        self.members.append(member)
        print(f"Registered member: {member.name}")

    def find_member(self, member_id: str):
        for member in self.members:
            if member.member_id == member_id:
                return member
        return None

    def find_book_by_isbn(self, isbn: str):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    # ---- Borrow/return orchestration ----
    def borrow_book(self, member_id: str, isbn: str):
        member = self.find_member(member_id)
        book = self.find_book_by_isbn(isbn)

        if not member:
            print(f"No member found with ID {member_id}.")
            return False
        if not book:
            print(f"No book found with ISBN {isbn}.")
            return False

        return member.borrow_book(book)

    def return_book(self, member_id: str, isbn: str):
        member = self.find_member(member_id)
        book = self.find_book_by_isbn(isbn)

        if not member or not book:
            print("Member or book not found.")
            return False

        return member.return_book(book)

    def list_all_books(self):
        if not self.books:
            print("No books in the library yet.")
            return
        print(f"\n--- {self.name}: All Books ---")
        for book in self.books:
            print(book)

    def __str__(self):
        return f"{self.name} | {len(self.books)} book(s) | {len(self.members)} member(s)"


if __name__ == "__main__":
    from book import PhysicalBook, DigitalBook
    from member import Member

    lib = Library("Veritas Campus Library")

    p = PhysicalBook("Clean Code", "Robert C. Martin", "978-0132350884", "A3-12")
    d = DigitalBook("The Pragmatic Programmer", "Andy Hunt", "978-0135957059", "PDF", "library.local/prag-prog.pdf")
    lib.add_book(p)
    lib.add_book(d)

    m = Member("Mancha Nerat", "M001")
    lib.add_member(m)

    lib.list_all_books()

    lib.borrow_book("M001", "978-0132350884")
    lib.list_all_books()

    results = lib.search_by_title("pragmatic")
    print(f"\nSearch results for 'pragmatic': {[b.title for b in results]}")

    lib.return_book("M001", "978-0132350884")
    lib.list_all_books()