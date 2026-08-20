"""
Student Management System Entry Point
Internship Assignment - Task 1
Applicant: KASARABOINA SRINU | Application ID: KTS020260716223
"""
import sys
import os

# Add root directory to python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from student_mgmt.storage.json_storage import JSONStorage
from student_mgmt.services.student_service import StudentService
from student_mgmt.ui.cli import StudentCLI


def seed_sample_data(service: StudentService):
    """Populates realistic sample data if the system is fresh."""
    if len(service.get_all_students()) == 0:
        sample_students = [
            ("CS202601", "Aarav", "Sharma", "aarav.sharma@example.com", "9876543210", "Computer Science", "2002-05-14"),
            ("CS202602", "Ananya", "Reddy", "ananya.reddy@example.com", "9876543211", "Computer Science", "2003-08-22"),
            ("AI202603", "Rohan", "Verma", "rohan.verma@example.com", "9876543212", "Artificial Intelligence", "2002-11-09"),
            ("EC202604", "Priya", "Nair", "priya.nair@example.com", "9876543213", "Electronics & Comm", "2003-02-17"),
            ("AI202605", "Vikram", "Patel", "vikram.patel@example.com", "9876543214", "Artificial Intelligence", "2002-09-30"),
        ]

        for roll, fname, lname, email, phone, dept, dob in sample_students:
            s = service.create_student(
                roll_number=roll,
                first_name=fname,
                last_name=lname,
                email=email,
                phone=phone,
                department=dept,
                date_of_birth=dob
            )
            # Add sample courses and grades
            if roll == "CS202601":
                service.enroll_course(s.student_id, "CS101", "Python Programming", 4, "1", 9.5)
                service.enroll_course(s.student_id, "CS102", "Data Structures", 4, "1", 9.0)
            elif roll == "CS202602":
                service.enroll_course(s.student_id, "CS101", "Python Programming", 4, "1", 8.5)
                service.enroll_course(s.student_id, "CS103", "Database Systems", 3, "1", 8.8)
            elif roll == "AI202603":
                service.enroll_course(s.student_id, "AI101", "Machine Learning Basics", 4, "1", 9.8)
                service.enroll_course(s.student_id, "AI102", "Deep Learning", 4, "1", 9.6)
            elif roll == "EC202604":
                service.enroll_course(s.student_id, "EC101", "Digital Electronics", 4, "1", 8.2)


def main():
    data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "students.json")
    storage = JSONStorage(file_path=data_file)
    service = StudentService(storage=storage)

    # Seed initial demo records if storage is empty
    seed_sample_data(service)

    cli = StudentCLI(service=service)
    cli.run()


if __name__ == "__main__":
    main()
