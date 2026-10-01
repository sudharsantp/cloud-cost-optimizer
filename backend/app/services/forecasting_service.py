from sqlalchemy.orm import Session
from sqlalchemy import func
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
from prophet import Prophet

from app.ml.arima_model import ARIMAModel
from app.models import CostRecord


def prepare_prophet_dataset(db: Session):
    rows = (
        db.query(
            CostRecord.billing_date,
            func.sum(CostRecord.amount).label("daily_cost")
        )
        .group_by(CostRecord.billing_date)
        .order_by(CostRecord.billing_date)
        .all()
    )

    if not rows:
        return pd.DataFrame(columns=["ds", "y"])

    df = pd.DataFrame([
        {
            "ds": row.billing_date,
            "y": float(row.daily_cost or 0)
        }
        for row in rows
    ])

    df["ds"] = pd.to_datetime(df["ds"], errors="coerce")
    df["y"] = pd.to_numeric(df["y"], errors="coerce")

    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=["ds", "y"])

    df = (
        df.groupby("ds", as_index=False)["y"]
        .sum()
        .sort_values("ds")
        .reset_index(drop=True)
    )

    return df


def create_prophet_model():
    return Prophet(
        growth="linear",
        daily_seasonality=False,
        weekly_seasonality=False,
        yearly_seasonality=False,
        changepoint_prior_scale=0.01,
        seasonality_mode="additive"
    )


def train_prophet_model(db: Session):
    df = prepare_prophet_dataset(db)

    if len(df) < 7:
        return None

    if df["y"].nunique() < 2:
        return None

    try:
        model = create_prophet_model()
        model.fit(df)
        return model

    except Exception as e:
        print("Prophet training failed:", str(e))
        return None


def simple_forecast(df, periods=30):
    """
    Safe fallback forecast.
    Uses recent average daily AWS cost.
    """

    if df.empty:
        return []

    recent_count = min(7, len(df))

    recent_average = float(
        df["y"].tail(recent_count).mean()
    )

    recent_average = max(recent_average, 0)

    last_date = pd.to_datetime(
        df["ds"].max()
    )

    results = []

    for i in range(1, periods + 1):

        date = last_date + pd.Timedelta(days=i)

        results.append({
            "ds": date.strftime("%Y-%m-%d"),
            "yhat": round(recent_average, 4),
            "yhat_lower": round(recent_average * 0.9, 4),
            "yhat_upper": round(recent_average * 1.1, 4)
        })

    return results


def forecast_next_30_days(db: Session):

    df = prepare_prophet_dataset(db)

    if len(df) < 7:
        return {
            "status": "error",
            "message": "Not enough valid historical data for forecasting."
        }

    model = train_prophet_model(db)

    # Prophet failed → safe fallback
    if model is None:

        print(
            "Using fallback forecast because Prophet "
            "optimization failed."
        )

        return simple_forecast(
            df,
            periods=30
        )

    try:

        future = model.make_future_dataframe(
            periods=30,
            freq="D"
        )

        forecast = model.predict(future)

        result = forecast[
            [
                "ds",
                "yhat",
                "yhat_lower",
                "yhat_upper"
            ]
        ].tail(30).copy()

        result["yhat"] = result["yhat"].clip(
            lower=0
        )

        result["yhat_lower"] = result[
            "yhat_lower"
        ].clip(
            lower=0
        )

        result["yhat_upper"] = result[
            "yhat_upper"
        ].clip(
            lower=0
        )

        result["ds"] = result["ds"].dt.strftime(
            "%Y-%m-%d"
        )

        return result.to_dict(
            orient="records"
        )

    except Exception as e:

        print(
            "Prophet prediction failed:",
            str(e)
        )

        return simple_forecast(
            df,
            periods=30
        )


def forecast_summary(db: Session):

    forecast = forecast_next_30_days(db)

    if isinstance(forecast, dict):

        return forecast

    if not forecast:

        return {
            "status": "error",
            "message": "No forecast data available."
        }

    tomorrow = forecast[0]

    next_7_days = forecast[:7]

    total_7_days = sum(
        float(day["yhat"])
        for day in next_7_days
    )

    total_30_days = sum(
        float(day["yhat"])
        for day in forecast
    )

    highest_day = max(
        forecast,
        key=lambda x: float(x["yhat"])
    )

    return {
        "tomorrow_prediction": round(
            float(tomorrow["yhat"]),
            4
        ),

        "next_7_days_total": round(
            total_7_days,
            4
        ),

        "next_30_days_total": round(
            total_30_days,
            4
        ),

        "highest_predicted_day":
            highest_day["ds"],

        "highest_cost": round(
            float(highest_day["yhat"]),
            4
        )
    }


def evaluate_prophet(db: Session):

    df = prepare_prophet_dataset(db)

    if len(df) < 14:

        return {
            "status": "error",
            "message": "Not enough data for evaluation."
        }

    split = int(len(df) * 0.8)

    train = df.iloc[:split].copy()
    test = df.iloc[split:].copy()

    if len(train) < 7:

        return {
            "status": "error",
            "message": "Not enough training data."
        }

    if train["y"].nunique() < 2:

        return {
            "status": "error",
            "message": "Insufficient variation in training data."
        }

    try:

        model = create_prophet_model()

        model.fit(train)

        future = model.make_future_dataframe(
            periods=len(test),
            freq="D"
        )

        forecast = model.predict(future)

        predicted = (
            forecast
            .tail(len(test))["yhat"]
            .values
        )

        predicted = np.maximum(
            predicted,
            0
        )

        actual = test["y"].values

        mae = mean_absolute_error(
            actual,
            predicted
        )

        rmse = np.sqrt(
            mean_squared_error(
                actual,
                predicted
            )
        )

        return {
            "model": "Facebook Prophet",
            "training_samples": len(train),
            "testing_samples": len(test),
            "MAE": round(float(mae), 6),
            "RMSE": round(float(rmse), 6)
        }

    except Exception as e:

        print(
            "Prophet evaluation failed:",
            str(e)
        )

        return {
            "status": "error",
            "message": "Prophet optimization failed."
        }


def evaluate_prophet_model(db: Session):
    return evaluate_prophet(db)


def arima_forecast(
    db: Session,
    periods: int = 30
):

    df = prepare_prophet_dataset(db)

    if len(df) < 7:
        return []

    try:

        model = ARIMAModel()

        model.train(df)

        prediction = model.predict(
            periods
        )

        return [
            {
                "day": i + 1,
                "prediction": round(
                    float(value),
                    6
                )
            }
            for i, value in enumerate(
                prediction
            )
        ]

    except Exception as e:

        print(
            "ARIMA forecast failed:",
            str(e)
        )

        return []


def evaluate_arima(db: Session):

    df = prepare_prophet_dataset(db)

    if len(df) < 14:

        return {
            "status": "error",
            "message": "Not enough data."
        }

    split = int(
        len(df) * 0.8
    )

    train = df.iloc[:split].copy()
    test = df.iloc[split:].copy()

    try:

        model = ARIMAModel()

        model.train(train)

        predicted = model.predict(
            len(test)
        )

        predicted = np.asarray(
            predicted,
            dtype=float
        )

        predicted = np.maximum(
            predicted,
            0
        )

        actual = test["y"].values

        mae = mean_absolute_error(
            actual,
            predicted
        )

        rmse = np.sqrt(
            mean_squared_error(
                actual,
                predicted
            )
        )

        return {
            "model": "ARIMA",
            "training_samples": len(train),
            "testing_samples": len(test),
            "MAE": round(
                float(mae),
                6
            ),
            "RMSE": round(
                float(rmse),
                6
            )
        }

    except Exception as e:

        print(
            "ARIMA evaluation failed:",
            str(e)
        )

        return {
            "status": "error",
            "message": "ARIMA evaluation failed."
        }


def compare_models(db: Session):

    prophet = evaluate_prophet(db)

    arima = evaluate_arima(db)

    prophet_ok = (
        "RMSE" in prophet
    )

    arima_ok = (
        "RMSE" in arima
    )

    if prophet_ok and arima_ok:

        prophet_rmse = float(
            prophet["RMSE"]
        )

        arima_rmse = float(
            arima["RMSE"]
        )

        if arima_rmse < prophet_rmse:
            best_model = "ARIMA"
        else:
            best_model = "Prophet"

    elif arima_ok:

        best_model = "ARIMA"

    elif prophet_ok:

        best_model = "Prophet"

    else:

        best_model = "Unavailable"

    return {
        "Prophet": prophet,
        "ARIMA": arima,
        "Best_Model": best_model
    }