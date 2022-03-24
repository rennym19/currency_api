from typing import List

from currency_convert.data import currencies
from currency_convert.models.currency import Currency
from fastapi import APIRouter

router = APIRouter(
    prefix="/currencies",
    tags=["currencies"],
)


@router.get("/")
async def get_currencies() -> List[Currency]:
    """Get list of currencies"""
    return await currencies.get_currencies()
