"""
Library Management System Interactive CLI
"""
import os
from library_mgmt.services.library_service import LibraryService

class Colors:
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


class LibraryCLI:
    def __init__(self, service: LibraryService):
        self.service = service

    def display_books(self, books):
        if not books:
            print(f"{Colors.YELLOW}No books found.{Colors.RESET}")
            return
        try:
            from tabulate import tabulate
            table_data = [[b.isbn, b.title, b.author, b.category, f"{b.available_copies}/{b.total_copies}", b.borrow_count] for b in books]
            print(tabulate(table_data, headers=["ISBN", "Title", "Author", "Category", "Available/Total", "Borrows"], tablefmt="grid"))
        except ImportError:
            for b in books:
                print(f"[{b.isbn}] {b.title} by {b.author} | Copies: {b.available_copies}/{b.total_copies}")

    def prompt_add_book(self):
        print(f"\n{Colors.BOLD}{Colors.GREEN}--- ➕ Add Book ---{Colors.RESET}")
        isbn = input("Enter ISBN (e.g. 978-0132350884): ").strip()
        title = input("Enter Book Title: ").strip()
        author = input("Enter Author: ").strip()
        cat = input("Enter Category [Default: General]: ").strip() or "General"
        copies = int(input("Enter Total Copies [Default: 1]: ").strip() or "1")
        try:
            b = self.service.add_book(isbn, title, author, cat, copies)
            print(f"{Colors.GREEN}✔ Book '{b.title}' added successfully.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}✖ Error: {e}{Colors.RESET}")

    def prompt_register_member(self):
        print(f"\n{Colors.BOLD}{Colors.GREEN}--- 👤 Register Member ---{Colors.RESET}")
        m_id = input("Enter Member ID (e.g. MEM-101): ").strip()
        name = input("Enter Full Name: ").strip()
        email = input("Enter Email: ").strip()
        phone = input("Enter Phone: ").strip()
        try:
            m = self.service.register_member(m_id, name, email, phone)
            print(f"{Colors.GREEN}✔ Registered member '{m.name}' (ID: {m.member_id}){Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}✖ Error: {e}{Colors.RESET}")

    def prompt_issue_book(self):
        print(f"\n{Colors.BOLD}{Colors.CYAN}--- 📖 Issue Book ---{Colors.RESET}")
        isbn = input("Enter Book ISBN: ").strip()
        m_id = input("Enter Member ID: ").strip()
        try:
            txn = self.service.issue_book(isbn, m_id)
            print(f"{Colors.GREEN}✔ Successfully issued book! Txn ID: {txn.transaction_id}, Due Date: {txn.due_date}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}✖ Issue Failed: {e}{Colors.RESET}")

    def prompt_return_book(self):
        print(f"\n{Colors.BOLD}{Colors.YELLOW}--- 🔄 Return Book ---{Colors.RESET}")
        isbn = input("Enter Book ISBN: ").strip()
        m_id = input("Enter Member ID: ").strip()
        try:
            txn = self.service.return_book(isbn, m_id)
            print(f"{Colors.GREEN}✔ Book returned successfully! Return Date: {txn.return_date}{Colors.RESET}")
            if txn.fine_amount > 0:
                print(f"{Colors.RED}⚠️ Overdue Fine Assessed: ${txn.fine_amount:.2f}{Colors.RESET}")
            else:
                print(f"{Colors.GREEN}✔ No fine assessed (returned on time).{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}✖ Return Failed: {e}{Colors.RESET}")

    def prompt_stats(self):
        print(f"\n{Colors.BOLD}{Colors.CYAN}--- 📊 Library Statistics ---{Colors.RESET}")
        stats = self.service.get_statistics()
        print(f"Total Unique Titles:   {stats['total_unique_titles']}")
        print(f"Total Physical Copies: {stats['total_copies']}")
        print(f"Currently Available:   {Colors.GREEN}{stats['available_copies']}{Colors.RESET}")
        print(f"Currently Borrowed:    {Colors.YELLOW}{stats['issued_copies']}{Colors.RESET}")
        print(f"Total Active Members:  {stats['total_members']}")
        print(f"Total Fines Collected: ${stats['total_fines_collected']:.2f}")

    def run(self):
        while True:
            print(f"\n{Colors.CYAN}{Colors.BOLD}========================================================================\n   📚 LIBRARY MANAGEMENT SYSTEM - INTERNSHIP TASK 2\n   Intern: KASARABOINA SRINU | App ID: KTS020260716223\n========================================================================{Colors.RESET}")
            print(f"  {Colors.GREEN}1.{Colors.RESET} Add Book")
            print(f"  {Colors.CYAN}2.{Colors.RESET} Search & View Books")
            print(f"  {Colors.GREEN}3.{Colors.RESET} Register Member")
            print(f"  {Colors.CYAN}4.{Colors.RESET} View All Members")
            print(f"  {Colors.BLUE}5.{Colors.RESET} Issue Book to Member")
            print(f"  {Colors.YELLOW}6.{Colors.RESET} Return Book (Calculate Overdue & Fine)")
            print(f"  {Colors.CYAN}7.{Colors.RESET} View Library Statistics & Most Popular Books")
            print(f"  {Colors.RED}0.{Colors.RESET} Exit")
            print("-" * 72)
            choice = input("Enter choice [0-7]: ").strip()

            if choice == "1":
                self.prompt_add_book()
            elif choice == "2":
                q = input("Search query (or press Enter for all): ").strip()
                books = self.service.search_books(q)
                self.display_books(books)
            elif choice == "3":
                self.prompt_register_member()
            elif choice == "4":
                members = self.service.list_members()
                for m in members:
                    print(f"[{m.member_id}] {m.name} ({m.email}) - Borrowed: {len(m.issued_books)}/{m.max_books_allowed}")
            elif choice == "5":
                self.prompt_issue_book()
            elif choice == "6":
                self.prompt_return_book()
            elif choice == "7":
                self.prompt_stats()
            elif choice == "0":
                print(f"\n{Colors.GREEN}Exiting Library System. Goodbye!{Colors.RESET}\n")
                break
            input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.RESET}")
