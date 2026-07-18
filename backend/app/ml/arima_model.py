from statsmodels.tsa.arima.model import ARIMA
import pandas as pd


class ARIMAModel:
    """
    ARIMA forecasting model.
    """

    def __init__(self):
        self.model = None
        self.fitted_model = None

    def train(self, dataframe: pd.DataFrame):
        series = dataframe["y"]

        self.model = ARIMA(
            series,
            order=(1, 1, 1)
        )

        self.fitted_model = self.model.fit()

        return self.fitted_model

    def predict(self, periods=30):

        if self.fitted_model is None:
            raise ValueError("Train the model first.")

        forecast = self.fitted_model.forecast(
            steps=periods
        )

        return forecast.tolist()