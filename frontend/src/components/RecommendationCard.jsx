import React from "react";

export default function RecommendationCard({ recommendation }) {
    const {
        type,
        priority,
        service,
        resource_id,
        resource_type,
        reason,
        metric,
        estimated_monthly_savings,
        action,
        detection_method,
        detected_on,
    } = recommendation;

    // =========================================================
    // Determine card severity
    // =========================================================

    const getSeverity = () => {

        // Underutilized EC2 is an actionable cost issue.
        if (type === "UNDERUTILIZED_EC2") {
            return "critical";
        }

        if (priority === "CRITICAL") {
            return "critical";
        }

        if (priority === "HIGH") {
            return "critical";
        }

        if (priority === "MEDIUM") {
            return "warning";
        }

        if (priority === "LOW") {
            return "warning";
        }

        return "healthy";
    };

    const severity = getSeverity();

    // =========================================================
    // Badge text
    // =========================================================

    const getBadgeText = () => {

        if (type === "UNDERUTILIZED_EC2") {
            return "ACTION REQUIRED";
        }

        if (priority) {
            return priority;
        }

        return "HEALTHY";
    };

    // =========================================================
    // Icon
    // =========================================================

    const getIcon = () => {

        if (severity === "critical") {
            return "🔴";
        }

        if (severity === "warning") {
            return "🟡";
        }

        return "🟢";
    };

    // =========================================================
    // Recommendation category
    // =========================================================

    const getCategory = () => {

        if (type === "UNDERUTILIZED_EC2") {
            return "EC2 utilization analysis";
        }

        if (type === "UNATTACHED_EBS") {
            return "Live AWS resource analysis";
        }

        if (type === "UNUSED_ELASTIC_IP") {
            return "Live AWS resource analysis";
        }

        if (service === "EC2") {
            return "Live AWS resource analysis";
        }

        return "AWS cost analysis";
    };

    // =========================================================
    // Savings display
    // =========================================================

    const hasSavings =
        typeof estimated_monthly_savings === "number" &&
        estimated_monthly_savings > 0;

    // =========================================================
    // CPU display
    // =========================================================

    const cpuValue =
        metric &&
            typeof metric.cpu_utilization === "number"
            ? metric.cpu_utilization
            : null;

    // =========================================================
    // Resource title
    // =========================================================

    const getTitle = () => {

        if (type === "UNDERUTILIZED_EC2") {
            return "EC2 instance may be underutilized";
        }

        if (type === "UNATTACHED_EBS") {
            return "Unattached EBS volume detected";
        }

        if (type === "UNUSED_ELASTIC_IP") {
            return "Unused Elastic IP detected";
        }

        return "AWS cost optimization opportunity";
    };

    return (
        <div className={`recommendation-card ${severity}`}>

            {/* =================================================
                HEADER
            ================================================= */}

            <div className="recommendation-header">

                <div className="recommendation-source">

                    <span className="recommendation-icon">
                        {getIcon()}
                    </span>

                    <span>
                        {getCategory()}
                    </span>

                </div>

                <span className={`recommendation-badge ${severity}`}>
                    {getBadgeText()}
                </span>

            </div>


            {/* =================================================
                RESOURCE
            ================================================= */}

            <div className="recommendation-resource">

                {resource_type || service}

                {resource_id && (
                    <div className="recommendation-resource-id">
                        {resource_id}
                    </div>
                )}

            </div>


            {/* =================================================
                TITLE
            ================================================= */}

            <h3 className="recommendation-title">
                {getTitle()}
            </h3>


            {/* =================================================
                CPU METRIC
            ================================================= */}

            {cpuValue !== null && (

                <div className="recommendation-metric">

                    <div className="metric-label">
                        Average CPU Utilization
                    </div>

                    <div className="metric-value">
                        {cpuValue.toFixed(2)}%
                    </div>

                </div>

            )}


            {/* =================================================
                SAVINGS
            ================================================= */}

            <div className="recommendation-savings">

                {hasSavings ? (

                    <>
                        <strong>
                            ${estimated_monthly_savings.toFixed(2)}
                        </strong>

                        <span>
                            estimated monthly savings
                        </span>
                    </>

                ) : (

                    <>
                        <strong>
                            —
                        </strong>

                        <span>
                            savings requires pricing analysis
                        </span>
                    </>

                )}

            </div>


            {/* =================================================
                WHY DETECTED
            ================================================= */}

            <div className="recommendation-section">

                <h4>
                    Why this was detected
                </h4>

                <p>
                    {reason ||
                        "The AWS resource analysis identified a potential cost optimization opportunity."
                    }
                </p>

            </div>


            {/* =================================================
                RECOMMENDED ACTION
            ================================================= */}

            <div className="recommendation-section">

                <h4>
                    Recommended action
                </h4>

                <p>
                    {action ||
                        "Review the resource and determine whether optimization is appropriate."
                    }
                </p>

            </div>


            {/* =================================================
                FOOTER
            ================================================= */}

            <div className="recommendation-footer">

                {detection_method && (
                    <span>
                        Detection method:{" "}
                        <strong>
                            {detection_method}
                        </strong>
                    </span>
                )}

                {detected_on && (
                    <span>
                        Detected:{" "}
                        {new Date(
                            detected_on
                        ).toLocaleDateString()}
                    </span>
                )}

            </div>

        </div>
    );
}