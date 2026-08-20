"""
Unit Tests for Library Management System
"""
import os
import tempfile
import pytest

from library_mgmt.models.book import Book
from library_mgmt.models.member import Member
from library_mgmt.storage.json_storage import LibraryStorage
from library_mgmt.services.library_service import LibraryService


@pytest.fixture
def library_service():
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
        temp_path = tf.name

    storage = LibraryStorage(file_path=temp_path)
    service = LibraryService(storage=storage)
    yield service

    if os.path.exists(temp_path):
        os.remove(temp_path)


def test_add_and_search_books(library_service):
    b = library_service.add_book("ISBN-100", "Design Patterns", "GoF", "Architecture", 3)
    assert b.isbn == "ISBN-100"
    assert b.available_copies == 3

    results = library_service.search_books("Patterns")
    assert len(results) == 1
    assert results[0].title == "Design Patterns"


def test_member_registration(library_service):
    m = library_service.register_member("MEM-01", "Kasara Boina Srinu", "srinu@example.com", "9876543210")
    assert m.member_id == "MEM-01"
    assert m.can_borrow() is True


def test_issue_and_return_workflow(library_service):
    b = library_service.add_book("ISBN-200", "Clean Architecture", "Robert Martin", "Software", 1)
    m = library_service.register_member("MEM-02", "Alex", "alex@example.com", "1234567890")

    # Issue book
    txn = library_service.issue_book("ISBN-200", "MEM-02")
    assert txn.status == "Issued"
    assert b.available_copies == 0
    assert "ISBN-200" in m.issued_books

    # Attempt to issue already out-of-stock book
    with pytest.raises(ValueError):
        library_service.issue_book("ISBN-200", "MEM-02")

    # Return book
    ret_txn = library_service.return_book("ISBN-200", "MEM-02")
    assert ret_txn.status == "Returned"
    assert b.available_copies == 1
    assert "ISBN-200" not in m.issued_books


def test_fine_calculation_on_overdue(library_service):
    b = library_service.add_book("ISBN-300", "Refactoring", "Martin Fowler", "Software", 2)
    m = library_service.register_member("MEM-03", "Sam", "sam@example.com", "9876543219")

    txn = library_service.issue_book("ISBN-300", "MEM-03")
    # Simulate return 5 days after due date
    from datetime import datetime, timedelta
    due = datetime.strptime(txn.due_date, "%Y-%m-%d").date()
    overdue_return = (due + timedelta(days=5)).isoformat()

    ret_txn = library_service.return_book("ISBN-300", "MEM-03", return_date_str=overdue_return)
    assert ret_txn.fine_amount == 10.0  # 5 days * $2.0/day
