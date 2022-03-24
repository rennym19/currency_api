from typing import List

from currency_convert.data import currencies
from currency_convert.models.currency import Currency
from fastapi import APIRouter

router = APIRouter(
    prefix="/currencies",
    tags=["currencies"],
)


@router.get("/", response_model=List[Currency])
async def get_currencies() -> List[Currency]:
    """Get list of currencies"""
    return await currencies.get_currencies()
