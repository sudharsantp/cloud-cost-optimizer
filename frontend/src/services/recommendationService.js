import axios from "axios";

const API = "http://127.0.0.1:8000";

export const getRecommendations = async () => {

    const response = await axios.get(
        `${API}/optimize/`
    );

    return response.data;
};