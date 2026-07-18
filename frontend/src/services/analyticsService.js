import api from "./api";

export const getDailyCost = () =>
    api.get("/analytics/daily-cost");

export const getServiceBreakdown = () =>
    api.get("/analytics/service-breakdown");

export const getAnalyticsSummary = () =>
    api.get("/analytics/summary");

export const getTopServices = () =>
    api.get("/analytics/top-services");