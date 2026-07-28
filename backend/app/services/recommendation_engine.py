from typing import List, Dict


class RecommendationEngine:
    """
    Generates cloud optimization recommendations
    based on cloud cost and utilization metrics.
    """

    def __init__(
        self,
        forecast_cost: float,
        budget: float,
        idle_resources: int,
        anomaly_count: int,
        estimated_savings: float,
        utilization: float,
    ):
        self.forecast_cost = forecast_cost
        self.budget = budget
        self.idle_resources = idle_resources
        self.anomaly_count = anomaly_count
        self.estimated_savings = estimated_savings
        self.utilization = utilization

    def generate(self) -> List[Dict]:

        recommendations = []

        # -------------------------------------------------
        # Forecast exceeds budget
        # -------------------------------------------------

        if self.forecast_cost > self.budget:

            recommendations.append({

                "priority": "HIGH",

                "service": "Billing",

                "resource": "AWS Account",

                "title": "Forecast exceeds monthly budget",

                "reason": (
                    f"Forecasted monthly cost (${self.forecast_cost:.2f}) "
                    f"is greater than the configured budget "
                    f"(${self.budget:.2f})."
                ),

                "estimated_monthly_savings": round(
                    self.forecast_cost - self.budget,
                    2
                ),

                "health_score_gain": 8,

                "confidence": 95
            })

        # -------------------------------------------------
        # Idle Resources
        # -------------------------------------------------

        if self.idle_resources > 0:

            recommendations.append({

                "priority": "HIGH",

                "service": "EC2",

                "resource": f"{self.idle_resources} Idle Resource(s)",

                "title": "Review idle EC2 instances",

                "reason": (
                    "Detected idle compute resources "
                    "that may be increasing cloud costs."
                ),

                "estimated_monthly_savings": (
                    self.idle_resources * 20
                ),

                "health_score_gain": (
                    self.idle_resources * 3
                ),

                "confidence": 90
            })

        # -------------------------------------------------
        # Cost Anomaly
        # -------------------------------------------------

        if self.anomaly_count > 0:

            recommendations.append({

                "priority": "MEDIUM",

                "service": "Cost Explorer",

                "resource": "Billing Data",

                "title": "Investigate recent cost anomalies",

                "reason": (
                    f"{self.anomaly_count} anomaly(s) "
                    "detected in recent billing records."
                ),

                "estimated_monthly_savings": 0,

                "health_score_gain": 4,

                "confidence": 92
            })

        # -------------------------------------------------
        # Low Utilization
        # -------------------------------------------------

        if self.utilization < 60:

            recommendations.append({

                "priority": "MEDIUM",

                "service": "Infrastructure",

                "resource": "Compute Resources",

                "title": "Improve resource utilization",

                "reason": (
                    f"Average utilization is only "
                    f"{self.utilization}%."
                ),

                "estimated_monthly_savings": (
                    self.estimated_savings
                ),

                "health_score_gain": 5,

                "confidence": 88
            })

        # -------------------------------------------------
        # Healthy Account
        # -------------------------------------------------

        if len(recommendations) == 0:

            recommendations.append({

                "priority": "LOW",

                "service": "AWS",

                "resource": "Account",

                "title": "Cloud environment is healthy",

                "reason": (
                    "No major optimization opportunities "
                    "were detected."
                ),

                "estimated_monthly_savings": 0,

                "health_score_gain": 0,

                "confidence": 100
            })

        return recommendations