import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


ROOT_DIR = Path(__file__).resolve().parents[3]

# Local: SQLite
# Produção: PostgreSQL através de DATABASE_URL

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    if DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgresql://",
            "postgresql+psycopg://",
            1,
        )

    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
    )

else:
    DATABASE_PATH = ROOT_DIR / "data" / "datapulse.db"
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"

    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
    )


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)

Base = declarative_base()


def create_tables() -> None:
    from src.datapulse.db.models import Sale  # noqa: F401

    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


