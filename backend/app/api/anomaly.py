from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Anomaly

router = APIRouter()


@router.get("/", response_model=List[dict])
def get_anomalies(
    db: Session = Depends(get_db)
):
    anomalies = (
        db.query(Anomaly)
        .order_by(Anomaly.date.desc())
        .all()
    )

    return [
        {
            "id": anomaly.id,

            "date": (
                anomaly.date.isoformat()
                if anomaly.date
                else None
            ),

            "service": anomaly.service,

            "detected_on": (
                anomaly.detected_on.isoformat()
                if anomaly.detected_on
                else None
            ),

            "details": anomaly.details,

            "cost_record_id": anomaly.cost_record_id,

            # =================================================
            # EXPLAINABLE ANOMALY EVIDENCE
            # =================================================

            "actual_cost": round(
                float(anomaly.actual_cost or 0),
                4
            ),

            "expected_cost": round(
                float(anomaly.expected_cost or 0),
                4
            ),

            "deviation_percent": round(
                float(anomaly.deviation_percent or 0),
                2
            ),

            "severity": (
                anomaly.severity
                or "medium"
            ),

            "detection_method": (
                anomaly.detection_method
                or "Isolation Forest"
            )
        }

        for anomaly in anomalies
    ]