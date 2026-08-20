"""
Library Service Module
Handles core business logic: Books CRUD, Members CRUD, Issue/Return workflow, Overdue fines, and Analytics.
"""
from datetime import date, timedelta
from typing import List, Dict, Optional, Any
from library_mgmt.models.book import Book
from library_mgmt.models.member import Member
from library_mgmt.models.transaction import Transaction
from library_mgmt.storage.json_storage import LibraryStorage


class LibraryService:
    def __init__(self, storage: Optional[LibraryStorage] = None):
        self.storage = storage or LibraryStorage()
        self.books: Dict[str, Book] = {}
        self.members: Dict[str, Member] = {}
        self.transactions: List[Transaction] = []
        self._load()

    def _load(self):
        data = self.storage.load_data()
        self.books = {b["isbn"]: Book.from_dict(b) for b in data.get("books", [])}
        self.members = {m["member_id"]: Member.from_dict(m) for m in data.get("members", [])}
        self.transactions = [Transaction.from_dict(t) for t in data.get("transactions", [])]

    def _sync(self):
        data = {
            "books": [b.to_dict() for b in self.books.values()],
            "members": [m.to_dict() for m in self.members.values()],
            "transactions": [t.to_dict() for t in self.transactions]
        }
        self.storage.save_data(data)

    # --- Book Operations ---

    def add_book(self, isbn: str, title: str, author: str, category: str = "General", copies: int = 1) -> Book:
        isbn_clean = isbn.strip().upper()
        if not isbn_clean:
            raise ValueError("ISBN cannot be empty.")
        if isbn_clean in self.books:
            # Increase stock if book already exists
            book = self.books[isbn_clean]
            book.total_copies += copies
            book.available_copies += copies
        else:
            book = Book(
                isbn=isbn_clean,
                title=title.strip(),
                author=author.strip(),
                category=category.strip(),
                total_copies=copies,
                available_copies=copies
            )
            self.books[isbn_clean] = book
        self._sync()
        return book

    def get_book(self, isbn: str) -> Book:
        isbn_clean = isbn.strip().upper()
        if isbn_clean not in self.books:
            raise ValueError(f"Book with ISBN '{isbn_clean}' not found.")
        return self.books[isbn_clean]

    def search_books(self, query: str) -> List[Book]:
        q = query.strip().lower()
        if not q:
            return list(self.books.values())
        return [
            b for b in self.books.values()
            if q in b.isbn.lower() or q in b.title.lower() or q in b.author.lower() or q in b.category.lower()
        ]

    def delete_book(self, isbn: str) -> Book:
        isbn_clean = isbn.strip().upper()
        book = self.get_book(isbn_clean)
        if book.available_copies < book.total_copies:
            raise ValueError(f"Cannot delete book '{book.title}' because some copies are currently issued.")
        deleted = self.books.pop(isbn_clean)
        self._sync()
        return deleted

    # --- Member Operations ---

    def register_member(self, member_id: str, name: str, email: str, phone: str, max_books: int = 3) -> Member:
        m_id = member_id.strip().upper()
        if not m_id:
            raise ValueError("Member ID cannot be empty.")
        if m_id in self.members:
            raise ValueError(f"Member with ID '{m_id}' is already registered.")

        member = Member(
            member_id=m_id,
            name=name.strip(),
            email=email.strip().lower(),
            phone=phone.strip(),
            max_books_allowed=max_books
        )
        self.members[m_id] = member
        self._sync()
        return member

    def get_member(self, member_id: str) -> Member:
        m_id = member_id.strip().upper()
        if m_id not in self.members:
            raise ValueError(f"Member with ID '{m_id}' not found.")
        return self.members[m_id]

    def list_members(self) -> List[Member]:
        return list(self.members.values())

    # --- Issue & Return Workflow ---

    def issue_book(self, isbn: str, member_id: str, loan_days: int = 14) -> Transaction:
        book = self.get_book(isbn)
        member = self.get_member(member_id)

        if not book.is_available():
            raise ValueError(f"Book '{book.title}' is currently out of stock (0 copies available).")
        if not member.can_borrow():
            raise ValueError(f"Member '{member.name}' has reached their maximum quota of {member.max_books_allowed} books.")
        if book.isbn in member.issued_books:
            raise ValueError(f"Member has already borrowed a copy of '{book.title}'.")

        # Process issue
        book.borrow_copy()
        member.add_issued_book(book.isbn)

        issue_d = date.today()
        due_d = issue_d + timedelta(days=loan_days)
        trans_id = f"TXN-{len(self.transactions) + 1:04d}"

        transaction = Transaction(
            transaction_id=trans_id,
            isbn=book.isbn,
            member_id=member.member_id,
            issue_date=issue_d.isoformat(),
            due_date=due_d.isoformat(),
            status="Issued"
        )
        self.transactions.append(transaction)
        self._sync()
        return transaction

    def return_book(self, isbn: str, member_id: str, return_date_str: Optional[str] = None) -> Transaction:
        book = self.get_book(isbn)
        member = self.get_member(member_id)

        # Find active transaction
        active_tx = None
        for t in reversed(self.transactions):
            if t.isbn == book.isbn and t.member_id == member.member_id and t.status == "Issued":
                active_tx = t
                break

        if not active_tx:
            raise ValueError(f"No active loan record found for book '{book.title}' issued to '{member.name}'.")

        ret_date = return_date_str or date.today().isoformat()
        fine = active_tx.calculate_fine(return_date_str=ret_date)

        book.return_copy()
        member.remove_issued_book(book.isbn)

        active_tx.return_date = ret_date
        active_tx.fine_amount = fine
        active_tx.status = "Returned"

        self._sync()
        return active_tx

    # --- Analytics & Statistics ---

    def get_statistics(self) -> Dict[str, Any]:
        total_books = len(self.books)
        total_copies = sum(b.total_copies for b in self.books.values())
        available_copies = sum(b.available_copies for b in self.books.values())
        issued_copies = total_copies - available_copies
        total_members = len(self.members)
        total_fines = sum(t.fine_amount for t in self.transactions)
        popular_books = sorted(self.books.values(), key=lambda b: b.borrow_count, reverse=True)[:5]

        return {
            "total_unique_titles": total_books,
            "total_copies": total_copies,
            "available_copies": available_copies,
            "issued_copies": issued_copies,
            "total_members": total_members,
            "total_fines_collected": round(total_fines, 2),
            "popular_books": [
                {"isbn": b.isbn, "title": b.title, "author": b.author, "borrows": b.borrow_count}
                for b in popular_books if b.borrow_count > 0
            ]
        }
