"""
JSON Storage Module for Library System
"""
import json
import os
from typing import Dict, Any


class LibraryStorage:
    def __init__(self, file_path: str = "data/library_data.json"):
        self.file_path = os.path.abspath(file_path)
        self._ensure_file()

    def _ensure_file(self):
        directory = os.path.dirname(self.file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump({"books": [], "members": [], "transactions": []}, f, indent=4)

    def load_data(self) -> Dict[str, Any]:
        self._ensure_file()
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return {"books": [], "members": [], "transactions": []}
                return json.loads(content)
        except Exception:
            return {"books": [], "members": [], "transactions": []}

    def save_data(self, data: Dict[str, Any]) -> bool:
        self._ensure_file()
        temp = f"{self.file_path}.tmp"
        try:
            with open(temp, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            if os.path.exists(self.file_path):
                os.replace(temp, self.file_path)
            else:
                os.rename(temp, self.file_path)
            return True
        except Exception:
            if os.path.exists(temp):
                try:
                    os.remove(temp)
                except Exception:
                    pass
            return False
