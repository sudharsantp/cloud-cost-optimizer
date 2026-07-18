from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.analytics_service import (
    get_summary,
    get_service_breakdown,
    get_daily_cost,
    get_top_services
)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    return get_summary(db)


@router.get("/service-breakdown")
def service_breakdown(db: Session = Depends(get_db)):
    return get_service_breakdown(db)


@router.get("/daily-cost")
def daily_cost(db: Session = Depends(get_db)):
    return get_daily_cost(db)


@router.get("/top-services")
def top_services(db: Session = Depends(get_db)):
    return get_top_services(db)