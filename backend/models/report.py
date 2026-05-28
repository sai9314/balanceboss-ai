from pydantic import BaseModel
from typing import List


class ReconciliationReport(BaseModel):
    total_sales: float
    total_expenses: float
    net: float
    discrepancies: List[str]
