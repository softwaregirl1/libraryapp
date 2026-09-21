"""
gui_app.py - Veritas Campus Library (CustomTkinter edition)

Requires: pip install customtkinter

Screens:
  - Login (member ID, or librarian password)
  - Librarian Dashboard: add/remove books, view members
  - Member Dashboard: browse, borrow, return books
"""

import customtkinter as ctk
from tkinter import ttk, messagebox

from book import PhysicalBook, DigitalBook
from member import Member
from library import Library


# ---------- Appearance ----------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

FONT_TITLE = ("Segoe UI", 22, "bold")
FONT_HEADER = ("Segoe UI", 14, "bold")
FONT_BODY = ("Segoe UI", 12)

LIBRARIAN_PASSWORD = "veritas2026"


class LibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Veritas Campus Library")
        self.geometry("1000x680")

        self.library = Library("Veritas Campus Library")
        self._seed_data()
        self.current_member = None

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self._style_treeview()
        self.show_login()

    def _style_treeview(self):
        """Make the ttk.Treeview tables match the CustomTkinter look."""
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", rowheight=28, font=FONT_BODY,
                         background="#FFFFFF", fieldbackground="#FFFFFF", borderwidth=0)
        style.configure("Treeview.Heading", font=FONT_HEADER,
                         background="#E8ECF1", foreground="#1F3A5F")
        style.map("Treeview", background=[("selected", "#2D7DD2")],
                  foreground=[("selected", "white")])

    def _seed_data(self):
        self.library.add_book(PhysicalBook("Clean Code", "Robert C. Martin", "978-0132350884", "A3-12"))
        self.library.add_book(DigitalBook("The Pragmatic Programmer", "Andy Hunt", "978-0135957059", "PDF", "library.local/prag-prog.pdf"))
        self.library.add_book(PhysicalBook("Introduction to Algorithms", "Thomas H. Cormen", "978-0262033848", "B1-04"))
        self.library.add_member(Member("Mancha Nerat", "M001"))
        self.library.add_member(Member("David Okafor", "M002"))

    def _clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_login(self):
        self._clear_container()
        LoginScreen(self.container, self)

    def show_admin_dashboard(self):
        self._clear_container()
        AdminDashboard(self.container, self)

    def show_member_dashboard(self, member):
        self.current_member = member
        self._clear_container()
        MemberDashboard(self.container, self)


class Header(ctk.CTkFrame):
    def __init__(self, parent, app, title_text, show_logout=True):
        super().__init__(parent, height=64, corner_radius=0, fg_color=("#1F3A5F", "#14273F"))
        self.pack(fill="x", side="top")
        self.pack_propagate(False)

        ctk.CTkLabel(self, text=title_text, font=FONT_TITLE, text_color="white").pack(side="left", padx=24)

        if show_logout:
            ctk.CTkButton(self, text="Log out", command=app.show_login,
                          font=FONT_BODY, width=100, corner_radius=8).pack(side="right", padx=24)


class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.app = app

        Header(self, app, "Veritas Campus Library", show_logout=False)

        card = ctk.CTkFrame(self, corner_radius=16, width=380)
        card.place(relx=0.5, rely=0.55, anchor="center")

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=36, pady=36)

        ctk.CTkLabel(inner, text="Sign in", font=("Segoe UI", 18, "bold")).pack(pady=(0, 20))

        ctk.CTkLabel(inner, text="Librarian Password", font=FONT_BODY, anchor="w").pack(fill="x")
        self.password_entry = ctk.CTkEntry(inner, width=280, height=36, show="*")
        self.password_entry.pack(pady=(4, 10))
        self.password_entry.bind("<Return>", lambda e: self._librarian_login())

        ctk.CTkButton(inner, text="Enter as Librarian", command=self._librarian_login,
                      width=280, height=40, corner_radius=10, font=FONT_BODY).pack(pady=6)

        ctk.CTkLabel(inner, text="— or —", font=FONT_BODY, text_color="gray").pack(pady=8)

        ctk.CTkLabel(inner, text="Member ID", font=FONT_BODY, anchor="w").pack(fill="x")
        self.member_id_entry = ctk.CTkEntry(inner, width=280, height=36)
        self.member_id_entry.pack(pady=(4, 10))
        self.member_id_entry.bind("<Return>", lambda e: self._member_login())

        ctk.CTkButton(inner, text="Enter as Member", command=self._member_login,
                      width=280, height=40, corner_radius=10, font=FONT_BODY,
                      fg_color="#4CAF50", hover_color="#3D8B40").pack(pady=6)

        ctk.CTkLabel(inner, text="(Try M001 or M002)", font=("Segoe UI", 10),
                     text_color="gray").pack(pady=(8, 0))

    def _librarian_login(self):
        password = self.password_entry.get()
        if password == LIBRARIAN_PASSWORD:
            self.password_entry.delete(0, "end")
            self.app.show_admin_dashboard()
        else:
            messagebox.showerror("Access denied", "Incorrect librarian password.")

    def _member_login(self):
        member_id = self.member_id_entry.get().strip()
        member = self.app.library.find_member(member_id)
        if member:
            self.app.show_member_dashboard(member)
        else:
            messagebox.showerror("Not found", f"No member found with ID '{member_id}'.")


class AdminDashboard(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.app = app

        Header(self, app, "Librarian Dashboard")

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=20, pady=20)

        # Left: books table
        left = ctk.CTkFrame(body, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ctk.CTkLabel(left, text="All Books", font=FONT_HEADER).pack(anchor="w", pady=(0, 6))
        columns = ("title", "author", "isbn", "type", "status")
        self.tree = ttk.Treeview(left, columns=columns, show="headings", height=14)
        for col, label, width in [
            ("title", "Title", 200), ("author", "Author", 150),
            ("isbn", "ISBN", 130), ("type", "Type", 80), ("status", "Status", 90),
        ]:
            self.tree.heading(col, text=label)
            self.tree.column(col, width=width)
        self.tree.pack(fill="both", expand=True)

        ctk.CTkButton(left, text="Remove Selected Book", command=self._remove_selected,
                      fg_color="#D9534F", hover_color="#B33C39", font=FONT_BODY,
                      corner_radius=8, height=36).pack(anchor="w", pady=(10, 0))

        # Right: add-book form
        right = ctk.CTkFrame(body, corner_radius=16, width=300)
        right.pack(side="right", fill="y")
        right_inner = ctk.CTkFrame(right, fg_color="transparent")
        right_inner.pack(padx=20, pady=20, fill="both")

        ctk.CTkLabel(right_inner, text="Add a Book", font=FONT_HEADER).pack(anchor="w", pady=(0, 12))

        self.book_type = ctk.StringVar(value="Physical")
        type_frame = ctk.CTkFrame(right_inner, fg_color="transparent")
        type_frame.pack(anchor="w", pady=(0, 12))
        ctk.CTkRadioButton(type_frame, text="Physical", variable=self.book_type, value="Physical",
                           command=self._toggle_fields).pack(side="left", padx=(0, 12))
        ctk.CTkRadioButton(type_frame, text="Digital", variable=self.book_type, value="Digital",
                           command=self._toggle_fields).pack(side="left")

        self.title_entry = self._labeled_entry(right_inner, "Title")
        self.author_entry = self._labeled_entry(right_inner, "Author")
        self.isbn_entry = self._labeled_entry(right_inner, "ISBN")

        self.extra_label = ctk.CTkLabel(right_inner, text="Shelf Location", font=FONT_BODY, anchor="w")
        self.extra_label.pack(fill="x")
        self.extra_entry = ctk.CTkEntry(right_inner, width=250, height=34)
        self.extra_entry.pack(pady=(4, 12))

        self.extra2_label = ctk.CTkLabel(right_inner, text="Download Link", font=FONT_BODY, anchor="w")
        self.extra2_entry = ctk.CTkEntry(right_inner, width=250, height=34)
        # extra2 only shown for Digital books

        ctk.CTkButton(right_inner, text="Add Book", command=self._add_book,
                      width=250, height=40, corner_radius=10, font=FONT_BODY).pack(pady=(6, 0))

        # Members panel
        members_frame = ctk.CTkFrame(self, fg_color="transparent")
        members_frame.pack(fill="x", padx=20, pady=(0, 20))
        ctk.CTkLabel(members_frame, text="Members", font=FONT_HEADER).pack(anchor="w", pady=(0, 6))
        self.members_box = ctk.CTkTextbox(members_frame, height=90, font=FONT_BODY)
        self.members_box.pack(fill="x")
        self.members_box.configure(state="disabled")

        self._refresh_all()

    def _labeled_entry(self, parent, label_text):
        ctk.CTkLabel(parent, text=label_text, font=FONT_BODY, anchor="w").pack(fill="x")
        entry = ctk.CTkEntry(parent, width=250, height=34)
        entry.pack(pady=(4, 12))
        return entry

    def _toggle_fields(self):
        if self.book_type.get() == "Physical":
            self.extra_label.configure(text="Shelf Location")
            self.extra2_label.pack_forget()
            self.extra2_entry.pack_forget()
        else:
            self.extra_label.configure(text="File Format (e.g. PDF)")
            self.extra2_label.pack(fill="x")
            self.extra2_entry.pack(pady=(4, 12))

    def _add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        isbn = self.isbn_entry.get().strip()

        if not title or not author or not isbn:
            messagebox.showwarning("Missing info", "Title, Author, and ISBN are required.")
            return

        if self.app.library.find_book_by_isbn(isbn):
            messagebox.showwarning("Duplicate ISBN", f"A book with ISBN {isbn} already exists.")
            return

        if self.book_type.get() == "Physical":
            shelf = self.extra_entry.get().strip() or "Unassigned"
            book = PhysicalBook(title, author, isbn, shelf)
        else:
            file_format = self.extra_entry.get().strip() or "PDF"
            link = self.extra2_entry.get().strip() or "N/A"
            book = DigitalBook(title, author, isbn, file_format, link)

        self.app.library.add_book(book)
        self._refresh_all()

        for entry in (self.title_entry, self.author_entry, self.isbn_entry, self.extra_entry, self.extra2_entry):
            entry.delete(0, "end")

    def _remove_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("No selection", "Select a book to remove first.")
            return
        isbn = self.tree.item(selected[0], "values")[2]
        self.app.library.remove_book(isbn)
        self._refresh_all()

    def _refresh_all(self):
        self.tree.delete(*self.tree.get_children())
        for book in self.app.library.books:
            book_type = "Digital" if isinstance(book, DigitalBook) else "Physical"
            status = "Available" if book.is_available else "Borrowed"
            self.tree.insert("", "end", values=(book.title, book.author, book.isbn, book_type, status))

        self.members_box.configure(state="normal")
        self.members_box.delete("1.0", "end")
        for member in self.app.library.members:
            line = f"{member.name}  (ID: {member.member_id})  —  {len(member.borrowed_books)} book(s) borrowed\n"
            self.members_box.insert("end", line)
        self.members_box.configure(state="disabled")


class MemberDashboard(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.app = app
        self.member = app.current_member

        Header(self, app, f"Welcome, {self.member.name}")

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(body, text="All Books", font=FONT_HEADER).pack(anchor="w", pady=(0, 6))
        columns = ("title", "author", "isbn", "type", "status")
        self.tree = ttk.Treeview(body, columns=columns, show="headings", height=10)
        for col, label, width in [
            ("title", "Title", 220), ("author", "Author", 160),
            ("isbn", "ISBN", 130), ("type", "Type", 80), ("status", "Status", 90),
        ]:
            self.tree.heading(col, text=label)
            self.tree.column(col, width=width)
        self.tree.pack(fill="both", expand=True, pady=(0, 14))

        btn_frame = ctk.CTkFrame(body, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(0, 20))
        ctk.CTkButton(btn_frame, text="Borrow Selected", command=self._borrow_selected,
                      width=160, height=38, corner_radius=10, font=FONT_BODY).pack(side="left")
        ctk.CTkButton(btn_frame, text="Return Selected", command=self._return_selected,
                      width=160, height=38, corner_radius=10, font=FONT_BODY,
                      fg_color="#D9534F", hover_color="#B33C39").pack(side="left", padx=10)

        ctk.CTkLabel(body, text="My Borrowed Books", font=FONT_HEADER).pack(anchor="w", pady=(0, 6))
        self.my_books_box = ctk.CTkTextbox(body, height=100, font=FONT_BODY)
        self.my_books_box.pack(fill="x")
        self.my_books_box.configure(state="disabled")

        self._refresh_all()

    def _selected_isbn(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("No selection", "Select a book first.")
            return None
        return self.tree.item(selected[0], "values")[2]

    def _borrow_selected(self):
        isbn = self._selected_isbn()
        if not isbn:
            return
        self.app.library.borrow_book(self.member.member_id, isbn)
        self._refresh_all()

    def _return_selected(self):
        isbn = self._selected_isbn()
        if not isbn:
            return
        self.app.library.return_book(self.member.member_id, isbn)
        self._refresh_all()

    def _refresh_all(self):
        self.tree.delete(*self.tree.get_children())
        for book in self.app.library.books:
            book_type = "Digital" if isinstance(book, DigitalBook) else "Physical"
            status = "Available" if book.is_available else "Borrowed"
            self.tree.insert("", "end", values=(book.title, book.author, book.isbn, book_type, status))

        self.my_books_box.configure(state="normal")
        self.my_books_box.delete("1.0", "end")
        if self.member.borrowed_books:
            for book in self.member.borrowed_books:
                self.my_books_box.insert("end", f"{book.title}\n")
        else:
            self.my_books_box.insert("end", "No books borrowed yet.")
        self.my_books_box.configure(state="disabled")


if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()