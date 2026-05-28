from pydantic import BaseModel
from typing import Literal
from datetime import date


class Transaction(BaseModel):
    date: date
    description: str
    amount: float
    category: str
    kind: Literal["sale", "expense"]
