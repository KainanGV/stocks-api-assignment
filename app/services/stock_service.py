from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from fastapi import HTTPException

from app.logger import logger
from app.services.cache import get_from_cache, set_to_cache
from app.services.polygon import get_daily_stock
from app.services.marketwatch import get_marketwatch_data
from app.db.models.stock import Stock
from app.repositories.stock_repository import StockRepository


class StockService:
    """Business logic for stock operations."""

    def __init__(self, repository: StockRepository) -> None:
        self.repository = repository

    def get_stock(self, symbol: str, date: Optional[str] = None) -> Dict[str, Any]:
        symbol = symbol.lower()
        cached = get_from_cache(symbol)
        if cached and (not date or cached.get("date") == date):
            logger.info(f"Cache hit for {symbol}")
            return cached

        base_date = (
            datetime.strptime(date, "%Y-%m-%d").date() if date else datetime.utcnow().date() - timedelta(days=2)
        )

        for i in range(5):
            query_date = base_date - timedelta(days=i)
            try:
                polygon_data = get_daily_stock(symbol, query_date.strftime("%Y-%m-%d"))
                market_data = get_marketwatch_data(symbol)
                result = {
                    "symbol": symbol,
                    "date": query_date.strftime("%Y-%m-%d"),
                    "status": polygon_data.get("status", "OK"),
                    "company_name": market_data.get("company_name", "Unknown"),
                    "stock_values": {
                        "open": polygon_data.get("open"),
                        "high": polygon_data.get("high"),
                        "low": polygon_data.get("low"),
                        "close": polygon_data.get("close"),
                    },
                    "performance_data": market_data.get("performance_data"),
                    "competitors": market_data.get("competitors"),
                }

                stock = self.repository.get_by_symbol(symbol)
                if not stock:
                    stock = Stock(
                        status=result["status"],
                        company_code=symbol,
                        company_name=result["company_name"],
                        stock_values=result["stock_values"],
                        performance_data=result["performance_data"],
                        competitors=result["competitors"],
                        request_date=datetime.utcnow().date(),
                    )
                    self.repository.add(stock)
                else:
                    stock.status = result["status"]
                    stock.company_name = result["company_name"]
                    stock.stock_values = result["stock_values"]
                    stock.performance_data = result["performance_data"]
                    stock.competitors = result["competitors"]
                    stock.request_date = datetime.utcnow().date()
                self.repository.commit()

                set_to_cache(symbol, result)
                logger.info(f"Stock data for {symbol} stored in DB and cache")
                return result
            except Exception as exc:  # pylint: disable=broad-except
                logger.error(f"Error fetching stock {symbol} for {query_date}: {exc}")
                if "NOT_FOUND" not in str(exc):
                    raise HTTPException(status_code=500, detail=str(exc))

        raise HTTPException(status_code=404, detail=f"No data found for {symbol} in the last 5 days")

    def add_stock(self, symbol: str, amount: int) -> None:
        symbol = symbol.lower()
        stock = self.repository.get_by_symbol(symbol)
        if not stock:
            stock = Stock(
                company_code=symbol,
                purchased_amount=amount,
                purchased_status="purchased",
                request_date=datetime.utcnow().date(),
            )
            self.repository.add(stock)
        else:
            stock.purchased_amount += amount
            stock.purchased_status = "purchased"
            stock.request_date = datetime.utcnow().date()
        self.repository.commit()
        logger.info(f"Stock {symbol} updated successfully: total {stock.purchased_amount} units")
