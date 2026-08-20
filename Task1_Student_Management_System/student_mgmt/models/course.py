"""
Course Model Module
Defines the Course data structure representing academic courses enrolled by students.
"""
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Course:
    course_code: str
    course_name: str
    credits: int
    grade_points: Optional[float] = None
    semester: str = "1"

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Course':
        return cls(
            course_code=data.get("course_code", "").strip().upper(),
            course_name=data.get("course_name", "").strip(),
            credits=int(data.get("credits", 3)),
            grade_points=float(data["grade_points"]) if data.get("grade_points") is not None else None,
            semester=str(data.get("semester", "1"))
        )

    def __str__(self) -> str:
        grade_str = f"{self.grade_points:.1f}" if self.grade_points is not None else "N/A"
        return f"{self.course_code}: {self.course_name} ({self.credits} cr) - Grade: {grade_str}"
