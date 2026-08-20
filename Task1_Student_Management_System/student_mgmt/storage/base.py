"""
Base Storage Interface
Abstract Base Class defining the persistence contract.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseStorage(ABC):
    """Abstract interface for all storage backends."""

    @abstractmethod
    def load_all(self) -> List[Dict[str, Any]]:
        """Load all raw student records from storage."""
        pass

    @abstractmethod
    def save_all(self, records: List[Dict[str, Any]]) -> bool:
        """Persist all student records to storage."""
        pass
