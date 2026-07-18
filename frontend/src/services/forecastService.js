import api from "./api";

export const getForecastSummary = () =>
    api.get("/prediction/summary");

export const getForecastNext30Days = () =>
    api.get("/prediction/next-30-days");

export const getModelComparison = () =>
    api.get("/prediction/compare");

export const getArimaForecast = () =>
    api.get("/prediction/arima");