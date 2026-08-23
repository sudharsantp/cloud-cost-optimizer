from typing import Dict, Any


class CostHealthScore:
    """
    Calculates the overall AWS Cloud Cost Health Score.

    Maximum Score = 100

    Score components:
        Forecast        = 20
        Idle Resources  = 25
        Budget          = 15
        Anomaly         = 15
        Savings         = 10
        Utilization     = 15
    """

    def __init__(
        self,
        forecast_cost: float,
        budget: float,
        idle_resources: int,
        anomaly_count: int,
        estimated_savings: float,
        utilization,
        budget_configured: bool = False,
    ):

        self.forecast_cost = float(
            forecast_cost or 0
        )

        self.budget = float(
            budget or 0
        )

        self.idle_resources = int(
            idle_resources or 0
        )

        self.anomaly_count = int(
            anomaly_count or 0
        )

        self.estimated_savings = float(
            estimated_savings or 0
        )

        # None means utilization could not be measured.
        self.utilization = (
            float(utilization)
            if utilization is not None
            else None
        )

        self.budget_configured = bool(
            budget_configured
        )

    # =========================================================
    # FORECAST SCORE — 20
    # =========================================================

    def forecast_score(self) -> int:

        if self.budget_configured:

            if self.forecast_cost <= self.budget:
                return 20

            elif self.forecast_cost <= self.budget * 1.10:
                return 15

            elif self.forecast_cost <= self.budget * 1.25:
                return 8

            return 0

        # No configured budget.
        # Forecast risk cannot be fully evaluated.
        return 15

    # =========================================================
    # IDLE RESOURCE SCORE — 25
    # =========================================================

    def idle_score(self) -> int:

        score = 25 - (
            self.idle_resources * 4
        )

        return max(
            0,
            score
        )

    # =========================================================
    # BUDGET SCORE — 15
    # =========================================================

    def budget_score(self) -> int:

        if not self.budget_configured:
            return 8

        if self.budget <= 0:
            return 8

        usage = (
            self.forecast_cost
            / self.budget
        )

        if usage <= 0.60:
            return 15

        elif usage <= 0.80:
            return 10

        elif usage <= 1.00:
            return 5

        return 0

    # =========================================================
    # ANOMALY SCORE — 15
    # =========================================================

    def anomaly_score(self) -> int:

        if self.anomaly_count == 0:
            return 15

        elif self.anomaly_count <= 2:
            return 10

        elif self.anomaly_count <= 5:
            return 5

        return 0

    # =========================================================
    # SAVINGS SCORE — 10
    # =========================================================

    def savings_score(self) -> int:

        if self.estimated_savings < 100:
            return 10

        elif self.estimated_savings < 500:
            return 8

        elif self.estimated_savings < 1000:
            return 5

        return 2

    # =========================================================
    # UTILIZATION SCORE — 15
    # =========================================================

    def utilization_score(self) -> int:

        # None means there were no measurable running
        # EC2 resources.
        #
        # Do NOT interpret None as 0% utilization.

        if self.utilization is None:
            return 15

        if self.utilization >= 80:
            return 15

        elif self.utilization >= 60:
            return 10

        elif self.utilization >= 40:
            return 5

        return 2

    # =========================================================
    # STATUS
    # =========================================================

    @staticmethod
    def get_status(score: int) -> str:

        if score >= 90:
            return "Excellent"

        elif score >= 75:
            return "Good"

        elif score >= 60:
            return "Fair"

        elif score >= 40:
            return "Poor"

        return "Critical"

    # =========================================================
    # FINAL CALCULATION
    # =========================================================

    def calculate(self) -> Dict[str, Any]:

        # -----------------------------------------------------
        # Calculate individual scores
        # -----------------------------------------------------

        forecast = self.forecast_score()

        idle = self.idle_score()

        budget = self.budget_score()

        anomaly = self.anomaly_score()

        savings = self.savings_score()

        utilization = self.utilization_score()

        # -----------------------------------------------------
        # Calculate total
        # -----------------------------------------------------

        total = (
            forecast
            + idle
            + budget
            + anomaly
            + savings
            + utilization
        )

        # Protect score boundaries.
        total = max(
            0,
            min(100, total)
        )

        status = self.get_status(total)

        # =====================================================
        # DYNAMIC SCORE FACTORS
        # =====================================================

        factors = []

        # =====================================================
        # FORECAST
        # =====================================================

        forecast_impact = 20 - forecast

        if self.budget_configured:

            if self.forecast_cost <= self.budget:

                forecast_reason = (
                    f"30-day forecast "
                    f"${self.forecast_cost:.2f} "
                    f"is within the configured budget "
                    f"of ${self.budget:.2f}."
                )

                forecast_status = "healthy"

            else:

                forecast_reason = (
                    f"30-day forecast "
                    f"${self.forecast_cost:.2f} "
                    f"exceeds the configured budget "
                    f"of ${self.budget:.2f}."
                )

                forecast_status = "warning"

        else:

            forecast_reason = (
                f"30-day forecast is "
                f"${self.forecast_cost:.2f}. "
                f"No application budget is configured, "
                f"so forecast risk cannot be fully evaluated."
            )

            forecast_status = "neutral"

        factors.append({
            "key": "forecast",
            "name": "Forecast",
            "score": forecast,
            "maximum": 20,
            "impact": forecast_impact,
            "status": forecast_status,
            "reason": forecast_reason
        })

        # =====================================================
        # IDLE RESOURCES
        # =====================================================

        idle_impact = 25 - idle

        if self.idle_resources > 0:

            idle_reason = (
                f"{self.idle_resources} AWS optimization "
                f"finding(s) were detected."
            )

            idle_status = "warning"

        else:

            idle_reason = (
                "No AWS optimization findings were "
                "detected by the current resource analysis."
            )

            idle_status = "healthy"

        factors.append({
            "key": "idle_resources",
            "name": "Idle Resources",
            "score": idle,
            "maximum": 25,
            "impact": idle_impact,
            "status": idle_status,
            "reason": idle_reason
        })

        # =====================================================
        # BUDGET
        # =====================================================

        budget_impact = 15 - budget

        if self.budget_configured:

            if self.budget > 0:

                usage = (
                    self.forecast_cost
                    / self.budget
                ) * 100

                budget_reason = (
                    f"Forecast uses approximately "
                    f"{usage:.1f}% of the configured budget."
                )

            else:

                budget_reason = (
                    "Configured budget is invalid."
                )

            budget_status = (
                "healthy"
                if budget >= 10
                else "warning"
            )

        else:

            budget_reason = (
                "No application budget is configured. "
                "Budget risk cannot currently be evaluated."
            )

            budget_status = "neutral"

        factors.append({
            "key": "budget",
            "name": "Budget",
            "score": budget,
            "maximum": 15,
            "impact": budget_impact,
            "status": budget_status,
            "reason": budget_reason
        })

        # =====================================================
        # ANOMALY
        # =====================================================

        anomaly_impact = 15 - anomaly

        if self.anomaly_count > 0:

            anomaly_reason = (
                f"{self.anomaly_count} billing anomaly "
                f"(or anomalies) detected from "
                f"synchronized AWS billing data."
            )

            anomaly_status = "critical"

        else:

            anomaly_reason = (
                "No billing anomalies were detected."
            )

            anomaly_status = "healthy"

        factors.append({
            "key": "anomaly",
            "name": "Billing Anomalies",
            "score": anomaly,
            "maximum": 15,
            "impact": anomaly_impact,
            "status": anomaly_status,
            "reason": anomaly_reason
        })

        # =====================================================
        # SAVINGS
        # =====================================================

        savings_impact = 10 - savings

        if self.estimated_savings > 0:

            savings_reason = (
                f"Estimated monthly optimization "
                f"opportunity is "
                f"${self.estimated_savings:.2f}."
            )

            savings_status = "warning"

        else:

            savings_reason = (
                "No measurable monthly savings "
                "opportunity was identified."
            )

            savings_status = "healthy"

        factors.append({
            "key": "savings",
            "name": "Savings Opportunity",
            "score": savings,
            "maximum": 10,
            "impact": savings_impact,
            "status": savings_status,
            "reason": savings_reason
        })

        # =====================================================
        # UTILIZATION
        # =====================================================

        if self.utilization is None:

            utilization_score_value = 15

            utilization_impact = 0

            utilization_reason = (
                "No running EC2 instances were available "
                "for CloudWatch CPU utilization measurement."
            )

            utilization_status = "neutral"

        elif self.utilization >= 80:

            utilization_score_value = 15

            utilization_impact = 0

            utilization_reason = (
                f"Average EC2 CPU utilization is "
                f"{self.utilization:.2f}%, indicating "
                f"healthy utilization."
            )

            utilization_status = "healthy"

        elif self.utilization >= 60:

            utilization_score_value = 10

            utilization_impact = 5

            utilization_reason = (
                f"Average EC2 CPU utilization is "
                f"{self.utilization:.2f}%."
            )

            utilization_status = "healthy"

        elif self.utilization >= 40:

            utilization_score_value = 5

            utilization_impact = 10

            utilization_reason = (
                f"Average EC2 CPU utilization is "
                f"{self.utilization:.2f}%, indicating "
                f"moderate utilization."
            )

            utilization_status = "warning"

        else:

            utilization_score_value = 2

            utilization_impact = 13

            utilization_reason = (
                f"Average EC2 CPU utilization is "
                f"{self.utilization:.2f}%, indicating "
                f"potential underutilization."
            )

            utilization_status = "warning"

        factors.append({
            "key": "utilization",
            "name": "EC2 Utilization",
            "score": utilization_score_value,
            "maximum": 15,
            "impact": utilization_impact,
            "status": utilization_status,
            "reason": utilization_reason
        })

        # =====================================================
        # FINAL RESPONSE
        # =====================================================

        return {
            "score": total,
            "status": status,

            "forecast_score": forecast,
            "idle_score": idle,
            "budget_score": budget,
            "anomaly_score": anomaly,
            "savings_score": savings,
            "utilization_score": utilization,

            "factors": factors,

            "score_breakdown": {
                "forecast": {
                    "score": forecast,
                    "maximum": 20,
                    "impact": forecast_impact
                },
                "idle_resources": {
                    "score": idle,
                    "maximum": 25,
                    "impact": idle_impact
                },
                "budget": {
                    "score": budget,
                    "maximum": 15,
                    "impact": budget_impact
                },
                "anomaly": {
                    "score": anomaly,
                    "maximum": 15,
                    "impact": anomaly_impact
                },
                "savings": {
                    "score": savings,
                    "maximum": 10,
                    "impact": savings_impact
                },
                "utilization": {
                    "score": utilization_score_value,
                    "maximum": 15,
                    "impact": utilization_impact
                }
            }
        }