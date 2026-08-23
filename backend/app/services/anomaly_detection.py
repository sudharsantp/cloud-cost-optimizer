import pandas as pd

from sklearn.ensemble import IsolationForest

from datetime import datetime

from app.models import CostRecord, Anomaly
from app.database import SessionLocal


def detect_anomalies():
    """
    Detect abnormal AWS billing behavior using Isolation Forest.

    For each AWS service, the function:

    1. Loads synchronized Cost Explorer data.
    2. Builds a service-specific baseline.
    3. Uses Isolation Forest to identify unusual costs.
    4. Calculates actual vs expected cost.
    5. Calculates percentage deviation.
    6. Assigns a severity based on positive cost deviation.
    7. Updates existing anomaly records instead of duplicating them.
    """

    db = SessionLocal()

    try:

        # =====================================================
        # 1. LOAD SYNCHRONIZED AWS BILLING DATA
        # =====================================================

        records = (
            db.query(CostRecord)
            .order_by(
                CostRecord.billing_date.asc()
            )
            .all()
        )

        if len(records) < 10:

            return {
                "status": "warning",
                "message": (
                    "Not enough billing records "
                    "for anomaly detection."
                ),
                "anomalies_detected": 0,
                "detection_method": "Isolation Forest"
            }

        # =====================================================
        # 2. CONVERT BILLING DATA TO DATAFRAME
        # =====================================================

        df = pd.DataFrame(
            [
                {
                    "id": r.id,
                    "billing_date": r.billing_date,
                    "service": r.service,
                    "amount": float(
                        r.amount or 0
                    ),
                    "usage": float(
                        r.usage or 0
                    ),
                    "region": r.region
                }
                for r in records
            ]
        )

        anomaly_count = 0

        # =====================================================
        # 3. ANALYZE EACH AWS SERVICE SEPARATELY
        # =====================================================

        for service in (
            df["service"]
            .dropna()
            .unique()
        ):

            service_df = (
                df[
                    df["service"] == service
                ]
                .copy()
                .sort_values("billing_date")
                .reset_index(drop=True)
            )

            # Isolation Forest requires enough observations
            # to establish a meaningful pattern.

            if len(service_df) < 10:
                continue

            # =================================================
            # 4. ISOLATION FOREST
            # =================================================

            model = IsolationForest(
                contamination=0.10,
                random_state=42
            )

            service_df["prediction"] = (
                model.fit_predict(
                    service_df[["amount"]]
                )
            )

            # =================================================
            # 5. BUILD EXPECTED-COST BASELINE
            # =================================================

            normal_values = (
                service_df[
                    service_df["prediction"] == 1
                ]["amount"]
            )

            if len(normal_values) > 0:

                expected_cost = float(
                    normal_values.median()
                )

            else:

                expected_cost = float(
                    service_df["amount"].median()
                )

            # Prevent division by zero.

            if expected_cost <= 0:

                expected_cost = 0.01

            # =================================================
            # 6. SELECT DETECTED ANOMALIES
            # =================================================

            anomalies = (
                service_df[
                    service_df["prediction"] == -1
                ]
            )

            for _, row in anomalies.iterrows():

                cost_record_id = int(
                    row["id"]
                )

                actual_cost = float(
                    row["amount"]
                )

                # =============================================
                # 7. CALCULATE COST DEVIATION
                # =============================================

                deviation_percent = (
                    (
                        actual_cost
                        - expected_cost
                    )
                    / expected_cost
                ) * 100

                deviation_percent = round(
                    deviation_percent,
                    2
                )

                # =============================================
                # 8. DETERMINE SEVERITY
                # =============================================
                #
                # Positive deviation means the actual cost
                # is ABOVE the expected baseline.
                #
                # Negative deviation means the actual cost
                # is BELOW the expected baseline.
                #
                # Therefore negative deviations are not treated
                # as cost-risk events.
                # =============================================

                if deviation_percent >= 200:

                    severity = "critical"

                elif deviation_percent >= 100:

                    severity = "high"

                elif deviation_percent >= 50:

                    severity = "medium"

                elif deviation_percent > 0:

                    severity = "low"

                else:

                    severity = "informational"

                # =============================================
                # 9. DETERMINE HUMAN-READABLE DIRECTION
                # =============================================

                if deviation_percent > 0:

                    direction = "above"

                elif deviation_percent < 0:

                    direction = "below"

                else:

                    direction = "equal to"

                # =============================================
                # 10. BUILD EXPLANATION
                # =============================================

                details = (
                    f"Abnormal AWS cost detected "
                    f"for {service}. "
                    f"Actual cost: "
                    f"${actual_cost:.4f}. "
                    f"Expected cost: "
                    f"${expected_cost:.4f}. "
                    f"Actual cost is "
                    f"{abs(deviation_percent):.2f}% "
                    f"{direction} the expected baseline."
                )

                # =============================================
                # 11. CHECK FOR EXISTING ANOMALY
                # =============================================

                existing = (
                    db.query(Anomaly)
                    .filter(
                        Anomaly.cost_record_id
                        == cost_record_id
                    )
                    .first()
                )

                # =============================================
                # 12. UPDATE EXISTING ANOMALY
                # =============================================

                if existing:

                    existing.actual_cost = (
                        actual_cost
                    )

                    existing.expected_cost = round(
                        expected_cost,
                        4
                    )

                    existing.deviation_percent = (
                        deviation_percent
                    )

                    existing.severity = (
                        severity
                    )

                    existing.detection_method = (
                        "Isolation Forest"
                    )

                    existing.details = details

                    anomaly_count += 1

                    continue

                # =============================================
                # 13. CREATE NEW ANOMALY
                # =============================================

                anomaly = Anomaly(

                    date=row["billing_date"],

                    service=service,

                    detected_on=datetime.utcnow(),

                    details=details,

                    cost_record_id=(
                        cost_record_id
                    ),

                    actual_cost=(
                        actual_cost
                    ),

                    expected_cost=round(
                        expected_cost,
                        4
                    ),

                    deviation_percent=(
                        deviation_percent
                    ),

                    severity=severity,

                    detection_method=(
                        "Isolation Forest"
                    )
                )

                db.add(anomaly)

                anomaly_count += 1

        # =====================================================
        # 14. SAVE DATABASE CHANGES
        # =====================================================

        db.commit()

        # =====================================================
        # 15. RETURN RESULT
        # =====================================================

        return {

            "status": "success",

            "anomalies_detected": (
                anomaly_count
            ),

            "detection_method": (
                "Isolation Forest"
            ),

            "message": (
                "AWS billing anomaly analysis "
                "completed successfully."
            )
        }

    except Exception as e:

        db.rollback()

        return {

            "status": "error",

            "message": str(e),

            "anomalies_detected": 0

        }

    finally:

        db.close()