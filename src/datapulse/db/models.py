
from datetime import date

from sqlalchemy import Date, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.datapulse.db.database import Base


class Sale(Base):
    __tablename__ = "sales"

    id_venda: Mapped[str] = mapped_column(
        String(50),
        primary_key=True,
    )

    data: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    produto: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    quantidade: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    preco_unitario: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    faturamento: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
