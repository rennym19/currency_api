from typing import Any

from pydantic import BaseModel


class Currency(BaseModel):
    """Class that represents a currency"""

    code: str
    name: str

    class Config:
        """Override schema extras, such as: example values"""

        schema_extra = {
            "example": {"code": "EUR", "name": "Euro"},
        }


class ExchangeRate(BaseModel):
    """Class that represents an exchange rate"""

    base_currency: str
    target_currency: str
    rate: str
