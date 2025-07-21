import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app
from app.api.dependencies import get_stock_service
from app.services.stock_service import StockService
from app.db.models.stock import Stock

class FakeRepository:
    def __init__(self):
        self.stocks = {}

    def get_by_symbol(self, symbol: str):
        return self.stocks.get(symbol)

    def add(self, stock: Stock) -> None:
        self.stocks[stock.company_code] = stock

    def commit(self) -> None:
        pass


@pytest.fixture()
def client():
    repo = FakeRepository()
    service = StockService(repo)
    app.dependency_overrides[get_stock_service] = lambda: service
    with TestClient(app) as c:
        yield c, repo
    app.dependency_overrides.clear()


@patch("app.services.polygon.get_daily_stock")
@patch("app.services.marketwatch.get_marketwatch_data")
def test_get_stock_with_cache(mock_marketwatch, mock_polygon, client):
    client, repo = client
    mock_polygon.return_value = {"open": 210, "high": 211, "low": 209, "close": 210.5}
    mock_marketwatch.return_value = {
        "company_name": "Apple Inc.",
        "performance_data": {"five_days": "0.01%"},
        "competitors": [{"name": "Microsoft", "chg_percent": "1.2%", "market_cap": "$2T"}],
    }

    response = client.get("/stock/aapl")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "aapl"
    assert repo.get_by_symbol("aapl") is not None

    mock_polygon.reset_mock()
    mock_marketwatch.reset_mock()

    response2 = client.get("/stock/aapl")
    assert response2.status_code == 200
    mock_polygon.assert_not_called()
    mock_marketwatch.assert_not_called()


@patch("app.services.polygon.get_daily_stock")
@patch("app.services.marketwatch.get_marketwatch_data")
def test_post_stock(mock_marketwatch, mock_polygon, client):
    client, repo = client
    mock_polygon.return_value = {"open": 100, "high": 101, "low": 99, "close": 100.5}
    mock_marketwatch.return_value = {"company_name": "Apple Inc.", "performance_data": {}, "competitors": []}

    response = client.post("/stock/aapl?amount=5")
    assert response.status_code == 201
    assert "added to your stock record" in response.json()["message"]

    stock = repo.get_by_symbol("aapl")
    assert stock is not None
    assert stock.purchased_amount == 5