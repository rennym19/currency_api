from datetime import datetime
from typing import Optional

from currency_convert.exceptions.convert import InvalidAmount, InvalidDate
from pydantic import BaseModel, validator


class ConvertInput(BaseModel):
    """Represents a conversion between currencies"""

    from_currency: str
    to_currency: str
    amount: float
    date: Optional[str] = None

    @validator("amount")
    def check_amount(cls, amount: float) -> float:
        """
        Checks if amount is valid

        Args:
            amount (float): amount

        Raises:
            InvalidAmount: invalid amount

        Returns:
            float: validated amount
        """
        if amount < 0:
            raise InvalidAmount(wrong_value=amount)
        return amount

    @validator("date")
    def check_date(cls, date: str) -> str:
        """
        Checks if date is valid. It has to be >= 1999, Jan 01.

        Args:
            amount (float): amount

        Raises:
            InvalidDate: invalid amount

        Returns:
            float: validated amount
        """
        # If none, skip validation
        if date is None:
            return date

        # Try to parse date. If not possible, throw error
        try:
            parsed_date = datetime.strptime(date, "%Y-%m-%d")
        except:
            raise InvalidDate(wrong_value=date)

        # Check that it is at least 1999-01-01
        if parsed_date.year < 1999:
            raise InvalidDate(wrong_value=date)

        return date

    class Config:
        """Override schema extras, such as: example values"""

        schema_extra = {
            "example": {
                "from_currency": "USD",
                "to_currency": "VES",
                "amount": 10,
                "date": "2021-01-01",
            }
        }


class ConvertResult(BaseModel):
    """Represents the result of a conversion between currencies"""

    from_currency: str
    to_currency: str
    amount: float
    rate: float
    result: float

    class Config:
        """Override schema extras, such as: example values"""

        schema_extra = {
            "example": {
                "from_currency": "USD",
                "to_currency": "VES",
                "amount": 10.0,
                "rate": 4.504,
                "result": 45.04,
            },
        }
