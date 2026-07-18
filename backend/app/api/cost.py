from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import CostRecord
from typing import List
from datetime import date

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[dict])
def get_costs(
    start_date: date = None,
    end_date: date = None,
    service: str = None,
    region: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(CostRecord)

    if start_date:
        query = query.filter(CostRecord.billing_date >= start_date)

    if end_date:
        query = query.filter(CostRecord.billing_date <= end_date)

    if service:
        query = query.filter(CostRecord.service == service)

    if region:
        query = query.filter(CostRecord.region == region)

    results = query.order_by(CostRecord.billing_date.desc()).all()

    return [
        {
            "billing_date": c.billing_date,
            "service": c.service,
            "region": c.region,
            "amount": c.amount,
            "usage": c.usage,
            "currency": c.currency,
            "granularity": c.granularity,
            "billing_period_start": c.billing_period_start,
            "billing_period_end": c.billing_period_end
        }
        for c in results
    ]