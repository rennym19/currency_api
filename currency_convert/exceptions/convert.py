from pydantic import PydanticValueError


class InvalidAmount(PydanticValueError):
    """Invalid amount exception"""

    code = "invalid_amount"
    msg_template = (
        "amount value has to be greater than or equal to 0, got '{wrong_value}'"
    )


class InvalidDate(PydanticValueError):
    """Invalid date exception"""

    code = "invalid_date"
    msg_template = (
        "date value has to be greater than or equal to 1999-01-01, and has to"
        " be in YYYY-MM-DD format, got '{wrong_value}'"
    )
