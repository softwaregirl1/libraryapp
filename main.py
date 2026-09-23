

from book import PhysicalBook, DigitalBook
from member import Member
from library import Library


def print_menu():
    print("\n===== Veritas Campus Library =====")
    print("1. Add a physical book")
    print("2. Add a digital book")
    print("3. Register a member")
    print("4. List all books")
    print("5. Search by title")
    print("6. Borrow a book")
    print("7. Return a book")
    print("8. Exit")


def main():
    lib = Library("Veritas Campus Library")

    # Seed with a couple of example books/members so the menu isn't empty at first
    lib.add_book(PhysicalBook("Clean Code", "Robert C. Martin", "978-0132350884", "A3-12"))
    lib.add_book(DigitalBook("The Pragmatic Programmer", "Andy Hunt", "978-0135957059", "PDF", "library.local/prag-prog.pdf"))
    lib.add_member(Member("Mancha Nerat", "M001"))

    while True:
        print_menu()
        choice = input("Choose an option (1-8): ").strip()

        if choice == "1":
            title = input("Title: ").strip()
            author = input("Author: ").strip()
            isbn = input("ISBN: ").strip()
            shelf = input("Shelf location: ").strip()
            lib.add_book(PhysicalBook(title, author, isbn, shelf))

        elif choice == "2":
            title = input("Title: ").strip()
            author = input("Author: ").strip()
            isbn = input("ISBN: ").strip()
            file_format = input("File format (e.g. PDF): ").strip()
            link = input("Download link: ").strip()
            lib.add_book(DigitalBook(title, author, isbn, file_format, link))

        elif choice == "3":
            name = input("Member name: ").strip()
            member_id = input("Member ID: ").strip()
            lib.add_member(Member(name, member_id))

        elif choice == "4":
            lib.list_all_books()

        elif choice == "5":
            keyword = input("Search title keyword: ").strip()
            results = lib.search_by_title(keyword)
            if results:
                print(f"\nFound {len(results)} result(s):")
                for b in results:
                    print(b)
            else:
                print("No matches found.")

        elif choice == "6":
            member_id = input("Member ID: ").strip()
            isbn = input("Book ISBN: ").strip()
            lib.borrow_book(member_id, isbn)

        elif choice == "7":
            member_id = input("Member ID: ").strip()
            isbn = input("Book ISBN: ").strip()
            lib.return_book(member_id, isbn)

        elif choice == "8":
            print("Goodbye!")
            break

        else:
            print("Invalid option, please choose 1-8.")


if __name__ == "__main__":
    main()