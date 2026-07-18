from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.forecasting_service import (
    forecast_next_30_days,
    forecast_summary,
    evaluate_prophet_model,
    arima_forecast,
    evaluate_arima,
    compare_models,
)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/next-30-days")
def predict_next_30_days(db: Session = Depends(get_db)):
    return forecast_next_30_days(db)


@router.get("/summary")
def predict_summary(db: Session = Depends(get_db)):
    return forecast_summary(db)


@router.get("/evaluation")
def evaluate_model(db: Session = Depends(get_db)):
    return evaluate_prophet_model(db)


@router.get("/arima")
def arima(db: Session = Depends(get_db)):
    return arima_forecast(db)


@router.get("/arima/evaluation")
def arima_evaluation(db: Session = Depends(get_db)):
    return evaluate_arima(db)


@router.get("/compare")
def compare(db: Session = Depends(get_db)):
    return compare_models(db)