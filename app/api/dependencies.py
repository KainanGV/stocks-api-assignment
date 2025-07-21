from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.repositories.stock_repository import StockRepository
from app.services.stock_service import StockService


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_stock_service(db: Session = Depends(get_db)) -> StockService:
    repo = StockRepository(db)
    return StockService(repo)
