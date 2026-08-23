import { useEffect, useState } from "react";
import "../styles/Recommendations.css";

const API = "http://127.0.0.1:8000";

export default function Recommendations() {
    const [health, setHealth] = useState(null);
    const [optimization, setOptimization] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const loadData = async () => {
        try {
            setLoading(true);
            setError("");

            const [healthRes, optimizeRes] = await Promise.all([
                fetch(`${API}/health/`),
                fetch(`${API}/optimize/`),
            ]);

            if (!healthRes.ok) throw new Error("Health API failed");
            if (!optimizeRes.ok) throw new Error("Optimization API failed");

            const healthData = await healthRes.json();
            const optimizeData = await optimizeRes.json();

            setHealth(healthData);
            setOptimization(optimizeData);
        } catch (err) {
            console.error(err);
            setError("Unable to load live AWS recommendation data.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadData();
    }, []);

    if (loading) {
        return (
            <div className="recommendations-page">
                <div className="loading-card">
                    <div className="spinner"></div>
                    <h2>Analyzing AWS cost data...</h2>
                    <p>
                        Reading billing anomalies, forecast risk, budgets and resource
                        optimization findings.
                    </p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="recommendations-page">
                <div className="error-card">
                    <h2>Unable to load recommendations</h2>
                    <p>{error}</p>
                    <button onClick={loadData}>Retry Analysis</button>
                </div>
            </div>
        );
    }

    const inputs = health?.inputs || {};
    const forecast = health?.forecast || {};
    const anomalyAnalysis = health?.anomaly_analysis || {};
    const evidence = anomalyAnalysis?.evidence || [];

    const optimizationFindings =
        optimization?.findings ||
        optimization?.recommendations ||
        optimization?.optimization_findings ||
        [];

    const recommendations = [];

    // --------------------------------------------------
    // 1. COST-RISK ANOMALIES
    // --------------------------------------------------

    evidence
        .filter(
            (item) =>
                ["critical", "high"].includes(
                    String(item.severity || "").toLowerCase()
                ) && Number(item.deviation_percent || 0) > 0
        )
        .forEach((item) => {
            const severity = String(item.severity).toLowerCase();

            recommendations.push({
                type: severity === "critical" ? "critical" : "high",
                title: `${item.service} cost anomaly detected`,
                source: "Live billing anomaly analysis",
                metric: `+${Number(item.deviation_percent).toFixed(0)}%`,
                metricLabel: "above expected",
                reason:
                    `Actual cost was $${Number(item.actual_cost).toFixed(4)} ` +
                    `against an expected baseline of $${Number(
                        item.expected_cost
                    ).toFixed(4)}.`,
                action:
                    `Review recent ${item.service} usage and billing activity. ` +
                    `Investigate whether increased usage, API activity, or an unexpected ` +
                    `configuration caused the increase.`,
                date: item.date,
                method: item.detection_method,
            });
        });

    // --------------------------------------------------
    // 2. BUDGET
    // --------------------------------------------------

    if (!inputs.budget_configured) {
        recommendations.push({
            type: "medium",
            title: "Configure an application budget",
            source: "Budget configuration analysis",
            metric: "NOT SET",
            metricLabel: "budget",
            reason:
                "No application budget is currently configured, so the system cannot " +
                "evaluate forecasted spending against a defined spending limit.",
            action:
                "Configure a monthly AWS application budget and establish alert " +
                "thresholds for abnormal cost growth.",
        });
    }

    // --------------------------------------------------
    // 3. FORECAST
    // --------------------------------------------------

    const forecast30 = Number(inputs.forecast_cost || 0);

    if (forecast30 > 0) {
        recommendations.push({
            type: "medium",
            title: "Monitor projected 30-day spending",
            source: "Forecasting engine",
            metric: `$${forecast30.toFixed(2)}`,
            metricLabel: "30-day forecast",
            reason:
                "The forecasting engine projects approximately $" +
                forecast30.toFixed(2) +
                " in AWS cost over the next 30 days.",
            action:
                "Use the forecast as a spending baseline and configure a budget or " +
                "alert threshold before projected costs increase unexpectedly.",
            extra:
                forecast.highest_predicted_day
                    ? `Highest predicted daily cost: $${Number(
                        forecast.highest_cost || 0
                    ).toFixed(4)} on ${new Date(
                        forecast.highest_predicted_day
                    ).toLocaleDateString()}.`
                    : null,
        });
    }

    // --------------------------------------------------
    // 4. RESOURCE OPTIMIZATION
    // --------------------------------------------------

    if (Array.isArray(optimizationFindings) && optimizationFindings.length > 0) {
        optimizationFindings.forEach((item) => {
            recommendations.push({
                type: "savings",
                title:
                    item.title ||
                    item.recommendation ||
                    item.resource_type ||
                    "AWS resource optimization opportunity",
                source: "Live AWS resource analysis",
                metric:
                    item.estimated_monthly_savings != null
                        ? `$${Number(item.estimated_monthly_savings).toFixed(2)}`
                        : "ACTION",
                metricLabel:
                    item.estimated_monthly_savings != null
                        ? "monthly savings"
                        : "optimization",
                reason:
                    item.reason ||
                    item.description ||
                    "The live AWS resource analysis identified an optimization opportunity.",
                action:
                    item.action ||
                    item.recommendation ||
                    "Review this resource and apply the suggested optimization.",
            });
        });
    }

    // --------------------------------------------------
    // 5. NO RESOURCE FINDINGS
    // --------------------------------------------------

    const findingCount = Number(inputs.optimization_findings || 0);

    if (findingCount === 0) {
        recommendations.push({
            type: "healthy",
            title: "No idle-resource cleanup required",
            source: "Live AWS resource analysis",
            metric: "0",
            metricLabel: "optimization findings",
            reason:
                "The current resource analysis found no actionable EC2, EBS or " +
                "Elastic IP optimization findings.",
            action:
                "No resource cleanup action is currently required. Continue monitoring " +
                "resource utilization as the AWS environment changes.",
        });
    }

    const criticalCount = recommendations.filter(
        (r) => r.type === "critical"
    ).length;

    const highCount = recommendations.filter(
        (r) => r.type === "high"
    ).length;

    const actionCount = recommendations.filter(
        (r) => !["healthy"].includes(r.type)
    ).length;

    return (
        <div className="recommendations-page">
            <div className="recommendations-container">

                {/* HEADER */}
                <div className="page-header">
                    <div>
                        <h1>AWS Cost Recommendations</h1>
                        <p>
                            Data-driven actions generated from your current AWS billing,
                            forecast and resource analysis.
                        </p>
                    </div>

                    <button className="refresh-button" onClick={loadData}>
                        Refresh Analysis
                    </button>
                </div>

                {/* SUMMARY */}
                <div className="summary-grid">

                    <div className="summary-card">
                        <span>Actions Identified</span>
                        <strong>{actionCount}</strong>
                        <small>Current cost signals</small>
                    </div>

                    <div className="summary-card critical-summary">
                        <span>Critical</span>
                        <strong>{criticalCount}</strong>
                        <small>Immediate attention</small>
                    </div>

                    <div className="summary-card">
                        <span>High Priority</span>
                        <strong>{highCount}</strong>
                        <small>Requires investigation</small>
                    </div>

                    <div className="summary-card">
                        <span>30-Day Forecast</span>
                        <strong>${forecast30.toFixed(2)}</strong>
                        <small>Projected AWS cost</small>
                    </div>

                </div>

                {/* LIVE SOURCE */}
                <div className="live-banner">
                    <span className="live-dot"></span>
                    LIVE AWS DATA
                    <span className="live-description">
                        Recommendations are derived from current backend analysis.
                    </span>
                </div>

                {/* RECOMMENDATIONS */}
                <section>
                    <div className="section-heading">
                        <h2>Recommended Actions</h2>
                        <p>
                            Each recommendation is linked to an observed AWS cost signal.
                        </p>
                    </div>

                    <div className="recommendation-grid">

                        {recommendations.map((item, index) => (
                            <RecommendationCard
                                key={`${item.title}-${index}`}
                                recommendation={item}
                            />
                        ))}

                    </div>
                </section>

                {/* RESOURCE STATUS */}
                <section className="resource-section">

                    <div className="section-heading">
                        <h2>Resource Optimization Status</h2>
                        <p>
                            Current findings from the live AWS resource optimization engine.
                        </p>
                    </div>

                    <div className="resource-grid">

                        <ResourceStatus
                            title="EC2 Instances"
                            value={optimization?.running_ec2_instances ?? 0}
                            description="Checked for CPU utilization and underutilization."
                        />

                        <ResourceStatus
                            title="EBS Volumes"
                            value={optimization?.ebs_volumes ?? 0}
                            description="Checked for unattached storage."
                        />

                        <ResourceStatus
                            title="Elastic IPs"
                            value={optimization?.elastic_ips ?? 0}
                            description="Checked for unused Elastic IP addresses."
                        />

                    </div>

                </section>

                {/* EXPLANATION */}
                <div className="method-card">
                    <h3>How recommendations are generated</h3>

                    <p>
                        Recommendations are not static messages. The page evaluates live
                        backend signals from billing anomaly detection, forecasting,
                        budget configuration and AWS resource analysis.
                    </p>

                    <div className="method-row">
                        <span>Billing anomalies</span>
                        <b>Isolation Forest</b>
                    </div>

                    <div className="method-row">
                        <span>Cost forecast</span>
                        <b>Forecasting engine</b>
                    </div>

                    <div className="method-row">
                        <span>Resource optimization</span>
                        <b>Live AWS resource analysis</b>
                    </div>

                    <div className="method-row">
                        <span>Budget risk</span>
                        <b>Application budget configuration</b>
                    </div>
                </div>

            </div>
        </div>
    );
}


/* =====================================================
   RECOMMENDATION CARD
===================================================== */

function RecommendationCard({ recommendation }) {
    const icons = {
        critical: "🔴",
        high: "🟠",
        medium: "🟡",
        savings: "💰",
        healthy: "✓",
    };

    return (
        <div className={`recommendation-card ${recommendation.type}`}>

            <div className="recommendation-top">

                <div className="recommendation-icon">
                    {icons[recommendation.type] || "ℹ️"}
                </div>

                <div className="recommendation-source">
                    {recommendation.source}
                </div>

                <span className={`severity ${recommendation.type}`}>
                    {recommendation.type.toUpperCase()}
                </span>

            </div>

            <h3>{recommendation.title}</h3>

            <div className="recommendation-metric">
                <strong>{recommendation.metric}</strong>
                <span>{recommendation.metricLabel}</span>
            </div>

            <div className="recommendation-reason">
                <strong>Why this was detected</strong>
                <p>{recommendation.reason}</p>
            </div>

            <div className="recommendation-action">
                <strong>Recommended action</strong>
                <p>{recommendation.action}</p>
            </div>

            {recommendation.extra && (
                <div className="recommendation-extra">
                    {recommendation.extra}
                </div>
            )}

            {recommendation.method && (
                <div className="recommendation-footer">
                    Detection method: <b>{recommendation.method}</b>
                    {recommendation.date && (
                        <>
                            {" "}• Detected: <b>{recommendation.date}</b>
                        </>
                    )}
                </div>
            )}

        </div>
    );
}


/* =====================================================
   RESOURCE STATUS
===================================================== */

function ResourceStatus({ title, value, description }) {
    return (
        <div className="resource-card">

            <div className="resource-header">
                <h3>{title}</h3>
                <strong>{value}</strong>
            </div>

            <p>{description}</p>

            <div className="resource-status">
                {Number(value) === 0
                    ? "✓ No actionable findings detected."
                    : `${value} resource(s) require analysis.`}
            </div>

        </div>
    );
}