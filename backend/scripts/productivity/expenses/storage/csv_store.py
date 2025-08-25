# import csv
# from datetime import date, datetime
# from pathlib import Path
# from typing import List, Optional, Dict, Tuple
# from ..models import Expense
# from .base import ExpenseStorage

# class CsvExpenseStorage(ExpenseStorage):
#     def __init__(self, csv_path: Path):
#         self.csv_path = csv_path
#         self.csv_path.parent.mkdir(parents=True, exist_ok=True)
#         if not self.csv_path.exists():
#             with self.csv_path.open("w", newline="", encoding="utf-8") as f:
#                 writer = csv.writer(f)
#                 writer.writerow(["date", "category", "amount", "note"])

#     def add(self, expense: Expense) -> None:
#         with self.csv_path.open("a", newline="", encoding="utf-8") as f:
#             writer = csv.writer(f)
#             writer.writerow([
#                 expense.when.isoformat(),
#                 expense.category,
#                 f"{expense.amount:.2f}",
#                 expense.note or ""
#             ])

#     def list(self, start: Optional[date] = None, end: Optional[date] = None) -> List[Expense]:
#         results: List[Expense] = []
#         with self.csv_path.open("r", newline="", encoding="utf-8") as f:
#             reader = csv.DictReader(f)
#             for row in reader:
#                 d = datetime.fromisoformat(row["date"]).date()
#                 if start and d < start:
#                     continue
#                 if end and d > end:
#                     continue
#                 results.append(Expense(
#                     when=d,
#                     category=row["category"],
#                     amount=float(row["amount"]),
#                     note=row.get("note") or None
#                 ))
#         return results

#     def summarize(self, period: str, ref: Optional[date] = None) -> Dict[str, float]:
#         """
#         period: 'day' | 'week' | 'month'
#         ref: reference date (defaults to today)
#         """
#         ref = ref or date.today()
#         items = self.list()
#         if period == "day":
#             filtered = [e for e in items if e.when == ref]
#         elif period == "week":
#             iso_y, iso_w, _ = ref.isocalendar()
#             filtered = [e for e in items if e.when.isocalendar()[:2] == (iso_y, iso_w)]
#         elif period == "month":
#             filtered = [e for e in items if e.when.year == ref.year and e.when.month == ref.month]
#         else:
#             raise ValueError("period must be one of: day, week, month")

#         total = sum(e.amount for e in filtered)
#         by_category: Dict[str, float] = {}
#         for e in filtered:
#             by_category[e.category] = by_category.get(e.category, 0.0) + e.amount
#         by_category["__total__"] = total
#         return by_category
# backend/scripts/productivity/expenses/storage/csv_store.py
import csv
from datetime import date, datetime
from pathlib import Path
from typing import List, Optional, Dict
from ..models import Expense
from .base import ExpenseStorage

class CsvExpenseStorage(ExpenseStorage):
    def __init__(self, csv_path: Path):
        self.csv_path = csv_path
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.csv_path.exists():
            with self.csv_path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["date", "category", "amount", "note"])

    def add(self, expense: Expense) -> None:
        with self.csv_path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                expense.when.isoformat(),
                expense.category,
                f"{expense.amount:.2f}",
                expense.note or ""
            ])

    def list(self, start: Optional[date] = None, end: Optional[date] = None) -> List[Expense]:
        items: List[Expense] = []
        with self.csv_path.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                d = datetime.fromisoformat(row["date"]).date()
                if start and d < start:
                    continue
                if end and d > end:
                    continue
                items.append(Expense(
                    when=d,
                    category=row["category"],
                    amount=float(row["amount"]),
                    note=row.get("note") or None
                ))
        return items

    def summarize(self, period: str, ref: Optional[date] = None) -> Dict[str, float]:
        ref = ref or date.today()
        items = self.list()
        if period == "day":
            filtered = [e for e in items if e.when == ref]
        elif period == "week":
            y, w, _ = ref.isocalendar()
            filtered = [e for e in items if e.when.isocalendar()[:2] == (y, w)]
        elif period == "month":
            filtered = [e for e in items if e.when.year == ref.year and e.when.month == ref.month]
        else:
            raise ValueError("period must be 'day', 'week', or 'month'")

        totals: Dict[str, float] = {}
        total_all = 0.0
        for e in filtered:
            totals[e.category] = totals.get(e.category, 0.0) + e.amount
            total_all += e.amount
        totals["__total__"] = total_all
        return totals
