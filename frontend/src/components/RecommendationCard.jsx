import React from "react";

export default function RecommendationCard({ recommendations }) {

    if (!recommendations || recommendations.length === 0) {

        return (

            <div className="recommendation-card">

                <div className="recommendation-header">

                    💡 AI Recommendations

                </div>

                <div className="recommendation-body">

                    No recommendations available.

                </div>

            </div>

        );

    }

    return (

        <div className="recommendation-card">

            <div className="recommendation-header">

                💡 AI Recommendations

            </div>

            {recommendations.map((item, index) => (

                <div
                    key={index}
                    className="recommendation-item"
                >

                    <h3>{item.title}</h3>

                    <p>
                        <strong>Priority:</strong> {item.priority}
                    </p>

                    <p>
                        <strong>Service:</strong> {item.service}
                    </p>

                    <p>
                        <strong>Resource:</strong> {item.resource}
                    </p>

                    <p>
                        <strong>Reason:</strong> {item.reason}
                    </p>

                    <p>
                        <strong>Estimated Savings:</strong> ${item.estimated_monthly_savings}
                    </p>

                    <p>
                        <strong>Health Score Gain:</strong> +{item.health_score_gain}
                    </p>

                    <p>
                        <strong>Confidence:</strong> {item.confidence}%
                    </p>

                    <hr />

                </div>

            ))}

        </div>

    );

}