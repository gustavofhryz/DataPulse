
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.datapulse.db.database import get_db
from src.datapulse.db.models import Sale


router = APIRouter(tags=["DataPulse Analytics"])


@router.get("/sales")
def list_sales(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    product: str | None = Query(default=None, min_length=1),
    db: Session = Depends(get_db),
):
    """Lista vendas com paginação e filtros."""

    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="A data inicial não pode ser maior que a data final.",
        )

    statement = select(Sale)

    if start_date:
        statement = statement.where(Sale.data >= start_date)

    if end_date:
        statement = statement.where(Sale.data <= end_date)

    if product:
        statement = statement.where(
            Sale.produto.ilike(f"%{product.strip()}%")
        )

    statement = (
        statement
        .order_by(Sale.data.desc(), Sale.id_venda)
        .limit(limit)
        .offset(offset)
    )

    sales = db.scalars(statement).all()

    return [
        {
            "id_venda": sale.id_venda,
            "data": sale.data.isoformat(),
            "produto": sale.produto,
            "quantidade": sale.quantidade,
            "preco_unitario": sale.preco_unitario,
            "faturamento": sale.faturamento,
        }
        for sale in sales
    ]


@router.get("/analytics/summary")
def get_summary(db: Session = Depends(get_db)):
    """Retorna indicadores gerais de vendas."""

    statement = select(
        func.count(Sale.id_venda),
        func.coalesce(func.sum(Sale.faturamento), 0.0),
    )

    total_sales, total_revenue = db.execute(statement).one()

    total_revenue = float(total_revenue or 0.0)
    total_sales = int(total_sales or 0)

    average_ticket = (
        total_revenue / total_sales if total_sales else 0.0
    )

    return {
        "total_vendas": total_sales,
        "faturamento_total": round(total_revenue, 2),
        "ticket_medio": round(average_ticket, 2),
    }


@router.get("/analytics/products")
def get_product_analytics(db: Session = Depends(get_db)):
    """Agrupa vendas por produto e ordena por faturamento."""

    revenue = func.sum(Sale.faturamento)

    statement = (
        select(
            Sale.produto.label("produto"),
            func.count(Sale.id_venda).label("quantidade_vendas"),
            func.sum(Sale.quantidade).label("unidades_vendidas"),
            revenue.label("faturamento"),
        )
        .group_by(Sale.produto)
        .order_by(revenue.desc(), Sale.produto)
    )

    rows = db.execute(statement).all()

    return [
        {
            "produto": row.produto,
            "quantidade_vendas": int(row.quantidade_vendas),
            "unidades_vendidas": int(row.unidades_vendidas),
            "faturamento": round(float(row.faturamento or 0.0), 2),
        }
        for row in rows
    ]
