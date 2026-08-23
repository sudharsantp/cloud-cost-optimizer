from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.database import get_db
from app.models import Budget, Anomaly

from app.services.forecasting_service import forecast_summary
from app.services.health_engine import CostHealthScore
from app.services.recommendation_engine import RecommendationEngine


router = APIRouter(tags=["Health"])


@router.get("/")
def get_cost_health(
    db: Session = Depends(get_db)
):

    try:

        # =====================================================
        # 1. FORECAST
        # =====================================================

        forecast = forecast_summary(db)

        if (
            isinstance(forecast, dict)
            and forecast.get("status") == "error"
        ):
            return forecast

        forecast_cost = float(
            forecast.get(
                "next_30_days_total",
                0
            )
        )

        # =====================================================
        # 2. LIVE AWS OPTIMIZATION
        # =====================================================

        engine = RecommendationEngine()

        optimization_result = (
            engine.generate_recommendations()
        )

        recommendations = (
            optimization_result.get(
                "recommendations",
                []
            )
        )

        idle_resources = len(
            recommendations
        )

        estimated_savings = sum(
            float(
                recommendation.get(
                    "estimated_monthly_savings",
                    0
                ) or 0
            )
            for recommendation in recommendations
        )

        # =====================================================
        # 3. ANOMALY ANALYSIS
        # =====================================================

        all_anomalies = (
            db.query(Anomaly)
            .order_by(
                Anomaly.date.desc()
            )
            .all()
        )

        total_anomalies = len(
            all_anomalies
        )

        # Only positive deviations represent
        # unexpected additional spending.

        cost_risk_anomalies = [
            anomaly
            for anomaly in all_anomalies
            if float(
                anomaly.deviation_percent or 0
            ) > 0
        ]

        anomaly_count = len(
            cost_risk_anomalies
        )

        critical_count = sum(
            1
            for anomaly in cost_risk_anomalies
            if anomaly.severity == "critical"
        )

        high_count = sum(
            1
            for anomaly in cost_risk_anomalies
            if anomaly.severity == "high"
        )

        medium_count = sum(
            1
            for anomaly in cost_risk_anomalies
            if anomaly.severity == "medium"
        )

        low_count = sum(
            1
            for anomaly in cost_risk_anomalies
            if anomaly.severity == "low"
        )

        # =====================================================
        # 4. ANOMALY EVIDENCE
        # =====================================================

        anomaly_evidence = []

        for anomaly in cost_risk_anomalies:

            anomaly_evidence.append(
                {
                    "id": anomaly.id,

                    "date": (
                        anomaly.date.isoformat()
                        if anomaly.date
                        else None
                    ),

                    "service": anomaly.service,

                    "actual_cost": round(
                        float(
                            anomaly.actual_cost or 0
                        ),
                        4
                    ),

                    "expected_cost": round(
                        float(
                            anomaly.expected_cost or 0
                        ),
                        4
                    ),

                    "deviation_percent": round(
                        float(
                            anomaly.deviation_percent or 0
                        ),
                        2
                    ),

                    "severity": (
                        anomaly.severity
                        or "low"
                    ),

                    "detection_method": (
                        anomaly.detection_method
                        or "Isolation Forest"
                    ),

                    "details": anomaly.details
                }
            )

        # =====================================================
        # 5. APPLICATION BUDGET
        # =====================================================

        budget_record = (
            db.query(Budget)
            .order_by(
                Budget.created_at.desc()
            )
            .first()
        )

        if budget_record:

            budget = float(
                budget_record.amount or 0
            )

            budget_configured = (
                budget > 0
            )

            budget_period = (
                budget_record.period
            )

        else:

            budget = 0.0

            budget_configured = False

            budget_period = None

        # =====================================================
        # 6. EC2 UTILIZATION
        # =====================================================

        utilization_values = []

        try:

            instances = (
                engine.get_running_instances()
            )

            for instance in instances:

                cpu = (
                    engine.get_cpu_utilization(
                        instance["instance_id"]
                    )
                )

                if cpu is not None:

                    utilization_values.append(
                        float(cpu)
                    )

        except Exception as utilization_error:

            print(
                "EC2 utilization collection error:",
                utilization_error
            )

        if utilization_values:

            average_utilization = round(
                sum(utilization_values)
                / len(utilization_values),
                2
            )

        else:

            average_utilization = None

        # =====================================================
        # 7. CALCULATE HEALTH
        # =====================================================

        health_engine = CostHealthScore(

            forecast_cost=forecast_cost,

            budget=budget,

            idle_resources=idle_resources,

            anomaly_count=anomaly_count,

            estimated_savings=estimated_savings,

            utilization=average_utilization,

            budget_configured=budget_configured
        )

        health = (
            health_engine.calculate()
        )

        # =====================================================
        # 8. ISSUES
        # =====================================================

        issues = []

        if anomaly_count > 0:

            issues.append(
                f"{anomaly_count} cost-risk "
                f"anomaly(s) detected."
            )

        if total_anomalies > anomaly_count:

            informational_count = (
                total_anomalies
                - anomaly_count
            )

            issues.append(
                f"{informational_count} additional "
                f"statistical outlier(s) were below "
                f"their expected cost baseline and "
                f"do not increase cost risk."
            )

        if critical_count > 0:

            issues.append(
                f"{critical_count} critical "
                f"cost anomaly detected."
                if critical_count == 1
                else
                f"{critical_count} critical "
                f"cost anomalies detected."
            )

        if idle_resources > 0:

            issues.append(
                f"{idle_resources} AWS optimization "
                f"finding(s) detected."
            )

        if not budget_configured:

            issues.append(
                "No application budget is configured; "
                "budget risk cannot be fully evaluated."
            )

        elif forecast_cost > budget:

            issues.append(
                "Forecasted 30-day cost exceeds "
                "the configured budget."
            )

        if (
            average_utilization is not None
            and average_utilization < 40
        ):

            issues.append(
                "Average EC2 utilization is low."
            )

        if estimated_savings > 0:

            issues.append(
                f"Potential monthly savings of "
                f"${estimated_savings:.2f} identified."
            )

        if not issues:

            issues.append(
                "No major cost health issues detected."
            )

        # =====================================================
        # 9. FINAL RESPONSE
        # =====================================================

        return {

            "status": "success",

            "generated_at": datetime.now(
                timezone.utc
            ).isoformat(),

            "data_source": {

                "billing":
                    "AWS Cost Explorer synchronized data",

                "resources":
                    "Live AWS EC2 / CloudWatch / EBS / Elastic IP",

                "anomalies":
                    "Isolation Forest on synchronized billing data",

                "forecast":
                    "ARIMA / Prophet forecasting service",

                "budget":
                    "Application budget configuration"
            },

            "health": health,

            "inputs": {

                "forecast_cost":
                    round(
                        forecast_cost,
                        4
                    ),

                "budget":
                    round(
                        budget,
                        4
                    ),

                "budget_configured":
                    budget_configured,

                "budget_period":
                    budget_period,

                "optimization_findings":
                    idle_resources,

                "idle_resources":
                    idle_resources,

                "anomaly_count":
                    anomaly_count,

                "total_statistical_anomalies":
                    total_anomalies,

                "estimated_monthly_savings":
                    round(
                        estimated_savings,
                        2
                    ),

                "average_utilization":
                    (
                        round(
                            average_utilization,
                            2
                        )
                        if average_utilization is not None
                        else None
                    )
            },

            # =================================================
            # ANOMALY ANALYSIS
            # =================================================

            "anomaly_analysis": {

                "total_detected":
                    total_anomalies,

                "cost_risk_anomalies":
                    anomaly_count,

                "critical":
                    critical_count,

                "high":
                    high_count,

                "medium":
                    medium_count,

                "low":
                    low_count,

                "informational":
                    total_anomalies
                    - anomaly_count,

                "evidence":
                    anomaly_evidence
            },

            "issues": issues,

            "recommendations":
                recommendations,

            "forecast":
                forecast
        }

    except Exception as e:

        return {

            "status": "error",

            "message": str(e)
        }