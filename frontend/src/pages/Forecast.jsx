import useFetch from "../hooks/useFetch";

import {
    getForecastNext30Days,
    getArimaForecast,
    getModelComparison,
} from "../services/forecastService";

import ProphetForecastChart from "../charts/ProphetForecastChart";
import ArimaForecastChart from "../charts/ArimaForecastChart";
import ModelComparisonCard from "../charts/ModelComparisonCard";

export default function Forecast() {

    const prophet =
        useFetch(getForecastNext30Days);

    const arima =
        useFetch(getArimaForecast);

    const comparison =
        useFetch(getModelComparison);

    if (
        prophet.loading ||
        arima.loading ||
        comparison.loading
    ) {
        return <h1>Loading...</h1>;
    }

    if (
        prophet.error ||
        arima.error ||
        comparison.error
    ) {
        return <h1>Error Loading Forecast</h1>;
    }

    return (

        <div className="space-y-8">

            <h1 className="text-4xl font-bold">
                Forecast
            </h1>

            <ModelComparisonCard
                comparison={comparison.data}
            />

            <ProphetForecastChart
                data={prophet.data}
            />

            <ArimaForecastChart
                data={arima.data}
            />

        </div>

    );

}