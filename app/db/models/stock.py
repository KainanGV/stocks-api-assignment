from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.sqlite import JSON
import os
from app.db.base import Base

USE_SQLITE = os.getenv("TESTING", "0") == "1"
JsonType = JSON if USE_SQLITE else JSONB

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, nullable=True)
    purchased_amount = Column(Integer, default=0)
    purchased_status = Column(String, nullable=True)
    request_date = Column(Date, nullable=True)
    company_code = Column(String, index=True, unique=True)
    company_name = Column(String, nullable=True)

    stock_values = Column(JSONB, nullable=True)
    performance_data = Column(JSONB, nullable=True)
    competitors = Column(JSONB, nullable=True)
