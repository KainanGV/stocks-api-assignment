from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Engine para conexão com Postgres
engine = create_engine(settings.DATABASE_URL, echo=True, future=True)

# Criar sessão de banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
