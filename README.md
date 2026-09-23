# Veritas Campus Library

A desktop library management system built in Python with a modern GUI, SQLite persistence, and role-based dashboards for librarians and members.

## Features

- **Two roles:** password-protected Librarian dashboard, and self-service Member dashboard
- **Member self-registration** — students create their own account and get an auto-generated member ID
- **Object-oriented design** — `Book` base class with `PhysicalBook` and `DigitalBook` subclasses demonstrating inheritance and polymorphism
- **Persistent storage** — all books, members, and borrow records are saved to a local SQLite database and survive restarts
- **Due dates** — 14-day loan periods with overdue tracking, shown in red on the member dashboard
- **Search & filter** — live search across the book catalog by title or author
- **Generated visuals** — book cover thumbnails and member avatars are generated on the fly (no external images needed), plus support for a real institution logo
- **31 unit tests** covering the core `Book`, `Member`, and `Library` classes

## Tech stack

- Python 3
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the GUI
- [Pillow](https://python-pillow.org/) for generated graphics
- SQLite (`sqlite3`, built into Python) for persistence
- `unittest` (built into Python) for testing

## Project structure

```
libraryapp/
├── book.py           # Book, PhysicalBook, DigitalBook classes
├── member.py         # Member class (borrowing, due dates)
├── library.py         # Library class (orchestrates books & members)
├── db.py              # SQLite persistence layer
├── assets.py           # Generates logos, book covers, avatars
├── gui_app.py           # Main GUI application (run this)
├── main.py              # CLI version (earlier prototype)
├── veritas_logo.png       # University logo used in the UI
├── tests/
│   ├── test_book.py
│   ├── test_member.py
│   └── test_library.py
└── library.db              # SQLite database (auto-created, gitignored)
```

## Getting started

1. Clone the repo and open it in your editor.
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Mac/Linux
   ```
3. Install dependencies:
   ```
   pip install customtkinter pillow
   ```
4. Run the app:
   ```
   python gui_app.py
   ```

**Default librarian password:** `veritas2026` (change it in `gui_app.py`)

## Running tests

```
python -m unittest discover -s tests
```

## Screenshots

*(Add a screenshot or two here once you're happy with the look — drag images into this section on GitHub, or reference them like `![Login screen](screenshots/login.png)`)*

## Author

Mancha Nerat — Software Engineering student, Veritas University
