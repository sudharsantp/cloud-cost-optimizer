from fastapi import APIRouter
from datetime import datetime, timedelta

from app.services.aws_cost_explorer import fetch_aws_cost_and_usage

router = APIRouter()


@router.post("/aws")
def sync_aws_cost_data(days: int = 30):
    """
    Synchronize AWS billing data from Cost Explorer.

    By default it imports the last 30 days of billing data.
    """

    end_date = datetime.utcnow().date()

    start_date = end_date - timedelta(days=days)

    result = fetch_aws_cost_and_usage(
        start_date=start_date.strftime("%Y-%m-%d"),
        end_date=end_date.strftime("%Y-%m-%d"),
        granularity="DAILY"
    )

    return {
        "status": "success",
        "days_synced": days,
        "start_date": start_date,
        "end_date": end_date,
        "result": result
    }