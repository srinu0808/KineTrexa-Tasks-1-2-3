"""
JSON Storage Module
Handles robust JSON file reading and writing with atomic save and backup.
"""
import json
import os
import shutil
from typing import List, Dict, Any
from student_mgmt.storage.base import BaseStorage
from student_mgmt.utils.exceptions import StorageError


class JSONStorage(BaseStorage):
    """
    JSON file implementation of the storage layer.
    """
    def __init__(self, file_path: str = "data/students.json"):
        self.file_path = os.path.abspath(file_path)
        self._ensure_directory()

    def _ensure_directory(self):
        """Ensures directory exists and file is initialized."""
        directory = os.path.dirname(self.file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)

    def load_all(self) -> List[Dict[str, Any]]:
        """Loads records from JSON file with error handling."""
        self._ensure_directory()
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return []
                data = json.loads(content)
                if isinstance(data, list):
                    return data
                return []
        except json.JSONDecodeError as e:
            # Backup corrupted file
            backup_path = f"{self.file_path}.corrupted_{os.getpid()}"
            try:
                shutil.copyfile(self.file_path, backup_path)
            except Exception:
                pass
            raise StorageError(f"Error parsing JSON data from {self.file_path}: {e}")
        except Exception as e:
            raise StorageError(f"Failed to load data from {self.file_path}: {e}")

    def save_all(self, records: List[Dict[str, Any]]) -> bool:
        """Persists records atomically via temporary file replacement."""
        self._ensure_directory()
        temp_file = f"{self.file_path}.tmp"
        try:
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(records, f, indent=4, ensure_ascii=False)
            
            # Atomic replacement
            if os.path.exists(self.file_path):
                os.replace(temp_file, self.file_path)
            else:
                os.rename(temp_file, self.file_path)
            return True
        except Exception as e:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except Exception:
                    pass
            raise StorageError(f"Failed to save data to {self.file_path}: {e}")
