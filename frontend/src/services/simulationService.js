import api from "./api";

export const simulateEC2 = (data) =>
    api.post("/simulation/ec2", data);