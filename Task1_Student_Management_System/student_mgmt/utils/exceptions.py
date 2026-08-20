"""
Custom Exception Classes for Student Management System
"""

class StudentSystemError(Exception):
    """Base exception for all system-related errors."""
    pass


class StudentNotFoundError(StudentSystemError):
    """Raised when a requested student is not found."""
    def __init__(self, identifier: str):
        super().__init__(f"Student with identifier '{identifier}' was not found.")
        self.identifier = identifier


class DuplicateRollNumberError(StudentSystemError):
    """Raised when attempting to add/update a student with an already existing roll number."""
    def __init__(self, roll_number: str):
        super().__init__(f"A student with Roll Number '{roll_number}' already exists.")
        self.roll_number = roll_number


class DuplicateEmailError(StudentSystemError):
    """Raised when attempting to use an already registered email."""
    def __init__(self, email: str):
        super().__init__(f"A student with Email '{email}' already exists.")
        self.email = email


class ValidationError(StudentSystemError):
    """Raised when data validation fails."""
    def __init__(self, message: str, field: str = None):
        super().__init__(message)
        self.field = field


class StorageError(StudentSystemError):
    """Raised when file input/output or persistence fails."""
    pass
