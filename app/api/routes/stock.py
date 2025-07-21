from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_stock_service
from app.services.stock_service import StockService
from app.schemas.stock import StockResponse, StockPurchaseResponse

router = APIRouter()


@router.get("/stock/{symbol}", response_model=StockResponse)
def get_stock(
    symbol: str,
    date: str | None = Query(None),
    service: StockService = Depends(get_stock_service),
):
    return service.get_stock(symbol, date)


@router.post("/stock/{symbol}", status_code=status.HTTP_201_CREATED, response_model=StockPurchaseResponse)
def add_stock(
    symbol: str,
    amount: int = Query(..., gt=0),
    service: StockService = Depends(get_stock_service),
):
    service.add_stock(symbol, amount)
    return {"message": f"{amount} units of stock {symbol} were added to your stock record"}
