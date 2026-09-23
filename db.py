
import sqlite3

from book import PhysicalBook, DigitalBook
from member import Member
from library import Library

DB_FILE = "library.db"


def get_connection():
    return sqlite3.connect(DB_FILE)


def init_db():
    """Create the tables if they don't exist yet. Safe to call every startup."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS books (
        isbn TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        book_type TEXT NOT NULL,
        extra1 TEXT,
        extra2 TEXT,
        is_available INTEGER NOT NULL
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS members (
        member_id TEXT PRIMARY KEY,
        name TEXT NOT NULL
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS borrowed (
        member_id TEXT NOT NULL,
        isbn TEXT NOT NULL,
        due_date TEXT,
        PRIMARY KEY (member_id, isbn)
    )""")
    conn.commit()

    cur.execute("PRAGMA table_info(borrowed)")
    existing_columns = [row[1] for row in cur.fetchall()]
    if "due_date" not in existing_columns:
        cur.execute("ALTER TABLE borrowed ADD COLUMN due_date TEXT")

    conn.commit()
    conn.close()


def save_snapshot(library: Library):
    """Overwrite the DB with the current in-memory state of the library.
    Simple and safe for a library this size — called after every change."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM books")
    cur.execute("DELETE FROM members")
    cur.execute("DELETE FROM borrowed")

    for book in library.books:
        if isinstance(book, DigitalBook):
            cur.execute(
                "INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?)",
                (book.isbn, book.title, book.author, "Digital",
                 book.file_format, book.download_link, int(book.is_available))
            )
        else:
            cur.execute(
                "INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?)",
                (book.isbn, book.title, book.author, "Physical",
                 book.shelf_location, getattr(book, "condition", "Good"), int(book.is_available))
            )

    for member in library.members:
        cur.execute("INSERT INTO members VALUES (?, ?)", (member.member_id, member.name))
        for borrowed_book in member.borrowed_books:
            due_date = member.due_dates.get(borrowed_book.isbn)
            cur.execute("INSERT OR IGNORE INTO borrowed VALUES (?, ?, ?)",
                        (member.member_id, borrowed_book.isbn, due_date))

    conn.commit()
    conn.close()


def load_library(name: str = "Veritas Campus Library"):
    """Load the library from the DB. Returns None if nothing has been saved yet."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT isbn, title, author, book_type, extra1, extra2, is_available FROM books")
    book_rows = cur.fetchall()

    cur.execute("SELECT member_id, name FROM members")
    member_rows = cur.fetchall()

    cur.execute("SELECT member_id, isbn, due_date FROM borrowed")
    borrowed_rows = cur.fetchall()

    conn.close()

    if not book_rows and not member_rows:
        return None  # fresh database, nothing saved yet

    library = Library(name)
    books_by_isbn = {}
    for isbn, title, author, book_type, extra1, extra2, is_available in book_rows:
        if book_type == "Digital":
            book = DigitalBook(title, author, isbn, extra1, extra2)
        else:
            book = PhysicalBook(title, author, isbn, extra1, extra2 or "Good")
        book.is_available = bool(is_available)
        library.books.append(book)
        books_by_isbn[isbn] = book

    members_by_id = {}
    for member_id, name_ in member_rows:
        member = Member(name_, member_id)
        library.members.append(member)
        members_by_id[member_id] = member

    for member_id, isbn, due_date in borrowed_rows:
        member = members_by_id.get(member_id)
        book = books_by_isbn.get(isbn)
        if member and book:
            member.borrowed_books.append(book)
            if due_date:
                member.due_dates[isbn] = due_date

    return library

import sqlite3

from book import PhysicalBook, DigitalBook
from member import Member
from library import Library

DB_FILE = "library.db"


def get_connection():
    return sqlite3.connect(DB_FILE)


def init_db():
    """Create the tables if they don't exist yet. Safe to call every startup."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS books (
        isbn TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        book_type TEXT NOT NULL,
        extra1 TEXT,
        extra2 TEXT,
        is_available INTEGER NOT NULL
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS members (
        member_id TEXT PRIMARY KEY,
        name TEXT NOT NULL
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS borrowed (
        member_id TEXT NOT NULL,
        isbn TEXT NOT NULL,
        due_date TEXT,
        PRIMARY KEY (member_id, isbn)
    )""")
    conn.commit()
    cur.execute("PRAGMA table_info(borrowed)")
    existing_columns = [row[1] for row in cur.fetchall()]
    if "due_date" not in existing_columns:
        cur.execute("ALTER TABLE borrowed ADD COLUMN due_date TEXT")

    conn.commit()
    conn.close()


def save_snapshot(library: Library):
    """Overwrite the DB with the current in-memory state of the library.
    Simple and safe for a library this size — called after every change."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM books")
    cur.execute("DELETE FROM members")
    cur.execute("DELETE FROM borrowed")

    for book in library.books:
        if isinstance(book, DigitalBook):
            cur.execute(
                "INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?)",
                (book.isbn, book.title, book.author, "Digital",
                 book.file_format, book.download_link, int(book.is_available))
            )
        else:
            cur.execute(
                "INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?)",
                (book.isbn, book.title, book.author, "Physical",
                 book.shelf_location, getattr(book, "condition", "Good"), int(book.is_available))
            )

    for member in library.members:
        cur.execute("INSERT INTO members VALUES (?, ?)", (member.member_id, member.name))
        for borrowed_book in member.borrowed_books:
            due_date = member.due_dates.get(borrowed_book.isbn)
            cur.execute("INSERT OR IGNORE INTO borrowed VALUES (?, ?, ?)",
                        (member.member_id, borrowed_book.isbn, due_date))

    conn.commit()
    conn.close()


def load_library(name: str = "Veritas Campus Library"):
    """Load the library from the DB. Returns None if nothing has been saved yet."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT isbn, title, author, book_type, extra1, extra2, is_available FROM books")
    book_rows = cur.fetchall()

    cur.execute("SELECT member_id, name FROM members")
    member_rows = cur.fetchall()

    cur.execute("SELECT member_id, isbn, due_date FROM borrowed")
    borrowed_rows = cur.fetchall()

    conn.close()

    if not book_rows and not member_rows:
        return None  # fresh database, nothing saved yet

    library = Library(name)
    books_by_isbn = {}
    for isbn, title, author, book_type, extra1, extra2, is_available in book_rows:
        if book_type == "Digital":
            book = DigitalBook(title, author, isbn, extra1, extra2)
        else:
            book = PhysicalBook(title, author, isbn, extra1, extra2 or "Good")
        book.is_available = bool(is_available)
        library.books.append(book)
        books_by_isbn[isbn] = book

    members_by_id = {}
    for member_id, name_ in member_rows:
        member = Member(name_, member_id)
        library.members.append(member)
        members_by_id[member_id] = member

    for member_id, isbn, due_date in borrowed_rows:
        member = members_by_id.get(member_id)
        book = books_by_isbn.get(isbn)
        if member and book:
            member.borrowed_books.append(book)
            if due_date:
                member.due_dates[isbn] = due_date

    return library