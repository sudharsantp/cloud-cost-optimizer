from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.analytics_service import get_summary
from app.services.forecasting_service import forecast_summary
from app.services.health_score import CostHealthScore
from app.services.recommendation_engine import RecommendationEngine

router = APIRouter(tags=["Cost Health"])


@router.get("/")
def get_cost_health(db: Session = Depends(get_db)):

    try:

        # -----------------------------------------
        # Fetch analytics data
        # -----------------------------------------

        summary = get_summary(db)

        # -----------------------------------------
        # Fetch forecast data
        # -----------------------------------------

        forecast = forecast_summary(db)

        if isinstance(forecast, dict) and forecast.get("status") == "error":
            return forecast

        # -----------------------------------------
        # Dynamic values
        # -----------------------------------------

        forecast_cost = forecast["next_30_days_total"]

        # Temporary values (will become dynamic later)
        budget = 5000
        idle_resources = 0
        anomaly_count = 0
        estimated_savings = 0
        utilization = 80

        # -----------------------------------------
        # Calculate Cost Health Score
        # -----------------------------------------

        health = CostHealthScore(
            forecast_cost=forecast_cost,
            budget=budget,
            idle_resources=idle_resources,
            anomaly_count=anomaly_count,
            estimated_savings=estimated_savings,
            utilization=utilization,
        )

        score = health.calculate()

        # -----------------------------------------
        # Generate Recommendations
        # -----------------------------------------

        recommendations = RecommendationEngine(
            forecast_cost=forecast_cost,
            budget=budget,
            idle_resources=idle_resources,
            anomaly_count=anomaly_count,
            estimated_savings=estimated_savings,
            utilization=utilization,
        ).generate()

        # -----------------------------------------
        # Final Response
        # -----------------------------------------

        return {
            "summary": summary,
            "forecast": forecast,
            "health": score,
            "recommendations": recommendations,
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }