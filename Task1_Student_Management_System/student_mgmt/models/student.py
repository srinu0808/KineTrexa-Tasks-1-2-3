"""
Student Model Module
Implements OOP principles (Encapsulation, Data abstraction, Methods) for Student entities.
"""
from datetime import datetime
from typing import List, Dict, Any, Optional
from student_mgmt.models.course import Course


class Student:
    """
    Represents a student in the educational management system.
    """
    def __init__(
        self,
        student_id: str,
        roll_number: str,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        department: str,
        date_of_birth: str = "",
        status: str = "Active",
        enrolled_courses: Optional[List[Course]] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None
    ):
        self._student_id = student_id.strip()
        self._roll_number = roll_number.strip().upper()
        self._first_name = first_name.strip()
        self._last_name = last_name.strip()
        self._email = email.strip().lower()
        self._phone = phone.strip()
        self._department = department.strip()
        self._date_of_birth = date_of_birth.strip()
        self._status = status.strip()
        self._enrolled_courses: List[Course] = enrolled_courses if enrolled_courses is not None else []
        self._created_at = created_at or datetime.now().isoformat()
        self._updated_at = updated_at or datetime.now().isoformat()

    # Properties for Encapsulation
    @property
    def student_id(self) -> str:
        return self._student_id

    @property
    def roll_number(self) -> str:
        return self._roll_number

    @roll_number.setter
    def roll_number(self, value: str):
        self._roll_number = value.strip().upper()
        self._mark_updated()

    @property
    def full_name(self) -> str:
        return f"{self._first_name} {self._last_name}".strip()

    @property
    def first_name(self) -> str:
        return self._first_name

    @first_name.setter
    def first_name(self, value: str):
        self._first_name = value.strip()
        self._mark_updated()

    @property
    def last_name(self) -> str:
        return self._last_name

    @last_name.setter
    def last_name(self, value: str):
        self._last_name = value.strip()
        self._mark_updated()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        self._email = value.strip().lower()
        self._mark_updated()

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str):
        self._phone = value.strip()
        self._mark_updated()

    @property
    def department(self) -> str:
        return self._department

    @department.setter
    def department(self, value: str):
        self._department = value.strip()
        self._mark_updated()

    @property
    def date_of_birth(self) -> str:
        return self._date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, value: str):
        self._date_of_birth = value.strip()
        self._mark_updated()

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        self._status = value.strip()
        self._mark_updated()

    @property
    def enrolled_courses(self) -> List[Course]:
        return list(self._enrolled_courses)

    @property
    def created_at(self) -> str:
        return self._created_at

    @property
    def updated_at(self) -> str:
        return self._updated_at

    def _mark_updated(self):
        self._updated_at = datetime.now().isoformat()

    # Domain methods
    def add_course(self, course: Course) -> bool:
        """Adds a course if not already enrolled."""
        for c in self._enrolled_courses:
            if c.course_code.upper() == course.course_code.upper():
                return False
        self._enrolled_courses.append(course)
        self._mark_updated()
        return True

    def remove_course(self, course_code: str) -> bool:
        """Removes a course by its code."""
        code_upper = course_code.strip().upper()
        initial_len = len(self._enrolled_courses)
        self._enrolled_courses = [c for c in self._enrolled_courses if c.course_code.upper() != code_upper]
        if len(self._enrolled_courses) < initial_len:
            self._mark_updated()
            return True
        return False

    def update_course_grade(self, course_code: str, grade_points: float) -> bool:
        """Updates grade for a specific enrolled course."""
        code_upper = course_code.strip().upper()
        for course in self._enrolled_courses:
            if course.course_code.upper() == code_upper:
                course.grade_points = grade_points
                self._mark_updated()
                return True
        return False

    @property
    def gpa(self) -> float:
        """Calculates cumulative GPA (Weighted Average based on credits)."""
        graded_courses = [c for c in self._enrolled_courses if c.grade_points is not None]
        if not graded_courses:
            return 0.0
        total_points = sum(c.grade_points * c.credits for c in graded_courses)
        total_credits = sum(c.credits for c in graded_courses)
        return round(total_points / total_credits, 2) if total_credits > 0 else 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Serializes Student object to dictionary format."""
        return {
            "student_id": self._student_id,
            "roll_number": self._roll_number,
            "first_name": self._first_name,
            "last_name": self._last_name,
            "email": self._email,
            "phone": self._phone,
            "department": self._department,
            "date_of_birth": self._date_of_birth,
            "status": self._status,
            "enrolled_courses": [c.to_dict() for c in self._enrolled_courses],
            "gpa": self.gpa,
            "created_at": self._created_at,
            "updated_at": self._updated_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Student':
        """Constructs a Student instance from a dictionary."""
        courses_data = data.get("enrolled_courses", [])
        courses = [Course.from_dict(c) for c in courses_data] if courses_data else []
        return cls(
            student_id=data.get("student_id", ""),
            roll_number=data.get("roll_number", ""),
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            email=data.get("email", ""),
            phone=data.get("phone", ""),
            department=data.get("department", "Computer Science"),
            date_of_birth=data.get("date_of_birth", ""),
            status=data.get("status", "Active"),
            enrolled_courses=courses,
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )

    def __str__(self) -> str:
        return f"[{self.roll_number}] {self.full_name} - Dept: {self.department} | GPA: {self.gpa:.2f} | Status: {self.status}"

    def __repr__(self) -> str:
        return f"Student(id='{self.student_id}', roll='{self.roll_number}', name='{self.full_name}')"
