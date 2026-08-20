"""
Library Management System Entry Point
Internship Assignment - Task 2
Applicant: KASARABOINA SRINU | Application ID: KTS020260716223
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from library_mgmt.storage.json_storage import LibraryStorage
from library_mgmt.services.library_service import LibraryService
from library_mgmt.ui.cli import LibraryCLI


def seed_library_sample(service: LibraryService):
    if len(service.books) == 0:
        b1 = service.add_book("978-0132350884", "Clean Code", "Robert C. Martin", "Software Engineering", 5)
        b2 = service.add_book("978-0134685991", "Effective Java", "Joshua Bloch", "Programming", 3)
        b3 = service.add_book("978-0596007126", "Head First Design Patterns", "Eric Freeman", "Architecture", 4)
        b4 = service.add_book("978-1449355730", "Learning Python", "Mark Lutz", "Programming", 6)

        m1 = service.register_member("MEM-101", "Srinu Kasaraboina", "srinu@example.com", "9876543210")
        m2 = service.register_member("MEM-102", "Priya Sharma", "priya@example.com", "9876543211")

        service.issue_book(b1.isbn, m1.member_id)
        service.issue_book(b4.isbn, m2.member_id)


def main():
    data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "library_data.json")
    storage = LibraryStorage(file_path=data_file)
    service = LibraryService(storage=storage)

    seed_library_sample(service)

    cli = LibraryCLI(service=service)
    cli.run()


if __name__ == "__main__":
    main()
