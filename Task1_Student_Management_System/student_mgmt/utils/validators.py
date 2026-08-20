"""
Validation utilities for Student Management System
"""
import re
from student_mgmt.utils.exceptions import ValidationError


def validate_email(email: str) -> str:
    """Validates email format using regex."""
    if not email or not isinstance(email, str):
        raise ValidationError("Email address cannot be empty.", field="email")
    email = email.strip()
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(pattern, email):
        raise ValidationError(f"Invalid email format: '{email}'", field="email")
    return email.lower()


def validate_phone(phone: str) -> str:
    """Validates phone number format."""
    if not phone or not isinstance(phone, str):
        raise ValidationError("Phone number cannot be empty.", field="phone")
    phone_clean = re.sub(r"[\s\-\(\)\+]", "", phone.strip())
    if not phone_clean.isdigit() or len(phone_clean) < 7 or len(phone_clean) > 15:
        raise ValidationError(
            f"Invalid phone number '{phone}'. Phone must contain between 7 to 15 digits.",
            field="phone"
        )
    return phone.strip()


def validate_roll_number(roll_no: str) -> str:
    """Validates roll number formatting."""
    if not roll_no or not isinstance(roll_no, str):
        raise ValidationError("Roll number cannot be empty.", field="roll_number")
    roll_clean = roll_no.strip().upper()
    if len(roll_clean) < 2 or len(roll_clean) > 20:
        raise ValidationError(
            "Roll number must be between 2 and 20 alphanumeric characters.",
            field="roll_number"
        )
    return roll_clean


def validate_non_empty(value: str, field_name: str) -> str:
    """Validates that a string value is not empty or whitespace."""
    if not value or not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{field_name} cannot be empty.", field=field_name)
    return value.strip()


def validate_grade_points(points: float) -> float:
    """Validates grade points on a scale of 0.0 to 10.0 or 4.0."""
    try:
        val = float(points)
    except (ValueError, TypeError):
        raise ValidationError("Grade points must be a valid numeric value.")
    if val < 0.0 or val > 10.0:
        raise ValidationError(f"Grade points must be between 0.0 and 10.0 (received {val}).")
    return round(val, 2)
