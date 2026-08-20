"""
CSV Storage & Export/Import Module
"""
import csv
import os
from typing import List, Dict, Any
from student_mgmt.utils.exceptions import StorageError


class CSVStorage:
    """Handles CSV export and import of student records."""

    FIELDNAMES = [
        "student_id",
        "roll_number",
        "first_name",
        "last_name",
        "email",
        "phone",
        "department",
        "date_of_birth",
        "status",
        "gpa",
        "created_at",
        "updated_at"
    ]

    @classmethod
    def export_to_csv(cls, records: List[Dict[str, Any]], export_path: str) -> str:
        """Exports a list of student dictionary records to a CSV file."""
        abs_path = os.path.abspath(export_path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        try:
            with open(abs_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=cls.FIELDNAMES, extrasaction="ignore")
                writer.writeheader()
                for rec in records:
                    writer.writerow(rec)
            return abs_path
        except Exception as e:
            raise StorageError(f"Failed to export students to CSV ({export_path}): {e}")

    @classmethod
    def import_from_csv(cls, import_path: str) -> List[Dict[str, Any]]:
        """Imports student records from a CSV file."""
        abs_path = os.path.abspath(import_path)
        if not os.path.exists(abs_path):
            raise StorageError(f"CSV file not found: {import_path}")

        records = []
        try:
            with open(abs_path, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get("roll_number") and row.get("first_name"):
                        rec = {
                            "student_id": row.get("student_id") or "",
                            "roll_number": row.get("roll_number", "").strip().upper(),
                            "first_name": row.get("first_name", "").strip(),
                            "last_name": row.get("last_name", "").strip(),
                            "email": row.get("email", "").strip().lower(),
                            "phone": row.get("phone", "").strip(),
                            "department": row.get("department", "Computer Science").strip(),
                            "date_of_birth": row.get("date_of_birth", "").strip(),
                            "status": row.get("status", "Active").strip(),
                            "enrolled_courses": []
                        }
                        records.append(rec)
            return records
        except Exception as e:
            raise StorageError(f"Failed to import students from CSV ({import_path}): {e}")
