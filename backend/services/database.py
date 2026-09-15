import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# PostgreSQL is used when DATABASE_URL is configured. SQLite keeps the SIH
# demo runnable locally without embedding credentials in source code.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./gramai_demo.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()