
import customtkinter as ctk
from tkinter import messagebox

from book import PhysicalBook, DigitalBook
from member import Member
from library import Library
from assets import make_ctk_book_cover, make_logo, make_avatar, load_real_logo
import db

LOGO_FILE = "veritas_logo.png"  

def get_logo(size: int = 64):
    """Use the real Veritas logo if the file exists, otherwise fall back
    to the generated placeholder logo."""
    try:
        return load_real_logo(LOGO_FILE, max_size=size)
    except (FileNotFoundError, OSError):
        return make_logo(size)


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_HEADER = ("Segoe UI", 14, "bold")
FONT_BODY = ("Segoe UI", 12)
FONT_SMALL = ("Segoe UI", 10)

SIDEBAR_COLOR = ("#1F3A5F", "#14273F")
CARD_COLOR = ("#FFFFFF", "#242424")

LIBRARIAN_PASSWORD = "veritas2026"


class LibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Veritas Campus Library")
        self.geometry("1080x700")

        db.init_db()
        loaded_library = db.load_library()
        if loaded_library:
            self.library = loaded_library
        else:
            self.library = Library("Veritas Campus Library")
            self._seed_data()
            db.save_snapshot(self.library)

        self.current_member = None
        self._next_member_number = self._compute_next_member_number()

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.show_login()

    def _compute_next_member_number(self):
        """Figure out the next free MXXX id based on what's already saved."""
        max_number = 2  # M001, M002 are the baseline seeded IDs
        for member in self.library.members:
            if member.member_id.startswith("M") and member.member_id[1:].isdigit():
                max_number = max(max_number, int(member.member_id[1:]))
        return max_number + 1

    def persist(self):
        """Save the current state to the database. Call after any change."""
        db.save_snapshot(self.library)

    def _seed_data(self):
        self.library.add_book(PhysicalBook("Clean Code", "Robert C. Martin", "978-0132350884", "A3-12"))
        self.library.add_book(DigitalBook("The Pragmatic Programmer", "Andy Hunt", "978-0135957059", "PDF", "library.local/prag-prog.pdf"))
        self.library.add_book(PhysicalBook("Introduction to Algorithms", "Thomas H. Cormen", "978-0262033848", "B1-04"))
        self.library.add_member(Member("Mancha Nerat", "M001"))
        self.library.add_member(Member("David Okafor", "M002"))

    def _clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def register_member(self, name: str):
        member_id = f"M{self._next_member_number:03d}"
        self._next_member_number += 1
        new_member = Member(name, member_id)
        self.library.add_member(new_member)
        self.persist()
        return new_member

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


class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=("#EEF2F6", "#1A1A1A"))
        self.pack(fill="both", expand=True)
        self.app = app
        self.logo_img = get_logo(72)  # keep a reference so it isn't garbage-collected

        card = ctk.CTkFrame(self, corner_radius=18, fg_color=CARD_COLOR)
        card.place(relx=0.5, rely=0.5, anchor="center")

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=40, pady=36)

        ctk.CTkLabel(inner, image=self.logo_img, text="").pack(pady=(0, 8))
        ctk.CTkLabel(inner, text="Veritas Campus Library", font=FONT_TITLE).pack()
        ctk.CTkLabel(inner, text="Sign in to continue", font=FONT_SMALL, text_color="gray").pack(pady=(0, 20))

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

        ctk.CTkButton(inner, text="New here? Register", command=self._open_register_dialog,
                      width=280, height=32, corner_radius=10, font=FONT_SMALL,
                      fg_color="transparent", text_color="#2D7DD2", hover_color=("#E8F0FA", "#1B2A3D"),
                      border_width=1, border_color="#2D7DD2").pack(pady=(2, 6))

        ctk.CTkLabel(inner, text="(Try M001 or M002)", font=FONT_SMALL, text_color="gray").pack(pady=(8, 0))

    def _open_register_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Register New Member")
        dialog.geometry("340x220")
        dialog.transient(self)
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="Create your account", font=("Segoe UI", 15, "bold")).pack(pady=(20, 12))
        ctk.CTkLabel(dialog, text="Full Name", font=FONT_BODY, anchor="w").pack(fill="x", padx=30)
        name_entry = ctk.CTkEntry(dialog, width=260, height=36)
        name_entry.pack(padx=30, pady=(4, 16))
        name_entry.focus()

        def do_register():
            name = name_entry.get().strip()
            if not name:
                messagebox.showwarning("Missing name", "Please enter your full name.")
                return
            new_member = self.app.register_member(name)
            dialog.destroy()
            messagebox.showinfo("Registered!",
                f"Welcome, {new_member.name}!\nYour member ID is {new_member.member_id} — save it, you'll use it to log in.")
            self.member_id_entry.delete(0, "end")
            self.member_id_entry.insert(0, new_member.member_id)

        name_entry.bind("<Return>", lambda e: do_register())
        ctk.CTkButton(dialog, text="Register", command=do_register,
                      width=260, height=38, corner_radius=10, font=FONT_BODY).pack(padx=30)

    def _librarian_login(self):
        if self.password_entry.get() == LIBRARIAN_PASSWORD:
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


class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, app, subtitle, nav_items, on_nav):
        super().__init__(parent, width=200, corner_radius=0, fg_color=SIDEBAR_COLOR)
        self.pack(side="left", fill="y")
        self.pack_propagate(False)
        self.logo_img = get_logo(48)

        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", pady=(24, 8), padx=16)
        ctk.CTkLabel(top, image=self.logo_img, text="").pack()
        ctk.CTkLabel(top, text="Veritas Library", font=("Segoe UI", 15, "bold"), text_color="white").pack(pady=(6, 0))
        ctk.CTkLabel(top, text=subtitle, font=FONT_SMALL, text_color="#9FB3C8").pack()

        ctk.CTkFrame(self, height=1, fg_color="#33507A").pack(fill="x", padx=16, pady=16)

        self.nav_buttons = {}
        for key, label in nav_items:
            btn = ctk.CTkButton(self, text=label, anchor="w", corner_radius=8,
                                fg_color="transparent", hover_color="#2C5182",
                                font=FONT_BODY, text_color="white", height=38,
                                command=lambda k=key: on_nav(k))
            btn.pack(fill="x", padx="12", pady=3)
            self.nav_buttons[key] = btn

        spacer = ctk.CTkFrame(self, fg_color="transparent")
        spacer.pack(fill="both", expand=True)

        ctk.CTkButton(self, text="Log out", command=app.show_login,
                      fg_color="#B33C39", hover_color="#8F2F2C",
                      font=FONT_BODY, height=38, corner_radius=8).pack(fill="x", padx=12, pady=16)

    def set_active(self, key):
        for k, btn in self.nav_buttons.items():
            btn.configure(fg_color="#2C5182" if k == key else "transparent")


class BookCard(ctk.CTkFrame):
    def __init__(self, parent, book, action_label, action_command, action_color="#2D7DD2",
                 action_hover="#1B5FA3", extra_text=None, extra_text_color=None):
        super().__init__(parent, corner_radius=14, fg_color=CARD_COLOR, width=200, height=300)
        self.pack_propagate(False)
        self.cover_img = make_ctk_book_cover(book.title, width=90, height=120)

        ctk.CTkLabel(self, image=self.cover_img, text="").pack(pady=(12, 6))

        book_type = "Digital" if isinstance(book, DigitalBook) else "Physical"
        status = "Available" if book.is_available else "Borrowed"
        status_color = "#4CAF50" if book.is_available else "#D9534F"

        title_lbl = ctk.CTkLabel(self, text=book.title, font=("Segoe UI", 12, "bold"),
                                  wraplength=170, justify="center")
        title_lbl.pack(padx=10, pady=(0, 2))
        ctk.CTkLabel(self, text=book.author, font=FONT_SMALL, text_color="gray",
                     wraplength=170, justify="center").pack(pady=(0, 4))

        badge_row = ctk.CTkFrame(self, fg_color="transparent")
        badge_row.pack(pady=(0, 4))
        ctk.CTkLabel(badge_row, text=book_type, font=FONT_SMALL, fg_color="#E8ECF1",
                     text_color="#1F3A5F", corner_radius=6, padx=8, pady=2).pack(side="left", padx=3)
        ctk.CTkLabel(badge_row, text=status, font=FONT_SMALL, fg_color=status_color,
                     text_color="white", corner_radius=6, padx=8, pady=2).pack(side="left", padx=3)

        if extra_text:
            ctk.CTkLabel(self, text=extra_text, font=FONT_SMALL,
                         text_color=extra_text_color or "gray").pack(pady=(0, 4))

        if action_label:
            ctk.CTkButton(self, text=action_label, command=action_command,
                          width=160, height=30, corner_radius=8, font=FONT_SMALL,
                          fg_color=action_color, hover_color=action_hover).pack(pady=(0, 10))


class AdminDashboard(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.app = app
        self.view = "books"

        self.sidebar = Sidebar(self, app, "Librarian", [("books", "📚  Books"), ("members", "👤  Members")], self._switch_view)
        self.sidebar.set_active("books")

        self.content = ctk.CTkFrame(self, fg_color=("#F4F6F8", "#1A1A1A"))
        self.content.pack(side="left", fill="both", expand=True)

        self._render_books_view()

    def _switch_view(self, key):
        self.view = key
        self.sidebar.set_active(key)
        for widget in self.content.winfo_children():
            widget.destroy()
        if key == "books":
            self._render_books_view()
        else:
            self._render_members_view()

    def _render_books_view(self):
        top_bar = ctk.CTkFrame(self.content, fg_color="transparent")
        top_bar.pack(fill="x", padx=24, pady=(20, 10))
        ctk.CTkLabel(top_bar, text="Book Catalog", font=FONT_TITLE).pack(side="left")
        ctk.CTkButton(top_bar, text="+ Add Book", command=self._open_add_book_dialog,
                      width=130, height=36, corner_radius=8, font=FONT_BODY).pack(side="right")

        search_bar = ctk.CTkFrame(self.content, fg_color="transparent")
        search_bar.pack(fill="x", padx=24, pady=(0, 10))
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *args: self._render_book_cards())
        search_entry = ctk.CTkEntry(search_bar, textvariable=self.search_var, width=320, height=36,
                                     placeholder_text="Search by title or author...")
        search_entry.pack(side="left")

        self.scroll = ctk.CTkScrollableFrame(self.content, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self._card_refs = []
        self._render_book_cards()

    def _render_book_cards(self):
        for widget in self.scroll.winfo_children():
            widget.destroy()
        self._card_refs.clear()

        query = self.search_var.get().strip().lower() if hasattr(self, "search_var") else ""
        books = [b for b in self.app.library.books
                 if query in b.title.lower() or query in b.author.lower()] if query else self.app.library.books

        col_count = 4
        for i, book in enumerate(books):
            card = BookCard(self.scroll, book, "Remove", lambda b=book: self._remove_book(b),
                             action_color="#D9534F", action_hover="#B33C39")
            card.grid(row=i // col_count, column=i % col_count, padx=10, pady=10)
            self._card_refs.append(card)  # keep reference so images aren't garbage-collected

        if not books:
            message = "No books match your search." if query else "No books yet — click '+ Add Book' to get started."
            ctk.CTkLabel(self.scroll, text=message, font=FONT_BODY, text_color="gray").pack(pady=40)

    def _remove_book(self, book):
        self.app.library.remove_book(book.isbn)
        self.app.persist()
        self._render_book_cards()

    def _open_add_book_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add a Book")
        dialog.geometry("360x460")
        dialog.transient(self)
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="Add a Book", font=("Segoe UI", 16, "bold")).pack(pady=(20, 12))

        book_type = ctk.StringVar(value="Physical")
        type_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        type_frame.pack(pady=(0, 10))
        ctk.CTkRadioButton(type_frame, text="Physical", variable=book_type, value="Physical",
                           command=lambda: toggle()).pack(side="left", padx=10)
        ctk.CTkRadioButton(type_frame, text="Digital", variable=book_type, value="Digital",
                           command=lambda: toggle()).pack(side="left", padx=10)

        def labeled(label_text):
            ctk.CTkLabel(dialog, text=label_text, font=FONT_BODY, anchor="w").pack(fill="x", padx=40)
            entry = ctk.CTkEntry(dialog, width=280, height=34)
            entry.pack(padx=40, pady=(2, 10))
            return entry

        title_entry = labeled("Title")
        author_entry = labeled("Author")
        isbn_entry = labeled("ISBN")

        extra_label = ctk.CTkLabel(dialog, text="Shelf Location", font=FONT_BODY, anchor="w")
        extra_label.pack(fill="x", padx=40)
        extra_entry = ctk.CTkEntry(dialog, width=280, height=34)
        extra_entry.pack(padx=40, pady=(2, 10))

        extra2_label = ctk.CTkLabel(dialog, text="Download Link", font=FONT_BODY, anchor="w")
        extra2_entry = ctk.CTkEntry(dialog, width=280, height=34)

        def toggle():
            if book_type.get() == "Physical":
                extra_label.configure(text="Shelf Location")
                extra2_label.pack_forget()
                extra2_entry.pack_forget()
            else:
                extra_label.configure(text="File Format (e.g. PDF)")
                extra2_label.pack(fill="x", padx=40)
                extra2_entry.pack(padx=40, pady=(2, 10))

        def submit():
            title = title_entry.get().strip()
            author = author_entry.get().strip()
            isbn = isbn_entry.get().strip()
            if not title or not author or not isbn:
                messagebox.showwarning("Missing info", "Title, Author, and ISBN are required.")
                return
            if self.app.library.find_book_by_isbn(isbn):
                messagebox.showwarning("Duplicate ISBN", f"A book with ISBN {isbn} already exists.")
                return
            if book_type.get() == "Physical":
                shelf = extra_entry.get().strip() or "Unassigned"
                book = PhysicalBook(title, author, isbn, shelf)
            else:
                file_format = extra_entry.get().strip() or "PDF"
                link = extra2_entry.get().strip() or "N/A"
                book = DigitalBook(title, author, isbn, file_format, link)
            self.app.library.add_book(book)
            self.app.persist()
            dialog.destroy()
            self._render_book_cards()

        ctk.CTkButton(dialog, text="Add Book", command=submit,
                      width=280, height=40, corner_radius=10, font=FONT_BODY).pack(padx=40, pady=(14, 0))

    def _render_members_view(self):
        ctk.CTkLabel(self.content, text="Members", font=FONT_TITLE).pack(anchor="w", padx=24, pady=(20, 10))
        scroll = ctk.CTkScrollableFrame(self.content, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self._avatar_refs = []
        for member in self.app.library.members:
            row = ctk.CTkFrame(scroll, corner_radius=12, fg_color=CARD_COLOR)
            row.pack(fill="x", pady=6, padx=4)
            avatar = make_avatar(member.name, 44)
            self._avatar_refs.append(avatar)
            ctk.CTkLabel(row, image=avatar, text="").pack(side="left", padx=14, pady=10)
            info = ctk.CTkFrame(row, fg_color="transparent")
            info.pack(side="left", fill="x", expand=True, pady=10)
            ctk.CTkLabel(info, text=member.name, font=("Segoe UI", 13, "bold"), anchor="w").pack(fill="x")
            ctk.CTkLabel(info, text=f"ID: {member.member_id}  •  {len(member.borrowed_books)} book(s) borrowed",
                         font=FONT_SMALL, text_color="gray", anchor="w").pack(fill="x")


class MemberDashboard(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.app = app
        self.member = app.current_member
        self.view = "browse"

        self.sidebar = Sidebar(self, app, self.member.name,
                               [("browse", "📚  Browse"), ("mine", "🎒  My Books")], self._switch_view)
        self.sidebar.set_active("browse")

        self.content = ctk.CTkFrame(self, fg_color=("#F4F6F8", "#1A1A1A"))
        self.content.pack(side="left", fill="both", expand=True)

        self._render_browse_view()

    def _switch_view(self, key):
        self.view = key
        self.sidebar.set_active(key)
        for widget in self.content.winfo_children():
            widget.destroy()
        if key == "browse":
            self._render_browse_view()
        else:
            self._render_mine_view()

    def _render_browse_view(self):
        ctk.CTkLabel(self.content, text="Browse Books", font=FONT_TITLE).pack(anchor="w", padx=24, pady=(20, 10))

        search_bar = ctk.CTkFrame(self.content, fg_color="transparent")
        search_bar.pack(fill="x", padx=24, pady=(0, 10))
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *args: self._render_book_cards())
        search_entry = ctk.CTkEntry(search_bar, textvariable=self.search_var, width=320, height=36,
                                     placeholder_text="Search by title or author...")
        search_entry.pack(side="left")

        self.scroll = ctk.CTkScrollableFrame(self.content, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self._render_book_cards()

    def _render_book_cards(self):
        for widget in self.scroll.winfo_children():
            widget.destroy()
        self._card_refs = []

        query = self.search_var.get().strip().lower() if hasattr(self, "search_var") else ""
        books = [b for b in self.app.library.books
                 if query in b.title.lower() or query in b.author.lower()] if query else self.app.library.books

        col_count = 4
        for i, book in enumerate(books):
            if book.is_available:
                label, color, hover, cmd = "Borrow", "#2D7DD2", "#1B5FA3", (lambda b=book: self._borrow(b))
            else:
                label, color, hover, cmd = None, None, None, None
            card = BookCard(self.scroll, book, label, cmd, action_color=color or "#2D7DD2", action_hover=hover or "#1B5FA3")
            card.grid(row=i // col_count, column=i % col_count, padx=10, pady=10)
            self._card_refs.append(card)

        if not books and query:
            ctk.CTkLabel(self.scroll, text="No books match your search.",
                         font=FONT_BODY, text_color="gray").pack(pady=40)

    def _borrow(self, book):
        self.app.library.borrow_book(self.member.member_id, book.isbn)
        self.app.persist()
        self._render_book_cards()

    def _render_mine_view(self):
        ctk.CTkLabel(self.content, text="My Borrowed Books", font=FONT_TITLE).pack(anchor="w", padx=24, pady=(20, 10))
        self.scroll = ctk.CTkScrollableFrame(self.content, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self._render_mine_cards()

    def _render_mine_cards(self):
        for widget in self.scroll.winfo_children():
            widget.destroy()
        self._card_refs = []

        if not self.member.borrowed_books:
            ctk.CTkLabel(self.scroll, text="You haven't borrowed any books yet.",
                         font=FONT_BODY, text_color="gray").pack(pady=40)
            return

        col_count = 4
        for i, book in enumerate(self.member.borrowed_books):
            due_date = self.member.due_dates.get(book.isbn, "unknown")
            overdue = self.member.is_overdue(book.isbn)
            extra_text = f"Overdue! Was due {due_date}" if overdue else f"Due {due_date}"
            extra_color = "#D9534F" if overdue else "gray"
            card = BookCard(self.scroll, book, "Return", lambda b=book: self._return(b),
                             action_color="#D9534F", action_hover="#B33C39",
                             extra_text=extra_text, extra_text_color=extra_color)
            card.grid(row=i // col_count, column=i % col_count, padx=10, pady=10)
            self._card_refs.append(card)

    def _return(self, book):
        self.app.library.return_book(self.member.member_id, book.isbn)
        self.app.persist()
        self._render_mine_cards()


if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()