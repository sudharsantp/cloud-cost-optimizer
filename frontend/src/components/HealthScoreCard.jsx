import React from "react";

export default function HealthScoreCard({ score, status }) {

    const getColor = () => {

        if (score >= 90) return "#22c55e";   // Green

        if (score >= 75) return "#3b82f6";   // Blue

        if (score >= 60) return "#f59e0b";   // Orange

        if (score >= 40) return "#ef4444";   // Red

        return "#991b1b";

    };

    return (

        <div className="score-card">

            <div
                className="score-circle"
                style={{
                    borderColor: getColor(),
                    color: getColor()
                }}
            >

                {score}

            </div>

            <h2
                className="score-status"
                style={{
                    color: getColor()
                }}
            >
                {status}
            </h2>

            <p className="score-description">

                Overall AWS Cost Health Score

            </p>

        </div>

    );

}