from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models import CostRecord


def get_summary(db: Session):
    total_cost = db.query(
        func.sum(CostRecord.amount)
    ).scalar() or 0

    total_services = db.query(
        func.count(func.distinct(CostRecord.service))
    ).scalar() or 0

    total_regions = db.query(
        func.count(func.distinct(CostRecord.region))
    ).scalar() or 0

    highest = (
        db.query(
            CostRecord.service,
            func.sum(CostRecord.amount).label("cost")
        )
        .group_by(CostRecord.service)
        .order_by(func.sum(CostRecord.amount).desc())
        .first()
    )

    return {
        "total_cost": round(total_cost, 2),
        "services": total_services,
        "regions": total_regions,
        "highest_service": highest.service if highest else None,
        "highest_cost": round(highest.cost, 2) if highest else 0,
        "currency": "USD"
    }


def get_service_breakdown(db: Session):
    rows = (
        db.query(
            CostRecord.service,
            func.sum(CostRecord.amount).label("cost")
        )
        .group_by(CostRecord.service)
        .order_by(func.sum(CostRecord.amount).desc())
        .all()
    )

    return [
        {
            "service": row.service,
            "cost": round(row.cost, 2)
        }
        for row in rows
    ]


def get_daily_cost(db: Session):
    rows = (
        db.query(
            CostRecord.billing_date,
            func.sum(CostRecord.amount).label("cost")
        )
        .group_by(CostRecord.billing_date)
        .order_by(CostRecord.billing_date)
        .all()
    )

    return [
        {
            "billing_date": row.billing_date,
            "cost": round(row.cost, 2)
        }
        for row in rows
    ]


def get_top_services(db: Session):
    rows = (
        db.query(
            CostRecord.service,
            func.sum(CostRecord.amount).label("cost")
        )
        .group_by(CostRecord.service)
        .order_by(func.sum(CostRecord.amount).desc())
        .limit(5)
        .all()
    )

    return [
        {
            "service": row.service,
            "cost": round(row.cost, 2)
        }
        for row in rows
    ]