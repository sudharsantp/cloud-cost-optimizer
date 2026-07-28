from typing import Dict


class CostHealthScore:
    """
    Calculates the overall Cloud Cost Health Score.
    Maximum Score = 100
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

    # -------------------------------------------------
    # Forecast Score (20 Marks)
    # -------------------------------------------------
    def forecast_score(self):

        if self.forecast_cost <= self.budget:
            return 20

        elif self.forecast_cost <= self.budget * 1.10:
            return 15

        elif self.forecast_cost <= self.budget * 1.25:
            return 8

        return 0

    # -------------------------------------------------
    # Idle Resource Score (25 Marks)
    # -------------------------------------------------
    def idle_score(self):

        score = 25 - (self.idle_resources * 4)

        return max(score, 0)

    # -------------------------------------------------
    # Budget Score (15 Marks)
    # -------------------------------------------------
    def budget_score(self):

        usage = self.forecast_cost / self.budget

        if usage <= 0.60:
            return 15

        elif usage <= 0.80:
            return 10

        elif usage <= 1.00:
            return 5

        return 0

    # -------------------------------------------------
    # Cost Anomaly Score (15 Marks)
    # -------------------------------------------------
    def anomaly_score(self):

        if self.anomaly_count == 0:
            return 15

        elif self.anomaly_count <= 2:
            return 10

        elif self.anomaly_count <= 5:
            return 5

        return 0

    # -------------------------------------------------
    # Savings Score (10 Marks)
    # -------------------------------------------------
    def savings_score(self):

        if self.estimated_savings < 100:
            return 10

        elif self.estimated_savings < 500:
            return 8

        elif self.estimated_savings < 1000:
            return 5

        return 2

    # -------------------------------------------------
    # Resource Utilization Score (15 Marks)
    # -------------------------------------------------
    def utilization_score(self):

        if self.utilization >= 80:
            return 15

        elif self.utilization >= 60:
            return 10

        elif self.utilization >= 40:
            return 5

        return 2

    # -------------------------------------------------
    # Final Cost Health Score
    # -------------------------------------------------
    def calculate(self) -> Dict:

        forecast = self.forecast_score()
        idle = self.idle_score()
        budget = self.budget_score()
        anomaly = self.anomaly_score()
        savings = self.savings_score()
        utilization = self.utilization_score()

        total = (
            forecast
            + idle
            + budget
            + anomaly
            + savings
            + utilization
        )

        if total >= 90:
            status = "Excellent"

        elif total >= 75:
            status = "Good"

        elif total >= 60:
            status = "Fair"

        elif total >= 40:
            status = "Poor"

        else:
            status = "Critical"

        return {
            "score": total,
            "status": status,
            "forecast_score": forecast,
            "idle_score": idle,
            "budget_score": budget,
            "anomaly_score": anomaly,
            "savings_score": savings,
            "utilization_score": utilization
        }