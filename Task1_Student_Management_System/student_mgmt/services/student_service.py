"""
Student Service Module
Core business logic for managing student records, CRUD, search, filter, and analytics.
"""
import uuid
from typing import List, Optional, Dict, Any
from collections import defaultdict

from student_mgmt.models.student import Student
from student_mgmt.models.course import Course
from student_mgmt.storage.base import BaseStorage
from student_mgmt.storage.json_storage import JSONStorage
from student_mgmt.storage.csv_storage import CSVStorage
from student_mgmt.utils.exceptions import (
    StudentNotFoundError,
    DuplicateRollNumberError,
    DuplicateEmailError,
    ValidationError
)
from student_mgmt.utils.validators import (
    validate_email,
    validate_phone,
    validate_roll_number,
    validate_non_empty,
    validate_grade_points
)


class StudentService:
    """
    Service layer encapsulating business logic for student management.
    """
    def __init__(self, storage: Optional[BaseStorage] = None):
        self.storage = storage or JSONStorage()
        self._students: Dict[str, Student] = {}
        self._load_cache()

    def _load_cache(self):
        """Loads data from storage into memory cache."""
        records = self.storage.load_all()
        self._students = {}
        for r in records:
            student = Student.from_dict(r)
            self._students[student.student_id] = student

    def _sync(self):
        """Persists current state to storage."""
        records = [s.to_dict() for s in self._students.values()]
        self.storage.save_all(records)

    def _generate_student_id(self) -> str:
        """Generates a clean unique student ID."""
        existing_ids = {s.student_id for s in self._students.values()}
        counter = len(existing_ids) + 1
        new_id = f"STU-{counter:04d}"
        while new_id in existing_ids:
            counter += 1
            new_id = f"STU-{counter:04d}"
        return new_id

    # --- CRUD Operations ---

    def create_student(
        self,
        roll_number: str,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        department: str,
        date_of_birth: str = "",
        status: str = "Active"
    ) -> Student:
        """Creates and persists a new student after validation and duplicate checks."""
        roll_no = validate_roll_number(roll_number)
        f_name = validate_non_empty(first_name, "First Name")
        l_name = validate_non_empty(last_name, "Last Name")
        v_email = validate_email(email)
        v_phone = validate_phone(phone)
        dept = validate_non_empty(department, "Department")

        # Duplicate Checks
        for s in self._students.values():
            if s.roll_number.upper() == roll_no.upper():
                raise DuplicateRollNumberError(roll_no)
            if s.email.lower() == v_email.lower():
                raise DuplicateEmailError(v_email)

        student_id = self._generate_student_id()
        student = Student(
            student_id=student_id,
            roll_number=roll_no,
            first_name=f_name,
            last_name=l_name,
            email=v_email,
            phone=v_phone,
            department=dept,
            date_of_birth=date_of_birth,
            status=status
        )

        self._students[student_id] = student
        self._sync()
        return student

    def get_student_by_id(self, student_id: str) -> Student:
        """Retrieves student by ID."""
        if student_id not in self._students:
            raise StudentNotFoundError(student_id)
        return self._students[student_id]

    def get_student_by_roll_number(self, roll_number: str) -> Student:
        """Retrieves student by Roll Number."""
        roll_clean = roll_number.strip().upper()
        for s in self._students.values():
            if s.roll_number == roll_clean:
                return s
        raise StudentNotFoundError(roll_number)

    def get_all_students(self, sort_by: str = "roll_number", reverse: bool = False) -> List[Student]:
        """Returns all students sorted by specified field."""
        students = list(self._students.values())
        if sort_by == "roll_number":
            students.sort(key=lambda s: s.roll_number, reverse=reverse)
        elif sort_by == "name":
            students.sort(key=lambda s: s.full_name.lower(), reverse=reverse)
        elif sort_by == "gpa":
            students.sort(key=lambda s: s.gpa, reverse=reverse)
        elif sort_by == "department":
            students.sort(key=lambda s: s.department.lower(), reverse=reverse)
        elif sort_by == "created_at":
            students.sort(key=lambda s: s.created_at, reverse=reverse)
        return students

    def update_student(
        self,
        student_id: str,
        roll_number: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        department: Optional[str] = None,
        date_of_birth: Optional[str] = None,
        status: Optional[str] = None
    ) -> Student:
        """Updates student details after validating new values and ensuring uniqueness."""
        student = self.get_student_by_id(student_id)

        if roll_number is not None:
            new_roll = validate_roll_number(roll_number)
            for sid, s in self._students.items():
                if sid != student_id and s.roll_number.upper() == new_roll.upper():
                    raise DuplicateRollNumberError(new_roll)
            student.roll_number = new_roll

        if email is not None:
            new_email = validate_email(email)
            for sid, s in self._students.items():
                if sid != student_id and s.email.lower() == new_email.lower():
                    raise DuplicateEmailError(new_email)
            student.email = new_email

        if first_name is not None:
            student.first_name = validate_non_empty(first_name, "First Name")

        if last_name is not None:
            student.last_name = validate_non_empty(last_name, "Last Name")

        if phone is not None:
            student.phone = validate_phone(phone)

        if department is not None:
            student.department = validate_non_empty(department, "Department")

        if date_of_birth is not None:
            student.date_of_birth = date_of_birth.strip()

        if status is not None:
            student.status = status.strip()

        self._sync()
        return student

    def delete_student(self, identifier: str) -> Student:
        """Deletes a student by ID or Roll Number."""
        target_id = None
        if identifier in self._students:
            target_id = identifier
        else:
            for sid, s in self._students.items():
                if s.roll_number.upper() == identifier.strip().upper():
                    target_id = sid
                    break

        if not target_id:
            raise StudentNotFoundError(identifier)

        deleted = self._students.pop(target_id)
        self._sync()
        return deleted

    # --- Search & Filter ---

    def search_students(self, query: str) -> List[Student]:
        """Searches students across multiple attributes (Name, Roll, Email, Department)."""
        q = query.strip().lower()
        if not q:
            return self.get_all_students()

        results = []
        for s in self._students.values():
            if (
                q in s.roll_number.lower()
                or q in s.full_name.lower()
                or q in s.email.lower()
                or q in s.phone.lower()
                or q in s.department.lower()
                or any(q in c.course_name.lower() or q in c.course_code.lower() for c in s.enrolled_courses)
            ):
                results.append(s)
        return results

    def filter_students(
        self,
        department: Optional[str] = None,
        status: Optional[str] = None,
        min_gpa: Optional[float] = None,
        max_gpa: Optional[float] = None
    ) -> List[Student]:
        """Filters students matching specific criteria."""
        results = list(self._students.values())

        if department and department.strip():
            dept_lower = department.strip().lower()
            results = [s for s in results if s.department.lower() == dept_lower]

        if status and status.strip():
            status_lower = status.strip().lower()
            results = [s for s in results if s.status.lower() == status_lower]

        if min_gpa is not None:
            results = [s for s in results if s.gpa >= min_gpa]

        if max_gpa is not None:
            results = [s for s in results if s.gpa <= max_gpa]

        return results

    # --- Course & Grade Management ---

    def enroll_course(
        self,
        student_id: str,
        course_code: str,
        course_name: str,
        credits: int,
        semester: str = "1",
        grade_points: Optional[float] = None
    ) -> Course:
        """Enrolls a student in a course."""
        student = self.get_student_by_id(student_id)
        c_code = validate_non_empty(course_code, "Course Code").upper()
        c_name = validate_non_empty(course_name, "Course Name")
        if credits <= 0:
            raise ValidationError("Credits must be a positive integer.")
        if grade_points is not None:
            grade_points = validate_grade_points(grade_points)

        course = Course(
            course_code=c_code,
            course_name=c_name,
            credits=credits,
            grade_points=grade_points,
            semester=semester
        )
        if not student.add_course(course):
            raise ValidationError(f"Student is already enrolled in course {c_code}.")
        self._sync()
        return course

    def update_grade(self, student_id: str, course_code: str, grade_points: float) -> bool:
        """Updates a student's grade for a course."""
        student = self.get_student_by_id(student_id)
        validated_grade = validate_grade_points(grade_points)
        if not student.update_course_grade(course_code, validated_grade):
            raise ValidationError(f"Course '{course_code}' not found in student enrollment list.")
        self._sync()
        return True

    def remove_course(self, student_id: str, course_code: str) -> bool:
        """Removes a course enrollment for a student."""
        student = self.get_student_by_id(student_id)
        if not student.remove_course(course_code):
            raise ValidationError(f"Course '{course_code}' is not enrolled by this student.")
        self._sync()
        return True

    # --- Analytics & Reporting ---

    def get_analytics(self) -> Dict[str, Any]:
        """Calculates system metrics, department distribution, GPA averages."""
        total_students = len(self._students)
        if total_students == 0:
            return {
                "total_students": 0,
                "active_students": 0,
                "inactive_students": 0,
                "average_gpa": 0.0,
                "department_counts": {},
                "top_performers": []
            }

        active_count = sum(1 for s in self._students.values() if s.status.lower() == "active")
        inactive_count = total_students - active_count
        all_gpas = [s.gpa for s in self._students.values() if s.gpa > 0]
        avg_gpa = round(sum(all_gpas) / len(all_gpas), 2) if all_gpas else 0.0

        dept_counts = defaultdict(int)
        for s in self._students.values():
            dept_counts[s.department] += 1

        top_performers = sorted(self._students.values(), key=lambda s: s.gpa, reverse=True)[:5]

        return {
            "total_students": total_students,
            "active_students": active_count,
            "inactive_students": inactive_count,
            "average_gpa": avg_gpa,
            "department_counts": dict(dept_counts),
            "top_performers": [
                {
                    "roll_number": s.roll_number,
                    "name": s.full_name,
                    "department": s.department,
                    "gpa": s.gpa
                }
                for s in top_performers if s.gpa > 0
            ]
        }

    # --- Import / Export ---

    def export_csv(self, file_path: str = "data/students_export.csv") -> str:
        """Exports all records to CSV."""
        records = [s.to_dict() for s in self._students.values()]
        return CSVStorage.export_to_csv(records, file_path)

    def import_csv(self, file_path: str) -> int:
        """Imports students from CSV, skipping duplicates."""
        records = CSVStorage.import_from_csv(file_path)
        imported_count = 0
        for r in records:
            try:
                self.create_student(
                    roll_number=r["roll_number"],
                    first_name=r["first_name"],
                    last_name=r["last_name"],
                    email=r["email"],
                    phone=r["phone"],
                    department=r["department"],
                    date_of_birth=r["date_of_birth"],
                    status=r["status"]
                )
                imported_count += 1
            except (DuplicateRollNumberError, DuplicateEmailError, ValidationError):
                # Skip duplicate or invalid rows
                continue
        return imported_count
