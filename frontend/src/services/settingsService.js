import api from "./api";

export const getBackendStatus = () =>
    api.get("/");

export const syncAWS = () =>
    api.post("/sync/aws");