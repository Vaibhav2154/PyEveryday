# from datetime import date, datetime
# from pathlib import Path
# from typing import Optional, Dict, List
# import os

# from .models import Expense
# from .storage.base import ExpenseStorage
# from .storage.csv_store import CsvExpenseStorage

# # Storage factory (CSV today, DB tomorrow)
# def get_storage() -> ExpenseStorage:
#     # later: read env var PYE_STORAGE=csv|db and switch
#     csv_path = Path(__file__).resolve().parents[3] / "data" / "expenses.csv"
#     return CsvExpenseStorage(csv_path)

# def add_expense(category: str, amount: float, when: Optional[str] = None, note: Optional[str] = None) -> Expense:
#     d = date.fromisoformat(when) if when else date.today()
#     exp = Expense(when=d, category=category.strip(), amount=float(amount), note=note)
#     store = get_storage()
#     store.add(exp)
#     return exp

# def list_expenses(start: Optional[str] = None, end: Optional[str] = None):
#     s = date.fromisoformat(start) if start else None
#     e = date.fromisoformat(end) if end else None
#     return get_storage().list(s, e)

# def summary(period: str, ref_date: Optional[str] = None) -> Dict[str, float]:
#     r = date.fromisoformat(ref_date) if ref_date else None
#     return get_storage().summarize(period, r)
# backend/scripts/productivity/expenses/service.py
from datetime import date
from pathlib import Path
from typing import Optional, Dict, List

from .models import Expense
from .storage.base import ExpenseStorage
from .storage.csv_store import CsvExpenseStorage

def _get_storage() -> ExpenseStorage:
    # CSV today; easy to swap to DB tomorrow
    csv_path = Path(__file__).resolve().parents[3] / "data" / "expenses.csv"
    return CsvExpenseStorage(csv_path)

def add_expense(category: str, amount: float, when: Optional[str] = None, note: Optional[str] = None) -> Expense:
    d = date.fromisoformat(when) if when else date.today()
    exp = Expense(when=d, category=category.strip(), amount=float(amount), note=note)
    _get_storage().add(exp)
    return exp

def list_expenses(start: Optional[str] = None, end: Optional[str] = None) -> List[Expense]:
    s = date.fromisoformat(start) if start else None
    e = date.fromisoformat(end) if end else None
    return _get_storage().list(s, e)

def summary(period: str, ref_date: Optional[str] = None) -> Dict[str, float]:
    ref = date.fromisoformat(ref_date) if ref_date else None
    return _get_storage().summarize(period, ref)
