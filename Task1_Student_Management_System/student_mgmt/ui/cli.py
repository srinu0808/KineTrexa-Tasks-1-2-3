"""
Command-Line Interface (CLI) Module for Student Management System
Provides an intuitive, menu-driven interactive terminal experience.
"""
import sys
import os
from typing import List
from student_mgmt.services.student_service import StudentService
from student_mgmt.models.student import Student
from student_mgmt.utils.exceptions import StudentSystemError

# Color helpers
class Colors:
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"


def print_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}========================================================================
   🎓 STUDENT MANAGEMENT SYSTEM - PYTHON OOP & PERSISTENCE
   Intern: KASARABOINA SRINU | App ID: KTS020260716223
========================================================================{Colors.RESET}"""
    print(banner)


class StudentCLI:
    def __init__(self, service: StudentService):
        self.service = service

    def display_students_table(self, students: List[Student]):
        """Displays student records in a clean tabular view."""
        if not students:
            print(f"{Colors.YELLOW}No student records found.{Colors.RESET}")
            return

        try:
            from tabulate import tabulate
            table_data = []
            for s in students:
                courses_count = len(s.enrolled_courses)
                table_data.append([
                    s.student_id,
                    s.roll_number,
                    s.full_name,
                    s.department,
                    s.email,
                    s.phone,
                    f"{s.gpa:.2f}",
                    courses_count,
                    s.status
                ])
            headers = ["ID", "Roll No", "Full Name", "Department", "Email", "Phone", "GPA", "Courses", "Status"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        except ImportError:
            # Fallback formatting if tabulate isn't available
            print("-" * 95)
            print(f"{'ID':<10} {'Roll No':<12} {'Full Name':<20} {'Dept':<15} {'GPA':<6} {'Status':<10}")
            print("-" * 95)
            for s in students:
                print(f"{s.student_id:<10} {s.roll_number:<12} {s.full_name[:18]:<20} {s.department[:13]:<15} {s.gpa:<6.2f} {s.status:<10}")
            print("-" * 95)

    def prompt_add_student(self):
        print(f"\n{Colors.BOLD}{Colors.GREEN}--- ➕ Add New Student ---{Colors.RESET}")
        roll_no = input("Enter Roll Number (e.g. CS202601): ").strip()
        first_name = input("Enter First Name: ").strip()
        last_name = input("Enter Last Name: ").strip()
        email = input("Enter Email Address: ").strip()
        phone = input("Enter Phone Number: ").strip()
        department = input("Enter Department (e.g. Computer Science, AI, ECE): ").strip()
        dob = input("Enter Date of Birth (YYYY-MM-DD) [Optional]: ").strip()
        status = input("Enter Status (Active/Inactive) [Default: Active]: ").strip() or "Active"

        try:
            student = self.service.create_student(
                roll_number=roll_no,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                department=department,
                date_of_birth=dob,
                status=status
            )
            print(f"{Colors.GREEN}✔ Successfully registered student: {student.full_name} (ID: {student.student_id}, Roll: {student.roll_number}){Colors.RESET}")
        except StudentSystemError as e:
            print(f"{Colors.RED}✖ Error: {e}{Colors.RESET}")

    def prompt_view_all(self):
        print(f"\n{Colors.BOLD}{Colors.CYAN}--- 📋 All Student Records ---{Colors.RESET}")
        print("Sort by: 1. Roll Number | 2. Name | 3. GPA (High-to-Low) | 4. Department")
        choice = input("Select sort option [1-4, Default: 1]: ").strip()
        
        sort_map = {"1": ("roll_number", False), "2": ("name", False), "3": ("gpa", True), "4": ("department", False)}
        sort_by, reverse = sort_map.get(choice, ("roll_number", False))

        students = self.service.get_all_students(sort_by=sort_by, reverse=reverse)
        print(f"\nTotal Records: {len(students)}")
        self.display_students_table(students)

    def prompt_search(self):
        print(f"\n{Colors.BOLD}{Colors.CYAN}--- 🔍 Search Students ---{Colors.RESET}")
        query = input("Enter search keyword (Roll No, Name, Dept, Email, Course): ").strip()
        results = self.service.search_students(query)
        print(f"\nFound {len(results)} matching records:")
        self.display_students_table(results)

    def prompt_filter(self):
        print(f"\n{Colors.BOLD}{Colors.CYAN}--- 🎯 Filter Students ---{Colors.RESET}")
        dept = input("Filter by Department (leave blank to skip): ").strip() or None
        status = input("Filter by Status (Active/Inactive, leave blank to skip): ").strip() or None
        min_gpa_in = input("Minimum GPA (0-10, leave blank to skip): ").strip()
        min_gpa = float(min_gpa_in) if min_gpa_in else None

        results = self.service.filter_students(department=dept, status=status, min_gpa=min_gpa)
        print(f"\nFound {len(results)} records matching filter criteria:")
        self.display_students_table(results)

    def prompt_view_details(self):
        print(f"\n{Colors.BOLD}{Colors.CYAN}--- 👤 View Student Profile & Courses ---{Colors.RESET}")
        ident = input("Enter Student ID or Roll Number: ").strip()
        try:
            student = self.service.get_student_by_roll_number(ident) if not ident.startswith("STU-") else self.service.get_student_by_id(ident)
        except StudentSystemError:
            try:
                student = self.service.get_student_by_id(ident)
            except StudentSystemError as e:
                print(f"{Colors.RED}✖ Error: {e}{Colors.RESET}")
                return

        print(f"\n{Colors.BOLD}Student Profile:{Colors.RESET}")
        print(f"  ID:            {student.student_id}")
        print(f"  Roll Number:   {student.roll_number}")
        print(f"  Name:          {student.full_name}")
        print(f"  Email:         {student.email}")
        print(f"  Phone:         {student.phone}")
        print(f"  Department:    {student.department}")
        print(f"  Date of Birth: {student.date_of_birth or 'N/A'}")
        print(f"  Status:        {student.status}")
        print(f"  Cumulative GPA:{Colors.GREEN} {student.gpa:.2f}{Colors.RESET}")
        print(f"  Enrolled Courses ({len(student.enrolled_courses)}):")
        if student.enrolled_courses:
            for idx, c in enumerate(student.enrolled_courses, 1):
                g_str = f"{c.grade_points:.1f}" if c.grade_points is not None else "Pending"
                print(f"    {idx}. [{c.course_code}] {c.course_name} ({c.credits} Credits, Sem {c.semester}) -> Grade: {g_str}")
        else:
            print("    (No courses currently enrolled)")

    def prompt_update_student(self):
        print(f"\n{Colors.BOLD}{Colors.YELLOW}--- ✏️ Update Student Information ---{Colors.RESET}")
        ident = input("Enter Student ID or Roll Number to update: ").strip()
        try:
            student = self.service.get_student_by_roll_number(ident) if not ident.startswith("STU-") else self.service.get_student_by_id(ident)
        except StudentSystemError:
            try:
                student = self.service.get_student_by_id(ident)
            except StudentSystemError as e:
                print(f"{Colors.RED}✖ Error: {e}{Colors.RESET}")
                return

        print(f"Updating details for: {student.full_name} (Press Enter to keep current value)")
        new_roll = input(f"Roll Number [{student.roll_number}]: ").strip() or None
        new_fname = input(f"First Name [{student.first_name}]: ").strip() or None
        new_lname = input(f"Last Name [{student.last_name}]: ").strip() or None
        new_email = input(f"Email [{student.email}]: ").strip() or None
        new_phone = input(f"Phone [{student.phone}]: ").strip() or None
        new_dept = input(f"Department [{student.department}]: ").strip() or None
        new_status = input(f"Status [{student.status}]: ").strip() or None

        try:
            updated = self.service.update_student(
                student_id=student.student_id,
                roll_number=new_roll,
                first_name=new_fname,
                last_name=new_lname,
                email=new_email,
                phone=new_phone,
                department=new_dept,
                status=new_status
            )
            print(f"{Colors.GREEN}✔ Successfully updated record for {updated.full_name}{Colors.RESET}")
        except StudentSystemError as e:
            print(f"{Colors.RED}✖ Update Failed: {e}{Colors.RESET}")

    def prompt_delete_student(self):
        print(f"\n{Colors.BOLD}{Colors.RED}--- 🗑️ Delete Student Record ---{Colors.RESET}")
        ident = input("Enter Student ID or Roll Number to delete: ").strip()
        confirm = input(f"Are you sure you want to delete record '{ident}'? (y/N): ").strip().lower()
        if confirm == 'y':
            try:
                deleted = self.service.delete_student(ident)
                print(f"{Colors.GREEN}✔ Successfully removed student: {deleted.full_name} ({deleted.roll_number}){Colors.RESET}")
            except StudentSystemError as e:
                print(f"{Colors.RED}✖ Delete Failed: {e}{Colors.RESET}")
        else:
            print("Operation cancelled.")

    def prompt_manage_courses(self):
        print(f"\n{Colors.BOLD}{Colors.CYAN}--- 📚 Course & Grade Management ---{Colors.RESET}")
        ident = input("Enter Student ID or Roll Number: ").strip()
        try:
            student = self.service.get_student_by_roll_number(ident) if not ident.startswith("STU-") else self.service.get_student_by_id(ident)
        except StudentSystemError as e:
            print(f"{Colors.RED}✖ Error: {e}{Colors.RESET}")
            return

        print(f"\nStudent: {student.full_name} (Current GPA: {student.gpa:.2f})")
        print("1. Enroll in new Course")
        print("2. Update Course Grade")
        print("3. Drop / Remove Course")
        sub_choice = input("Select an option [1-3]: ").strip()

        try:
            if sub_choice == "1":
                code = input("Course Code (e.g. CS101): ").strip()
                name = input("Course Name (e.g. Data Structures): ").strip()
                credits = int(input("Credits (e.g. 3 or 4): ").strip() or "3")
                sem = input("Semester [Default: 1]: ").strip() or "1"
                grade_in = input("Initial Grade Points (0-10, leave blank if in progress): ").strip()
                grade = float(grade_in) if grade_in else None
                self.service.enroll_course(student.student_id, code, name, credits, sem, grade)
                print(f"{Colors.GREEN}✔ Course {code} enrolled successfully.{Colors.RESET}")

            elif sub_choice == "2":
                code = input("Course Code to grade: ").strip()
                grade_val = float(input("Enter Grade Points (0.0 to 10.0): ").strip())
                self.service.update_grade(student.student_id, code, grade_val)
                print(f"{Colors.GREEN}✔ Grade updated. New GPA: {student.gpa:.2f}{Colors.RESET}")

            elif sub_choice == "3":
                code = input("Course Code to drop: ").strip()
                self.service.remove_course(student.student_id, code)
                print(f"{Colors.GREEN}✔ Course {code} dropped.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}✖ Course Operation Failed: {e}{Colors.RESET}")

    def prompt_analytics(self):
        print(f"\n{Colors.BOLD}{Colors.CYAN}--- 📊 System Analytics & Performance Report ---{Colors.RESET}")
        analytics = self.service.get_analytics()
        print(f"Total Enrolled Students:  {Colors.BOLD}{analytics['total_students']}{Colors.RESET}")
        print(f"Active Status:            {analytics['active_students']} | Inactive: {analytics['inactive_students']}")
        print(f"Overall Average GPA:      {Colors.GREEN}{analytics['average_gpa']:.2f}{Colors.RESET}")
        print("\nDepartment Breakdown:")
        for dept, count in analytics['department_counts'].items():
            print(f"  • {dept:<25}: {count} students")

        print("\n🏆 Top Academic Performers:")
        if analytics['top_performers']:
            for idx, p in enumerate(analytics['top_performers'], 1):
                print(f"  {idx}. {p['roll_number']} - {p['name']} ({p['department']}) -> GPA: {p['gpa']:.2f}")
        else:
            print("  No graded student records available yet.")

    def prompt_export_import(self):
        print(f"\n{Colors.BOLD}{Colors.CYAN}--- 💾 CSV Export & Import ---{Colors.RESET}")
        print("1. Export all students to CSV")
        print("2. Import students from CSV")
        choice = input("Select option [1-2]: ").strip()

        if choice == "1":
            default_path = os.path.join("data", "students_export.csv")
            path = input(f"Enter export path [Default: {default_path}]: ").strip() or default_path
            try:
                saved = self.service.export_csv(path)
                print(f"{Colors.GREEN}✔ Records successfully exported to: {saved}{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}✖ Export Failed: {e}{Colors.RESET}")
        elif choice == "2":
            path = input("Enter path of CSV to import: ").strip()
            try:
                count = self.service.import_csv(path)
                print(f"{Colors.GREEN}✔ Successfully imported {count} student records.{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}✖ Import Failed: {e}{Colors.RESET}")

    def run(self):
        while True:
            print_banner()
            print(f"{Colors.BOLD}Main Menu:{Colors.RESET}")
            print(f"  {Colors.GREEN}1.{Colors.RESET} Add Student Record")
            print(f"  {Colors.CYAN}2.{Colors.RESET} View All Students")
            print(f"  {Colors.CYAN}3.{Colors.RESET} Search Students")
            print(f"  {Colors.CYAN}4.{Colors.RESET} Filter Students (by Dept, GPA, Status)")
            print(f"  {Colors.CYAN}5.{Colors.RESET} View Student Profile & Enrolled Courses")
            print(f"  {Colors.YELLOW}6.{Colors.RESET} Update Student Details")
            print(f"  {Colors.YELLOW}7.{Colors.RESET} Manage Courses & Grades (GPA Calculation)")
            print(f"  {Colors.RED}8.{Colors.RESET} Delete Student Record")
            print(f"  {Colors.CYAN}9.{Colors.RESET} View System Analytics & Reports")
            print(f"  {Colors.BLUE}10.{Colors.RESET} CSV Data Export / Import")
            print(f"  {Colors.RED}0.{Colors.RESET} Exit")
            print("-" * 72)

            choice = input(f"{Colors.BOLD}Enter your choice [0-10]: {Colors.RESET}").strip()

            if choice == "1":
                self.prompt_add_student()
            elif choice == "2":
                self.prompt_view_all()
            elif choice == "3":
                self.prompt_search()
            elif choice == "4":
                self.prompt_filter()
            elif choice == "5":
                self.prompt_view_details()
            elif choice == "6":
                self.prompt_update_student()
            elif choice == "7":
                self.prompt_manage_courses()
            elif choice == "8":
                self.prompt_delete_student()
            elif choice == "9":
                self.prompt_analytics()
            elif choice == "10":
                self.prompt_export_import()
            elif choice == "0":
                print(f"\n{Colors.GREEN}Thank you for using Student Management System. Exiting...{Colors.RESET}\n")
                break
            else:
                print(f"{Colors.RED}Invalid selection. Please enter a number between 0 and 10.{Colors.RESET}")

            input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.RESET}")
