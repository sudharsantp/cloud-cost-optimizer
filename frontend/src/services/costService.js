import api from "./api";

export const getCostHistory = () =>
    api.get("/cost");