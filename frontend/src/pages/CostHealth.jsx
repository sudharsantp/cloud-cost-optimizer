import { useEffect, useState } from "react";

import HealthScoreCard from "../components/HealthScoreCard";
import ScoreBreakdown from "../components/ScoreBreakdown";

import "../styles/CostHealth.css";


const API_URL = "http://127.0.0.1:8000";


export default function CostHealth() {

    const [data, setData] = useState(null);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState(null);


    useEffect(() => {

        loadHealth();

    }, []);


    async function loadHealth() {

        try {

            setLoading(true);
            setError(null);

            const response = await fetch(
                `${API_URL}/health/`
            );

            if (!response.ok) {
                throw new Error(
                    `Health API returned ${response.status}`
                );
            }

            const result =
                await response.json();

            setData(result);

        } catch (err) {

            console.error(
                "Cost Health error:",
                err
            );

            setError(
                "Unable to load Cost Health data."
            );

        } finally {

            setLoading(false);

        }

    }


    if (loading) {

        return (
            <div className="health-page-state">
                Loading Cost Health...
            </div>
        );

    }


    if (error || !data) {

        return (
            <div className="health-page-state error">
                {error || "No health data available."}
            </div>
        );

    }


    const health =
        data.health || {};

    const inputs =
        data.inputs || {};

    const forecast =
        data.forecast || {};

    const anomalyAnalysis =
        data.anomaly_analysis || {};

    const issues =
        data.issues || [];

    const factors =
        health.factors || [];


    const evidence =
        anomalyAnalysis.evidence || [];


    return (

        <div className="health-page">

            {/* =====================================
                PAGE HEADER
            ====================================== */}

            <div className="health-page-header">

                <div>

                    <h1>
                        Cloud Cost Health
                    </h1>

                    <p>
                        A data-driven assessment of
                        your current AWS cost environment.
                    </p>

                </div>


                <button
                    className="health-refresh-button"
                    onClick={loadHealth}
                >
                    Refresh Analysis
                </button>

            </div>


            {/* =====================================
                MAIN SCORE
            ====================================== */}

            <HealthScoreCard
                score={health.score}
                status={health.status}
            />


            {/* =====================================
                SCORE BREAKDOWN
            ====================================== */}

            <section className="health-section">

                <div className="health-section-heading">

                    <div>

                        <h2>
                            Score Breakdown
                        </h2>

                        <p>
                            Each component contributes
                            to the overall AWS Cost Health Score.
                        </p>

                    </div>

                </div>


                <ScoreBreakdown
                    health={health}
                />

            </section>


            {/* =====================================
                CURRENT SIGNALS
            ====================================== */}

            <section className="health-section">

                <div className="health-section-heading">

                    <div>

                        <h2>
                            Current Cost Health Signals
                        </h2>

                        <p>
                            Live values used by the health
                            scoring engine.
                        </p>

                    </div>

                </div>


                <div className="health-signal-grid">


                    <div className="health-signal-card">

                        <span>
                            30-Day Forecast
                        </span>

                        <strong>
                            $
                            {Number(
                                inputs.forecast_cost || 0
                            ).toFixed(2)}
                        </strong>

                        <small>
                            Predicted AWS spend
                        </small>

                    </div>


                    <div className="health-signal-card">

                        <span>
                            Application Budget
                        </span>

                        <strong
                            className={
                                inputs.budget_configured
                                    ? ""
                                    : "neutral-value"
                            }
                        >

                            {inputs.budget_configured
                                ? `$${Number(
                                    inputs.budget || 0
                                ).toFixed(2)}`
                                : "Not configured"}

                        </strong>

                        <small>
                            {inputs.budget_configured
                                ? "Configured"
                                : "Risk cannot be fully evaluated"}
                        </small>

                    </div>


                    <div className="health-signal-card">

                        <span>
                            Cost-Risk Anomalies
                        </span>

                        <strong
                            className={
                                Number(
                                    anomalyAnalysis.cost_risk_anomalies || 0
                                ) > 0
                                    ? "danger-value"
                                    : ""
                            }
                        >

                            {
                                anomalyAnalysis.cost_risk_anomalies
                                || 0
                            }

                        </strong>

                        <small>
                            High-impact billing anomalies
                        </small>

                    </div>


                    <div className="health-signal-card">

                        <span>
                            Statistical Outliers
                        </span>

                        <strong>
                            {
                                anomalyAnalysis.total_detected
                                || 0
                            }
                        </strong>

                        <small>
                            Detected by Isolation Forest
                        </small>

                    </div>


                    <div className="health-signal-card">

                        <span>
                            Optimization Findings
                        </span>

                        <strong>
                            {
                                inputs.optimization_findings
                                || 0
                            }
                        </strong>

                        <small>
                            AWS resource findings
                        </small>

                    </div>


                    <div className="health-signal-card">

                        <span>
                            Monthly Savings
                        </span>

                        <strong>
                            $
                            {Number(
                                inputs.estimated_monthly_savings || 0
                            ).toFixed(2)}
                        </strong>

                        <small>
                            Estimated optimization savings
                        </small>

                    </div>


                </div>

            </section>


            {/* =====================================
                FACTORS
            ====================================== */}

            <section className="health-section">

                <div className="health-section-heading">

                    <div>

                        <h2>
                            Factors Affecting Cost Health
                        </h2>

                        <p>
                            These are the actual signals
                            affecting the current score.
                        </p>

                    </div>

                </div>


                <div className="factor-list">

                    {factors.map(
                        (factor) => (

                            <div
                                className={
                                    `factor-card ${factor.status}`
                                }
                                key={factor.key}
                            >

                                <div className="factor-top">

                                    <div>

                                        <h3>
                                            {factor.name}
                                        </h3>

                                        <span
                                            className={
                                                "factor-status"
                                            }
                                        >
                                            {factor.status}
                                        </span>

                                    </div>


                                    <div className="factor-score">

                                        <strong>
                                            {factor.score}
                                        </strong>

                                        <span>
                                            / {factor.maximum}
                                        </span>

                                    </div>

                                </div>


                                <div className="factor-progress">

                                    <div
                                        style={{
                                            width: `${(
                                                factor.score /
                                                factor.maximum
                                            ) * 100}%`
                                        }}
                                    />

                                </div>


                                <p>
                                    {factor.reason}
                                </p>


                                {factor.impact > 0 && (

                                    <div className="factor-impact">

                                        Score impact:
                                        {" "}
                                        <strong>
                                            -{factor.impact}
                                        </strong>

                                    </div>

                                )}

                            </div>

                        )
                    )}

                </div>

            </section>


            {/* =====================================
                ANOMALY EVIDENCE
            ====================================== */}

            {evidence.length > 0 && (

                <section className="health-section">

                    <div className="health-section-heading">

                        <div>

                            <h2>
                                Cost-Risk Anomaly Evidence
                            </h2>

                            <p>
                                Statistical anomalies that
                                represent increased cost risk.
                            </p>

                        </div>

                    </div>


                    <div className="anomaly-evidence-grid">

                        {evidence.map(
                            (anomaly) => (

                                <div
                                    className={
                                        `anomaly-evidence-card ${anomaly.severity}`
                                    }
                                    key={anomaly.id}
                                >

                                    <div className="anomaly-header">

                                        <div>

                                            <h3>
                                                {anomaly.service}
                                            </h3>

                                            <span>
                                                {anomaly.date}
                                            </span>

                                        </div>


                                        <span className="anomaly-severity">
                                            {anomaly.severity}
                                        </span>

                                    </div>


                                    <div className="anomaly-metrics">

                                        <div>

                                            <span>
                                                Actual Cost
                                            </span>

                                            <strong>
                                                $
                                                {Number(
                                                    anomaly.actual_cost || 0
                                                ).toFixed(4)}
                                            </strong>

                                        </div>


                                        <div>

                                            <span>
                                                Expected Cost
                                            </span>

                                            <strong>
                                                $
                                                {Number(
                                                    anomaly.expected_cost || 0
                                                ).toFixed(4)}
                                            </strong>

                                        </div>


                                        <div>

                                            <span>
                                                Deviation
                                            </span>

                                            <strong>
                                                +
                                                {Math.abs(
                                                    Number(
                                                        anomaly.deviation_percent || 0
                                                    )
                                                )}%
                                            </strong>

                                        </div>

                                    </div>


                                    <p className="anomaly-details">

                                        {anomaly.details}

                                    </p>


                                    <div className="anomaly-method">

                                        Detection method:
                                        {" "}
                                        <strong>
                                            {
                                                anomaly.detection_method
                                            }
                                        </strong>

                                    </div>

                                </div>

                            )
                        )}

                    </div>

                </section>

            )}


            {/* =====================================
                FORECAST
            ====================================== */}

            <section className="health-section">

                <div className="health-section-heading">

                    <div>

                        <h2>
                            Forecast Risk
                        </h2>

                        <p>
                            Predicted AWS spending based on
                            the current forecasting model.
                        </p>

                    </div>

                </div>


                <div className="forecast-grid">

                    <div className="forecast-card">

                        <span>
                            Tomorrow
                        </span>

                        <strong>
                            $
                            {Number(
                                forecast.tomorrow_prediction || 0
                            ).toFixed(4)}
                        </strong>

                    </div>


                    <div className="forecast-card">

                        <span>
                            Next 7 Days
                        </span>

                        <strong>
                            $
                            {Number(
                                forecast.next_7_days_total || 0
                            ).toFixed(2)}
                        </strong>

                    </div>


                    <div className="forecast-card">

                        <span>
                            Next 30 Days
                        </span>

                        <strong>
                            $
                            {Number(
                                forecast.next_30_days_total || 0
                            ).toFixed(2)}
                        </strong>

                    </div>


                    <div className="forecast-card">

                        <span>
                            Highest Predicted Day
                        </span>

                        <strong>
                            $
                            {Number(
                                forecast.highest_cost || 0
                            ).toFixed(4)}
                        </strong>

                        <small>
                            {
                                forecast.highest_predicted_day
                                    ? new Date(
                                        forecast.highest_predicted_day
                                    ).toLocaleDateString()
                                    : "-"
                            }
                        </small>

                    </div>

                </div>

            </section>


            {/* =====================================
                NO AI RECOMMENDATION COMPONENT HERE
            ====================================== */}

        </div>

    );

}