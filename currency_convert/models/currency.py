from typing import Any

from pydantic import BaseModel


class Currency(BaseModel):
    """Class that represents a currency"""

    code: str
    name: str


class ExchangeRate(BaseModel):
    """Class that represents an exchange rate"""

    base_currency: str
    target_currency: str
    rate: str
