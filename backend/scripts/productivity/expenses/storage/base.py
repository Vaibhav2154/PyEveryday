# from abc import ABC, abstractmethod
# from datetime import date
# from typing import Iterable, List, Optional, Dict, Tuple
# from ..models import Expense

# class ExpenseStorage(ABC):
#     @abstractmethod
#     def add(self, expense: Expense) -> None: ...
#     @abstractmethod
#     def list(self, start: Optional[date] = None, end: Optional[date] = None) -> List[Expense]: ...
#     @abstractmethod
#     def summarize(self, period: str, ref: Optional[date] = None) -> Dict[str, float]: ...
# backend/scripts/productivity/expenses/storage/base.py
from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional, Dict
from ..models import Expense

class ExpenseStorage(ABC):
    @abstractmethod
    def add(self, expense: Expense) -> None: ...
    @abstractmethod
    def list(self, start: Optional[date] = None, end: Optional[date] = None) -> List[Expense]: ...
    @abstractmethod
    def summarize(self, period: str, ref: Optional[date] = None) -> Dict[str, float]: ...
