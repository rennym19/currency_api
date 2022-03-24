import json
from typing import List, Optional

from currency_convert.cache.redis import redis_cache
from currency_convert.models.currency import ExchangeRate
from currency_convert.provider.open_exchange_rates import (
    fetch_exchange_rates_from_api,
)

CACHE_KEYS = {
    "EXCHANGE_RATES": "exchange_rates",
    "HISTORICAL_RATES": "historical_rates_{date}",
}


async def get_exchange_rate(
    base_currency: str,
    target_currency: str,
    date: Optional[str] = None,
) -> List[ExchangeRate]:
    """
    Gets exchange rate between a pair of currencies, either from cache or from
    an external API.

    Args:
        base_currency (str): currency we want to convert from
        target_currency (str): currency we want to convert to
        date (str, optional): get exchange rate at this date. Defaults to latest

    Returns:
        List[ExchangeRate]: exchange rates
    """
    # Try to get from cache, but take the date into account as well
    if date is None:
        exchange_rates = await redis_cache.get_key(CACHE_KEYS["EXCHANGE_RATES"])
    else:
        exchange_rates = await redis_cache.get_key(
            CACHE_KEYS["HISTORICAL_RATES"].format(date=date)
        )

    # If cache did not return a valid set of exchange rates, fetch from api
    if not exchange_rates:
        exchange_rates = await fetch_exchange_rates_from_api(date)

        # Cache result
        exchange_rates_to_cache = json.dumps(exchange_rates).encode("utf-8")

        # If using latest exchange rate, expire after 3 hours.
        if date is None:
            await redis_cache.set_key(
                key=CACHE_KEYS["EXCHANGE_RATES"],
                value=exchange_rates_to_cache,
                expire=10800,
            )
        else:
            # If using historical data, don't expire.
            await redis_cache.set_key(
                key=CACHE_KEYS["HISTORICAL_RATES"].format(date=date),
                value=exchange_rates_to_cache,
            )

    else:
        # Decode and parse cache
        exchange_rates = json.loads(exchange_rates.decode("utf-8"))

    return ExchangeRate(
        base_currency=base_currency,
        target_currency=target_currency,
        rate=exchange_rates[target_currency] / exchange_rates[base_currency],
    )
