"""
Member Model Module
"""
from dataclasses import dataclass, asdict, field
from typing import List


@dataclass
class Member:
    member_id: str
    name: str
    email: str
    phone: str
    max_books_allowed: int = 3
    issued_books: List[str] = field(default_factory=list)  # List of ISBNs

    def can_borrow(self) -> bool:
        return len(self.issued_books) < self.max_books_allowed

    def add_issued_book(self, isbn: str) -> bool:
        if self.can_borrow() and isbn not in self.issued_books:
            self.issued_books.append(isbn)
            return True
        return False

    def remove_issued_book(self, isbn: str) -> bool:
        if isbn in self.issued_books:
            self.issued_books.remove(isbn)
            return True
        return False

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Member':
        return cls(
            member_id=data.get("member_id", "").strip().upper(),
            name=data.get("name", "").strip(),
            email=data.get("email", "").strip().lower(),
            phone=data.get("phone", "").strip(),
            max_books_allowed=int(data.get("max_books_allowed", 3)),
            issued_books=data.get("issued_books", [])
        )
