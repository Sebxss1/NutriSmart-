from functools import lru_cache


from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase

from config.settings import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
    


def get_db():
    db: Session = SessionLocal
    
    try:
        yield db
        
    finally:
        db.close()
        
        