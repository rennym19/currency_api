import uvicorn

from currency_convert.main import app

if __name__ == "__main__":
    uvicorn.run(app)
