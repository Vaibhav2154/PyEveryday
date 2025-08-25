# from dataclasses import dataclass
# from datetime import date
# from typing import Optional

# @dataclass(frozen=True)
# class Expense:
#     when: date
#     category: str
#     amount: float
#     note: Optional[str] = None
# backend/scripts/productivity/expenses/models.py
from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass(frozen=True)
class Expense:
    when: date
    category: str
    amount: float
    note: Optional[str] = None
