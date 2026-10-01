# AI-Powered AWS Cloud Cost Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![React](https://img.shields.io/badge/React-Frontend-61DAFB)
![AWS](https://img.shields.io/badge/AWS-Cloud-orange)
![Machine Learning](https://img.shields.io/badge/ML-Prophet%20%7C%20ARIMA-red)
![Database](https://img.shields.io/badge/Database-SQLite-lightgrey)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Overview

The **AI-Powered AWS Cloud Cost Intelligence Platform** is a FinOps-oriented cloud cost analytics and optimization platform designed to help organizations understand, forecast, and optimize their AWS spending.

The platform integrates **AWS Cost Explorer, AWS CloudWatch, and the AWS Pricing API** to collect cost and resource information. Historical cost data is analyzed using **Prophet and ARIMA forecasting models** to estimate future spending.

The platform also provides an automated **Cost Health Score**, cost optimization recommendations, anomaly insights, and EC2 deployment cost simulation through an interactive React dashboard.

---

# Key Highlights

- Automated **Cost Health Score (0–100)**
- AWS Cost Analytics
- Service-wise cost analysis
- Prophet & ARIMA forecasting
- 30-day cost forecasting
- Forecast model comparison
- AWS Pricing API integration
- AWS Cost Explorer integration
- CloudWatch monitoring
- EC2 deployment cost simulation
- Cost optimization recommendations
- Interactive React dashboard

---

# Features

## 1. AWS Cost Analytics

Analyze AWS spending through a centralized dashboard.

### Capabilities

- Daily AWS cost analysis
- Historical cost tracking
- Service-wise cost breakdown
- Cost trend visualization
- Spending analysis
- AWS Cost Explorer integration

---

# 2. AI Cost Forecasting

The platform uses time-series forecasting techniques to estimate future AWS spending.

## Prophet Forecasting

Prophet is used for:

- Time-series forecasting
- Trend analysis
- Future cost estimation
- 30-day cost prediction

## ARIMA Forecasting

ARIMA is used for:

- Statistical time-series forecasting
- Historical spending analysis
- Future cost estimation

## Forecast Comparison

The platform provides:

- Prophet vs ARIMA predictions
- Forecast summaries
- Future cost visualization
- Model-based spending insights

---

# 3. Cost Health Score

The platform provides an automated **Cost Health Score from 0–100** to summarize the financial health of cloud spending.

The health assessment considers cost-related signals and optimization indicators to provide an overall view of AWS cost efficiency.

### Features

- Cost Health Score
- Health status indicators
- Cost efficiency analysis
- Health score breakdown
- Optimization recommendations
- Actionable FinOps insights

---

# 4. Cost Optimization Recommendations

The recommendation engine analyzes available cost information and identifies potential optimization opportunities.

### Example Insights

- High-cost services
- Spending trends
- Potential cost optimization areas
- Resource utilization-related insights
- Recommended actions

The recommendations are presented through the dashboard to help users investigate potential areas for cost reduction.

---

# 5. AWS CloudWatch Monitoring

The platform integrates AWS CloudWatch to provide resource utilization information alongside cost data.

### Capabilities

- CloudWatch metric integration
- Resource monitoring
- Historical metric visualization
- Utilization insights

---

# 6. EC2 Cost Simulation

The platform allows users to estimate EC2 infrastructure costs before deploying resources.

### Simulation Parameters

- AWS Region
- EC2 Instance Type
- Operating System
- Storage Type
- Storage Size
- Usage Hours

This provides users with an estimated infrastructure cost before provisioning resources.

---

# 7. Interactive Dashboard

The React-based dashboard provides a centralized interface for AWS cost intelligence.

### Dashboard Components

- Cost analytics
- Cost trends
- Service distribution
- Forecasting
- Forecast comparison
- EC2 cost simulation
- Cost Health Score
- Optimization recommendations

---

# Technology Stack

## Frontend

- React
- Vite
- Axios
- Chart.js

## Backend

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pandas
- NumPy

## Machine Learning & Analytics

- Prophet
- ARIMA
- Statsmodels
- Scikit-learn

## AWS

- AWS Cost Explorer
- AWS CloudWatch
- AWS Pricing API
- Boto3

## Development Tools

- Git
- GitHub
- Postman
- Uvicorn

---

# System Architecture

```text
                         ┌──────────────────────┐
                         │    React Frontend    │
                         │      Dashboard       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    FastAPI Backend   │
                         └──────────┬───────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
      ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
      │ Cost Analytics│     │ Forecasting   │     │ Cost Health & │
      │    Engine     │     │    Engine     │     │ Recommendations│
      └───────┬───────┘     └───────┬───────┘     └───────┬───────┘
              │                     │                     │
              └─────────────────────┼─────────────────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   SQLite Database    │
                         └──────────────────────┘
                                    ▲
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
      ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
      │ AWS Cost      │     │ AWS CloudWatch│     │ AWS Pricing   │
      │ Explorer      │     │               │     │ API           │
      └───────────────┘     └───────────────┘     └───────────────┘

                         Forecasting Models
                         ┌─────────┬─────────┐
                         │ Prophet │  ARIMA  │
                         └─────────┴─────────┘
