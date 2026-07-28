import { useEffect, useState } from "react";
import { getHealthScore } from "../services/healthService";

import HealthScoreCard from "../components/HealthScoreCard";
import ScoreBreakdown from "../components/ScoreBreakdown";
import RecommendationCard from "../components/RecommendationCard";

import "../styles/CostHealth.css";

export default function CostHealth() {

    const [health, setHealth] = useState(null);

    const [recommendations, setRecommendations] = useState([]);

    const [summary, setSummary] = useState(null);

    const [forecast, setForecast] = useState(null);

    const [loading, setLoading] = useState(true);

    useEffect(() => {

        loadHealth();

    }, []);

    async function loadHealth() {

        try {

            const data = await getHealthScore();

            setHealth(data.health);

            setRecommendations(data.recommendations);

            setSummary(data.summary);

            setForecast(data.forecast);

        }

        catch (error) {

            console.log(error);

        }

        finally {

            setLoading(false);

        }

    }

    if (loading) {

        return (

            <div className="health-loading">

                Loading Cloud Cost Health...

            </div>

        );

    }

    return (

        <div className="health-container">

            <h1 className="health-title">

                Cloud Cost Health

            </h1>

            <HealthScoreCard
                score={health.score}
                status={health.status}
            />

            <ScoreBreakdown
                health={health}
            />

            <RecommendationCard
                recommendations={recommendations}
            />

        </div>

    );

}