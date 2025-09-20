from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config import DATABASE_URL, DATABASE_DIR
import os

# Ensure database directory exists
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

SQLALCHEMY_DATABASE_URL = DATABASE_URL

# Enhanced engine configuration for SQLAlchemy 2.0 compatibility
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {},
    echo=False,  # Set to True for SQL logging
    pool_pre_ping=True,  # Validate connections before use
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()