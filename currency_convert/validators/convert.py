from currency_convert.data.currencies import get_currencies


async def is_valid_currency(currency: str) -> bool:
    """
    Checks if currency is valid / supported

    Args:
        currency (str): currency

    Raises:
        InvalidAmount: invalid currency

    Returns:
        bool: is valid currency
    """
    # Get list of codes for the available currencies
    currencies = await get_currencies()
    currency_codes = [c.code for c in currencies]

    # If the currency is not in the list, it's invalid
    if currency not in currency_codes:
        return False

    return True
