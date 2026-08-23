export default function ScoreBreakdown({ health }) {

    const breakdown = health?.score_breakdown || {};

    const items = [
        {
            key: "forecast",
            label: "Forecast",
        },
        {
            key: "idle_resources",
            label: "Idle Resources",
        },
        {
            key: "budget",
            label: "Budget",
        },
        {
            key: "anomaly",
            label: "Billing Anomalies",
        },
        {
            key: "savings",
            label: "Savings Opportunity",
        },
        {
            key: "utilization",
            label: "EC2 Utilization",
        },
    ];

    return (
        <div className="score-breakdown-grid">

            {items.map((item) => {

                const value =
                    breakdown[item.key] || {};

                const score =
                    Number(value.score || 0);

                const maximum =
                    Number(value.maximum || 0);

                const percentage =
                    maximum > 0
                        ? (score / maximum) * 100
                        : 0;

                return (
                    <div
                        className="score-breakdown-card"
                        key={item.key}
                    >

                        <div className="score-breakdown-top">

                            <div>
                                <h3>
                                    {item.label}
                                </h3>

                                <span>
                                    {score} / {maximum}
                                </span>
                            </div>

                            <strong>
                                {Math.round(percentage)}%
                            </strong>

                        </div>

                        <div className="score-breakdown-bar">

                            <div
                                style={{
                                    width: `${percentage}%`,
                                }}
                            />

                        </div>

                        {Number(value.impact || 0) > 0 && (

                            <p>
                                Score impact: -
                                {value.impact}
                            </p>

                        )}

                    </div>
                );

            })}

        </div>
    );
}