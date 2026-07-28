# AI-Powered AWS Cloud Cost Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![React](https://img.shields.io/badge/React-Frontend-61DAFB)
![AWS](https://img.shields.io/badge/AWS-Cloud-orange)
![Machine Learning](https://img.shields.io/badge/ML-Prophet%20%7C%20ARIMA-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## Overview

The **AI-Powered AWS Cloud Cost Intelligence Platform** is a FinOps-inspired cloud cost optimization solution that enables organizations to monitor AWS spending, forecast future cloud costs, estimate deployment expenses before provisioning resources, and evaluate overall cloud financial health through an AI-driven **Cost Health Score**.

The platform integrates **AWS Cost Explorer**, **AWS CloudWatch**, and the **AWS Pricing API** with machine learning forecasting models (**Prophet** and **ARIMA**) to provide actionable insights that help reduce cloud expenditure and improve cost efficiency.

---

# Key Highlights

- AI-based **Cost Health Score (0–100)**
- Real-time AWS Cost Analytics
- Prophet & ARIMA Cost Forecasting
- 30-Day Cost Prediction
- EC2 Deployment Cost Simulation
- AWS Cost Explorer Integration
- AWS Pricing API Integration
- Interactive Dashboard
- Intelligent Cost Optimization Recommendations

---

# Features

## Cost Analytics

- Real-time AWS billing dashboard
- Daily cost monitoring
- Service-wise cost breakdown
- Historical spending visualization
- Cost trend analysis

---

## AI Cost Forecasting

Forecast future AWS spending using multiple forecasting models.

### Prophet Forecasting

- Time-series forecasting
- Trend detection
- 30-day cost prediction

### ARIMA Forecasting

- Statistical forecasting
- Historical trend analysis
- Future expense estimation

### Forecast Comparison

- Prophet vs ARIMA comparison
- Prediction summary
- Forecast visualization

---

## AI Cost Health Assessment

Evaluate the overall financial health of your AWS account.

Features include:

- AI-generated Cost Health Score (0–100)
- Spending efficiency assessment
- Resource utilization insights
- Cost optimization recommendations
- Health score breakdown
- Actionable FinOps suggestions

---

## CloudWatch Monitoring

Monitor cloud resource utilization alongside spending.

- CloudWatch metrics integration
- Resource monitoring
- Historical metric visualization
- Performance insights

---

## EC2 Cost Simulation

Estimate infrastructure expenses before deploying EC2 instances.

Simulation Parameters

- AWS Region
- Instance Type
- Operating System
- Storage Type
- Storage Size
- Usage Hours

This enables users to evaluate deployment costs before provisioning cloud infrastructure.

---

## Interactive Dashboard

The web dashboard provides:

- Cost analytics
- Forecast graphs
- Service distribution charts
- EC2 simulation results
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

- FastAPI
- SQLAlchemy
- SQLite
- Pandas
- NumPy

## Machine Learning

- Prophet
- ARIMA (Statsmodels)

## AWS Services

- AWS Cost Explorer API
- AWS CloudWatch
- AWS Pricing API
- Boto3 SDK

---

# Project Architecture

```text
                    React Frontend
                          │
                          ▼
                  FastAPI Backend
                          │
     ┌─────────────────────────────────────┐
     │        Analytics Engine             │
     │        Forecast Engine              │
     │        Cost Health Engine           │
     │        Simulation Engine            │
     └─────────────────────────────────────┘
               │                │
               ▼                ▼
     AWS Cost Explorer     AWS Pricing API
               │                │
               └────────┬───────┘
                        ▼
                 SQLite Database
                        │
                        ▼
             Prophet & ARIMA Models
```

---

# API Endpoints

## Analytics

```
GET /analytics/daily-cost
GET /analytics/service-breakdown
```

## Prediction

```
GET /prediction/arima
GET /prediction/summary
GET /prediction/compare
GET /prediction/next-30-days
```

## Cost Health

```
GET /health/score
GET /health/recommendations
GET /health/breakdown
```

## Simulation

```
POST /simulation/ec2
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/sudharsantp/cloud-cost-optimizer.git

cd cloud-cost-optimizer
```

---

## Backend Setup

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file

```env
AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY
AWS_REGION=ap-south-1
```

Run the backend

```bash
uvicorn app.main:app --reload
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

---

# Why This Project?

Cloud cost management often requires navigating multiple AWS services such as Cost Explorer, CloudWatch, and Pricing APIs separately.

This platform consolidates analytics, forecasting, deployment cost estimation, and AI-driven financial health assessment into a single dashboard, enabling users to make informed decisions before unnecessary cloud expenses occur.

---

# Future Enhancements

- AI-powered Cost Anomaly Detection
- Budget Burn Rate Prediction
- Reserved Instance Savings Advisor
- Rightsizing Recommendations
- Automated Weekly Cost Reports
- PDF & CSV Report Generation
- Docker Deployment
- Kubernetes Cost Monitoring
- Multi-Cloud Support (Azure & GCP)

---

# Screenshots

> Add screenshots here after deployment.

### Dashboard

```
assets/dashboard.png
```

### Cost Forecasting

```
assets/forecast.png
```

### EC2 Cost Simulation

```
assets/simulation.png
```

### Cost Health Score

```
assets/cost-health.png
```

---

# License

This project is licensed under the **MIT License**.

---

# Author

**Sudharsan T P**

GitHub: https://github.com/sudharsantp

---

⭐ If you found this project useful, consider giving it a star.
