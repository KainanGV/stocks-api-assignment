from typing import Any, Dict, List
from pydantic import BaseModel


class Competitor(BaseModel):
    name: str
    chg_percent: str
    market_cap: str


class StockResponse(BaseModel):
    symbol: str
    date: str
    status: str
    company_name: str
    stock_values: Dict[str, Any]
    performance_data: Dict[str, Any]
    competitors: List[Competitor]


class StockPurchaseResponse(BaseModel):
    message: str
