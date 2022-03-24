import ssl
from typing import Any, Callable, Dict, Optional

import aiohttp
import certifi

ENDPOINTS = {
    "LIST": {"CURRENCIES": "https://openexchangerates.org/api/currencies.json"},
    "GET": {
        "RATES": (
            "https://openexchangerates.org/api/latest.json?base=USD"
            "&app_id=db2516aa5488449db8bdf6d6a4b1df3c"
        ),
        "HISTORICAL_RATES": (
            "https://openexchangerates.org/api/historical/{date}.json?"
            "app_id=db2516aa5488449db8bdf6d6a4b1df3c"
            "&base=USD"
        ),
    },
}


async def fetch_currencies_from_api() -> Dict[str, str]:
    """
    Fetches list of available currencies from an external API.

    Returns:
        Dict[str, str]: available currencies in the form -> code: name
    """

    async def response_handler(response: aiohttp.ClientResponse) -> Any:
        return await response.json()

    return await fetch_open_exchange_rates_api(
        ENDPOINTS["LIST"]["CURRENCIES"], response_handler
    )


async def fetch_exchange_rates_from_api(
    date: Optional[str] = None,
) -> Dict[str, str]:
    """
    Fetches list of exchange rates from an external API where the base currency
    always is USD.

    Args:
        date (str, optional): Date of rates to fetch. Defaults to latest.

    Returns:
        Dict[str, str]: exchange rates in the form -> code: rate
    """

    async def response_handler(response: aiohttp.ClientResponse) -> Any:
        data = await response.json()
        return data.get("rates")

    # If date is None, fetch latest exchange rates
    if date is None:
        return await fetch_open_exchange_rates_api(
            ENDPOINTS["GET"]["RATES"], response_handler
        )
    else:
        # else, fetch historical rates
        return await fetch_open_exchange_rates_api(
            ENDPOINTS["GET"]["HISTORICAL_RATES"].format(date=date),
            response_handler,
        )


async def fetch_open_exchange_rates_api(url: str, get_data: Callable) -> Any:
    """
    Fetches an open exchange rate API endpoint.

    Args:
        url (str): url
        get_data (Callable): response handler

    Returns:
        Any: parsed response
    """
    data = {}

    # Make request to external API, asynchronously
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=ssl_context) as response:
            data = await get_data(response)

    # No rates, return empty dict
    if not data:
        return {}

    # Return results
    return data
