import json
from typing import List

from currency_convert.cache.redis import redis_cache
from currency_convert.models.currency import Currency
from currency_convert.provider.open_exchange_rates import (
    fetch_currencies_from_api,
)

CACHE_KEYS = {
    "AVAILABLE_CURRENCIES": "available_currencies",
}


async def get_currencies() -> List[Currency]:
    """
    Gets list of currencies either from cache or external API.

    Returns:
        List[Currency]: currencies
    """
    # Try to get from cache
    currencies = await redis_cache.get_key(CACHE_KEYS["AVAILABLE_CURRENCIES"])

    # If cache did not return a valid set of currencies, fetch from api
    if not currencies:
        currencies = await fetch_currencies_from_api()

        # Cache result
        currencies_to_cache = json.dumps(currencies).encode("utf-8")
        await redis_cache.set_key(
            key=CACHE_KEYS["AVAILABLE_CURRENCIES"],
            value=currencies_to_cache,
            expire=43200,
        )
    else:
        # Decode and parse cache
        currencies = json.loads(currencies.decode("utf-8"))

    return [
        Currency(code=currency_code, name=currency_name)
        for currency_code, currency_name in currencies.items()
    ]
