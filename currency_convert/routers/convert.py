from currency_convert.data.rates import get_exchange_rate
from currency_convert.models.convert import ConvertInput, ConvertResult
from currency_convert.validators.convert import is_valid_currency
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/convert",
    tags=["convert"],
)


@router.post("/", response_model=ConvertResult)
async def convert(convert_input: ConvertInput):
    """
    Converts the received amount in a currency into another currency. If a valid
    date is passed, the API will use historical data (the exchange rate for
    that date).

    Args:
    * from_currency (str): base currency code
    * to_currency (str): target currency code
    * amount (float): amount to convert from base to target currency.
    * date (str, optional): date in YYYY-MM-DD format.
    """
    # Validate base and target currencies
    if not await is_valid_currency(
        convert_input.from_currency
    ) or not await is_valid_currency(convert_input.to_currency):
        raise HTTPException(
            status_code=422, detail="Invalid base or target currency"
        )

    exchange_rate = await get_exchange_rate(
        base_currency=convert_input.from_currency,
        target_currency=convert_input.to_currency,
        date=convert_input.date,
    )

    # Return results
    return ConvertResult(
        from_currency=convert_input.from_currency,
        to_currency=convert_input.to_currency,
        amount=convert_input.amount,
        rate=round(float(exchange_rate.rate), 3),
        result=round(
            float(convert_input.amount) * float(exchange_rate.rate), 2
        ),
    )
