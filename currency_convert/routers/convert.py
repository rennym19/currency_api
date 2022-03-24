from currency_convert.data.rates import get_exchange_rate
from currency_convert.models.convert import ConvertInput, ConvertResult
from currency_convert.validators.convert import is_valid_currency
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/convert",
    tags=["convert"],
)


@router.post("/")
async def convert(convert_input: ConvertInput):
    """
    Converts the received amount from a currency into another currency

    Args:
        convert_input: request's body containing amount, base currency, target
        currency, and optionally, date.
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
        rate=round(float(exchange_rate.rate), 3),
        result=round(
            float(convert_input.amount) * float(exchange_rate.rate), 2
        ),
    )
