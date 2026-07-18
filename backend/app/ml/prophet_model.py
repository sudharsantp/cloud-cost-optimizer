from prophet import Prophet
import joblib
import pandas as pd
from pathlib import Path


MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)

MODEL_PATH = MODEL_DIR / "prophet_model.pkl"


class ProphetModel:
    """
    Handles Prophet model lifecycle.

    Responsibilities
    ----------------
    • Train
    • Save
    • Load
    • Predict
    """

    def __init__(self):
        self.model = None

    def train(self, dataframe: pd.DataFrame):

        self.model = Prophet(
            daily_seasonality=True,
            weekly_seasonality=True,
            yearly_seasonality=False
        )

        self.model.fit(dataframe)

        return self.model

    def save(self):

        if self.model is None:
            raise ValueError("Model has not been trained.")

        joblib.dump(
            self.model,
            MODEL_PATH
        )

    def load(self):

        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                "No trained Prophet model found."
            )

        self.model = joblib.load(
            MODEL_PATH
        )

        return self.model

    def predict(
        self,
        periods=30
    ):

        if self.model is None:
            raise ValueError(
                "Load or train model first."
            )

        future = self.model.make_future_dataframe(
            periods=periods,
            freq="D"
        )

        forecast = self.model.predict(
            future
        )

        return forecast[
            [
                "ds",
                "yhat",
                "yhat_lower",
                "yhat_upper"
            ]
        ]