import pandas as pd
from sklearn.ensemble import IsolationForest
from datetime import datetime

from app.models import CostRecord, Anomaly
from app.database import SessionLocal


def detect_anomalies():
    """
    Detect billing anomalies using Isolation Forest.
    """

    db = SessionLocal()

    try:
        records = db.query(CostRecord).all()

        if len(records) < 10:
            return {
                "status": "warning",
                "message": "Not enough billing records for anomaly detection."
            }

        df = pd.DataFrame([
            {
                "id": r.id,
                "billing_date": r.billing_date,
                "service": r.service,
                "amount": r.amount,
                "usage": r.usage,
                "region": r.region
            }
            for r in records
        ])

        anomaly_count = 0

        for service in df["service"].unique():

            service_df = (
                df[df["service"] == service]
                .copy()
                .sort_values("billing_date")
                .reset_index(drop=True)
            )

            if len(service_df) < 10:
                continue

            model = IsolationForest(
                contamination=0.10,
                random_state=42
            )

            service_df["prediction"] = model.fit_predict(
                service_df[["amount"]]
            )

            anomalies = service_df[
                service_df["prediction"] == -1
            ]

            for _, row in anomalies.iterrows():

                exists = (
                    db.query(Anomaly)
                    .filter(
                        Anomaly.cost_record_id == row["id"]
                    )
                    .first()
                )

                if exists:
                    continue

                anomaly = Anomaly(
                    date=row["billing_date"],
                    service=row["service"],
                    detected_on=datetime.utcnow(),
                    details=(
                        f"Abnormal AWS cost detected "
                        f"for {row['service']} : "
                        f"${row['amount']:.2f}"
                    ),
                    cost_record_id=row["id"]
                )

                db.add(anomaly)
                anomaly_count += 1

        db.commit()

        return {
            "status": "success",
            "anomalies_detected": anomaly_count
        }

    except Exception as e:

        db.rollback()

        return {
            "status": "error",
            "message": str(e)
        }

    finally:
        db.close()