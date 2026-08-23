from fastapi import APIRouter
from datetime import datetime, timedelta

from app.services.aws_cost_explorer import fetch_aws_cost_and_usage
from app.services.anomaly_detection import detect_anomalies

router = APIRouter()


@router.post("/aws")
def sync_aws_cost_data(days: int = 30):
    """
    Synchronize AWS billing data from Cost Explorer
    and refresh anomaly detection.
    """

    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days)

    # -------------------------------------------------
    # 1. Fetch AWS billing data
    # -------------------------------------------------

    result = fetch_aws_cost_and_usage(
        start_date=start_date.strftime("%Y-%m-%d"),
        end_date=end_date.strftime("%Y-%m-%d"),
        granularity="DAILY"
    )

    # -------------------------------------------------
    # 2. Stop if AWS synchronization failed
    # -------------------------------------------------

    if result.get("status") != "success":
        return {
            "status": "error",
            "message": result.get(
                "message",
                "AWS billing synchronization failed."
            ),
            "cost_data": result
        }

    # -------------------------------------------------
    # 3. Re-run anomaly detection
    # -------------------------------------------------

    anomaly_result = detect_anomalies()

    # -------------------------------------------------
    # 4. Return complete synchronization result
    # -------------------------------------------------

    return {
        "status": "success",
        "days_synced": days,
        "start_date": start_date,
        "end_date": end_date,
        "cost_data": result,
        "anomaly_detection": anomaly_result
    }