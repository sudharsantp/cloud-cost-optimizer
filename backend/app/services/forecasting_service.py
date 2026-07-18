from sqlalchemy.orm import Session
from sqlalchemy import func
import pandas as pd
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)
import numpy as np
from prophet import Prophet
from app.ml.arima_model import ARIMAModel
from app.models import CostRecord


def prepare_prophet_dataset(db: Session):
    """
    Prepare AWS billing data for Prophet.
    """

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

    df = pd.DataFrame(
        [
            {
                "ds": row.billing_date,
                "y": float(row.daily_cost)
            }
            for row in rows
        ]
    )

    return df


def train_prophet_model(db: Session):

    df = prepare_prophet_dataset(db)

    if len(df) < 7:
        return None

    model = Prophet(
        daily_seasonality=True,
        weekly_seasonality=True,
        yearly_seasonality=False
    )

    model.fit(df)

    return model


def forecast_next_30_days(db: Session):

    model = train_prophet_model(db)

    if model is None:
        return {
            "status": "error",
            "message": "Not enough historical data."
        }

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
    ].tail(30)

    return result.to_dict(
        orient="records"
    )
def forecast_summary(db: Session):

    forecast = forecast_next_30_days(db)

    if isinstance(forecast, dict):
        return forecast

    tomorrow = forecast[0]

    next_7_days = forecast[:7]

    total_7_days = sum(day["yhat"] for day in next_7_days)

    total_30_days = sum(day["yhat"] for day in forecast)

    highest_day = max(
        forecast,
        key=lambda x: x["yhat"]
    )

    return {
        "tomorrow_prediction": round(
            tomorrow["yhat"], 4
        ),
        "next_7_days_total": round(
            total_7_days, 4
        ),
        "next_30_days_total": round(
            total_30_days, 4
        ),
        "highest_predicted_day": highest_day["ds"],
        "highest_cost": round(
            highest_day["yhat"], 4
        )
    }    


def evaluate_prophet_model(db: Session):
    """
    Evaluate Prophet using a chronological train/test split.
    """

    df = prepare_prophet_dataset(db)

    if len(df) < 14:
        return {
            "status": "error",
            "message": "Need at least 14 days of data."
        }

    split_index = int(len(df) * 0.8)

    train_df = df.iloc[:split_index].copy()
    test_df = df.iloc[split_index:].copy()

    model = Prophet(
        daily_seasonality=True,
        weekly_seasonality=True,
        yearly_seasonality=False
    )

    model.fit(train_df)

    future = model.make_future_dataframe(
        periods=len(test_df),
        freq="D"
    )

    forecast = model.predict(future)

    predicted = forecast.tail(len(test_df))["yhat"].values
    actual = test_df["y"].values

    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))

    return {
        "model": "Facebook Prophet",
        "training_samples": len(train_df),
        "testing_samples": len(test_df),
        "MAE": round(float(mae), 6),
        "RMSE": round(float(rmse), 6)
    }   

def evaluate_prophet(db: Session):

    df = prepare_prophet_dataset(db)

    if len(df) < 14:
        return {
            "status": "error",
            "message": "Not enough data for evaluation."
        }

    split = int(len(df) * 0.8)

    train = df.iloc[:split]
    test = df.iloc[split:]

    model = Prophet(
        daily_seasonality=True,
        weekly_seasonality=True,
        yearly_seasonality=False
    )

    model.fit(train)

    future = model.make_future_dataframe(
        periods=len(test),
        freq="D"
    )

    forecast = model.predict(future)

    prediction = forecast.tail(len(test))

    actual = test["y"].values

    predicted = prediction["yhat"].values

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

from app.ml.arima_model import ARIMAModel


def arima_forecast(db: Session, periods: int = 30):

    df = prepare_prophet_dataset(db)

    model = ARIMAModel()

    model.train(df)

    prediction = model.predict(periods)

    return [
        {
            "day": i + 1,
            "prediction": round(value, 6)
        }
        for i, value in enumerate(prediction)
    ]
def evaluate_arima(db: Session):

    df = prepare_prophet_dataset(db)

    if len(df) < 14:
        return {
            "status": "error",
            "message": "Not enough data for evaluation."
        }

    split = int(len(df) * 0.8)

    train = df.iloc[:split]
    test = df.iloc[split:]

    model = ARIMAModel()

    model.train(train)

    predicted = model.predict(len(test))

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
        "MAE": round(float(mae), 6),
        "RMSE": round(float(rmse), 6)
    }

def arima_forecast(db: Session, periods: int = 30):

    df = prepare_prophet_dataset(db)

    model = ARIMAModel()

    model.train(df)

    prediction = model.predict(periods)

    return [
        {
            "day": i + 1,
            "prediction": round(float(value), 6)
        }
        for i, value in enumerate(prediction)
    ]


def evaluate_arima(db: Session):

    df = prepare_prophet_dataset(db)

    if len(df) < 14:
        return {
            "status": "error",
            "message": "Not enough data."
        }

    split = int(len(df) * 0.8)

    train = df.iloc[:split]
    test = df.iloc[split:]

    model = ARIMAModel()

    model.train(train)

    predicted = model.predict(len(test))

    actual = test["y"].values

    mae = mean_absolute_error(actual, predicted)

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
        "MAE": round(float(mae), 6),
        "RMSE": round(float(rmse), 6)
    }


def compare_models(db: Session):

    prophet = evaluate_prophet(db)

    arima = evaluate_arima(db)

    prophet_rmse = prophet["RMSE"]
    arima_rmse = arima["RMSE"]

    best = "Prophet"

    if arima_rmse < prophet_rmse:
        best = "ARIMA"

    return {

        "Prophet": prophet,

        "ARIMA": arima,

        "Best_Model": best

    }

