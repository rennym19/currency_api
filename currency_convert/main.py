from fastapi import FastAPI

from currency_convert.cache.redis import redis_cache
from currency_convert.routers.convert import router as convert_router
from currency_convert.routers.currencies import router as currency_router

description = """
Currency Convert API was made so that you can easily convert any of the
available currencies!

## What can I do with this API?

You will be able to:

* **List currencies:** get a list of the available currencies.
* **Convert:** convert any available currency into other available currency.
* **Historical Convert:** convert a currency into another using the exchange
rate for a specific date.
"""

app = FastAPI(
    title="Currency Convert",
    description=description,
    version="0.1.0",
    contact={
        "name": "Renny",
        "url": "https://github.com/rennym19",
        "email": "rennym19@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    docs_url="/docs",
    redoc_url=None,
)

# Include routes
app.include_router(currency_router, prefix="/api")
app.include_router(convert_router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    """Code to run during startup"""
    # Start pool of connections to the Redis cache
    await redis_cache.start()


@app.on_event("shutdown")
async def shutdown_event():
    """Code to run during shutdown"""
    await redis_cache.close()
