import os
from dotenv import load_dotenv

load_dotenv() 

class Settings:
    PROJECT_NAME: str = "Stocks API"
    API_V1_STR: str = "/"
    POLYGON_API_KEY: str = os.getenv("POLYGON_API_KEY", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://stocks:stocks123@db:5432/stocksdb")

settings = Settings()
