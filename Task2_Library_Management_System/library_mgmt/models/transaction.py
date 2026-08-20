"""
Transaction Model Module (Issue / Return / Fines)
"""
from dataclasses import dataclass, asdict
from datetime import datetime, date, timedelta
from typing import Optional


@dataclass
class Transaction:
    transaction_id: str
    isbn: str
    member_id: str
    issue_date: str  # YYYY-MM-DD
    due_date: str    # YYYY-MM-DD
    return_date: Optional[str] = None
    fine_amount: float = 0.0
    status: str = "Issued"  # 'Issued' or 'Returned'

    def calculate_fine(self, return_date_str: Optional[str] = None, daily_rate: float = 2.0) -> float:
        """Calculates fine based on days overdue beyond due_date."""
        ret_date = datetime.strptime(return_date_str, "%Y-%m-%d").date() if return_date_str else date.today()
        due = datetime.strptime(self.due_date, "%Y-%m-%d").date()
        overdue_days = (ret_date - due).days
        if overdue_days > 0:
            return round(overdue_days * daily_rate, 2)
        return 0.0

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Transaction':
        return cls(
            transaction_id=data.get("transaction_id", ""),
            isbn=data.get("isbn", "").strip().upper(),
            member_id=data.get("member_id", "").strip().upper(),
            issue_date=data.get("issue_date", ""),
            due_date=data.get("due_date", ""),
            return_date=data.get("return_date"),
            fine_amount=float(data.get("fine_amount", 0.0)),
            status=data.get("status", "Issued")
        )
