from fastapi import FastAPI

from app.api.routes import stock

app = FastAPI(title="Stocks API", version="1.0.0")

app.include_router(stock.router)

@app.get("/")
def root():
    return {"message": "Stocks API is running!"}
