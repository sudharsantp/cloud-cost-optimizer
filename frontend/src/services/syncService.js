import api from "./api";

export const syncAWS = () =>
    api.post("/sync/aws");