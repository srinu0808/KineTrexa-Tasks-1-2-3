"""
Book Model Module
"""
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Book:
    isbn: str
    title: str
    author: str
    category: str
    total_copies: int = 1
    available_copies: int = 1
    borrow_count: int = 0

    def is_available(self) -> bool:
        return self.available_copies > 0

    def borrow_copy(self) -> bool:
        if self.available_copies > 0:
            self.available_copies -= 1
            self.borrow_count += 1
            return True
        return False

    def return_copy(self) -> bool:
        if self.available_copies < self.total_copies:
            self.available_copies += 1
            return True
        return False

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Book':
        return cls(
            isbn=data.get("isbn", "").strip().upper(),
            title=data.get("title", "").strip(),
            author=data.get("author", "").strip(),
            category=data.get("category", "General").strip(),
            total_copies=int(data.get("total_copies", 1)),
            available_copies=int(data.get("available_copies", 1)),
            borrow_count=int(data.get("borrow_count", 0))
        )
