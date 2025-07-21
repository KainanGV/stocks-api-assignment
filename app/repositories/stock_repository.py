from sqlalchemy.orm import Session
from app.db.models.stock import Stock


class StockRepository:
    """Repository layer for Stock model."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_symbol(self, symbol: str) -> Stock | None:
        return self.session.query(Stock).filter_by(company_code=symbol).first()

    def add(self, stock: Stock) -> None:
        self.session.add(stock)

    def commit(self) -> None:
        self.session.commit()
