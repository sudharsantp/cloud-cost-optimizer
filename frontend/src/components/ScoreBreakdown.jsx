import React from "react";

export default function ScoreBreakdown({ health }) {

    const metrics = [

        {
            title: "Forecast",
            value: health.forecast_score,
            max: 20
        },

        {
            title: "Idle Resources",
            value: health.idle_score,
            max: 25
        },

        {
            title: "Budget",
            value: health.budget_score,
            max: 15
        },

        {
            title: "Anomaly",
            value: health.anomaly_score,
            max: 15
        },

        {
            title: "Savings",
            value: health.savings_score,
            max: 10
        },

        {
            title: "Utilization",
            value: health.utilization_score,
            max: 15
        }

    ];

    return (

        <div className="breakdown-grid">

            {metrics.map((item) => {

                const percentage = (item.value / item.max) * 100;

                return (

                    <div
                        key={item.title}
                        className="metric-card"
                    >

                        <div className="metric-header">

                            <span>{item.title}</span>

                            <span>

                                {item.value}/{item.max}

                            </span>

                        </div>

                        <div className="progress-bar">

                            <div
                                className="progress-fill"
                                style={{
                                    width: `${percentage}%`
                                }}
                            />

                        </div>

                    </div>

                );

            })}

        </div>

    );

}