from app.ml.prophet_model import ProphetModel
from app.ml.arima_model import ARIMAModel


class ModelManager:
    """
    Factory responsible for returning ML models.

    This allows us to switch forecasting
    algorithms without changing API code.
    """

    @staticmethod
    def get_model(model_name="prophet"):

        model_name = model_name.lower()

        if model_name == "prophet":
            return ProphetModel()

        elif model_name == "arima":
            return ARIMAModel()

        raise ValueError(
            f"Unsupported model: {model_name}"
        )