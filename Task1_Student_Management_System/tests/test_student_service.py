"""
Unit & Integration Tests for Student Management System
"""
import os
import tempfile
import pytest

from student_mgmt.models.student import Student
from student_mgmt.models.course import Course
from student_mgmt.storage.json_storage import JSONStorage
from student_mgmt.services.student_service import StudentService
from student_mgmt.utils.exceptions import (
    StudentNotFoundError,
    DuplicateRollNumberError,
    DuplicateEmailError,
    ValidationError
)


@pytest.fixture
def temp_service():
    """Provides an isolated StudentService backed by a temporary file."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
        temp_path = tf.name

    storage = JSONStorage(file_path=temp_path)
    service = StudentService(storage=storage)
    yield service

    if os.path.exists(temp_path):
        os.remove(temp_path)


def test_create_student_success(temp_service):
    student = temp_service.create_student(
        roll_number="CS202610",
        first_name="Kasarabina",
        last_name="Srinu",
        email="srinu@example.com",
        phone="9876543210",
        department="Computer Science"
    )
    assert student.student_id.startswith("STU-")
    assert student.roll_number == "CS202610"
    assert student.full_name == "Kasarabina Srinu"
    assert student.email == "srinu@example.com"
    assert len(temp_service.get_all_students()) == 1


def test_duplicate_roll_number_error(temp_service):
    temp_service.create_student(
        roll_number="CS202610",
        first_name="Test",
        last_name="One",
        email="one@example.com",
        phone="9876543210",
        department="CS"
    )
    with pytest.raises(DuplicateRollNumberError):
        temp_service.create_student(
            roll_number="CS202610",
            first_name="Test",
            last_name="Two",
            email="two@example.com",
            phone="9876543211",
            department="CS"
        )


def test_duplicate_email_error(temp_service):
    temp_service.create_student(
        roll_number="CS202611",
        first_name="Test",
        last_name="One",
        email="same@example.com",
        phone="9876543210",
        department="CS"
    )
    with pytest.raises(DuplicateEmailError):
        temp_service.create_student(
            roll_number="CS202612",
            first_name="Test",
            last_name="Two",
            email="same@example.com",
            phone="9876543211",
            department="CS"
        )


def test_invalid_email_validation(temp_service):
    with pytest.raises(ValidationError):
        temp_service.create_student(
            roll_number="CS202613",
            first_name="Test",
            last_name="User",
            email="invalid-email-address",
            phone="9876543210",
            department="CS"
        )


def test_invalid_phone_validation(temp_service):
    with pytest.raises(ValidationError):
        temp_service.create_student(
            roll_number="CS202614",
            first_name="Test",
            last_name="User",
            email="valid@example.com",
            phone="123",  # Too short
            department="CS"
        )


def test_update_student(temp_service):
    student = temp_service.create_student(
        roll_number="CS202615",
        first_name="Original",
        last_name="Name",
        email="original@example.com",
        phone="9876543210",
        department="CS"
    )
    updated = temp_service.update_student(
        student_id=student.student_id,
        first_name="Updated",
        department="Data Science"
    )
    assert updated.first_name == "Updated"
    assert updated.department == "Data Science"
    assert updated.full_name == "Updated Name"


def test_delete_student(temp_service):
    student = temp_service.create_student(
        roll_number="CS202616",
        first_name="Delete",
        last_name="Me",
        email="delete@example.com",
        phone="9876543210",
        department="CS"
    )
    deleted = temp_service.delete_student(student.student_id)
    assert deleted.student_id == student.student_id
    assert len(temp_service.get_all_students()) == 0

    with pytest.raises(StudentNotFoundError):
        temp_service.get_student_by_id(student.student_id)


def test_course_enrollment_and_gpa_calculation(temp_service):
    student = temp_service.create_student(
        roll_number="CS202617",
        first_name="Grade",
        last_name="Test",
        email="grade@example.com",
        phone="9876543210",
        department="CS"
    )
    assert student.gpa == 0.0

    temp_service.enroll_course(student.student_id, "CS101", "Python", credits=4, grade_points=9.0)
    temp_service.enroll_course(student.student_id, "CS102", "Maths", credits=4, grade_points=7.0)

    # GPA should be (4*9.0 + 4*7.0) / (4+4) = (36 + 28) / 8 = 64/8 = 8.0
    student_refreshed = temp_service.get_student_by_id(student.student_id)
    assert student_refreshed.gpa == 8.0


def test_search_and_filter(temp_service):
    temp_service.create_student(
        roll_number="AI202601",
        first_name="Elon",
        last_name="Musk",
        email="elon@ai.com",
        phone="9876543210",
        department="Artificial Intelligence"
    )
    temp_service.create_student(
        roll_number="CS202602",
        first_name="Linus",
        last_name="Torvalds",
        email="linus@linux.org",
        phone="9876543211",
        department="Computer Science"
    )

    search_res = temp_service.search_students("Linus")
    assert len(search_res) == 1
    assert search_res[0].first_name == "Linus"

    filter_res = temp_service.filter_students(department="Artificial Intelligence")
    assert len(filter_res) == 1
    assert filter_res[0].roll_number == "AI202601"
