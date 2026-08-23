export default function HealthScoreCard({
    score,
    status,
}) {

    const safeScore =
        Math.max(
            0,
            Math.min(100, Number(score || 0))
        );

    return (
        <div className="health-score-card">

            <div
                className="health-score-ring"
                style={{
                    "--score": `${safeScore * 3.6}deg`,
                }}
            >

                <div className="health-score-inner">

                    <strong>
                        {safeScore}
                    </strong>

                </div>

            </div>


            <h2>
                {status}
            </h2>

            <p>
                Overall AWS Cost Health Score
            </p>

        </div>
    );
}