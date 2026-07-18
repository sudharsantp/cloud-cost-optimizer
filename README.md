# AWS CloudWatch Cost Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![React](https://img.shields.io/badge/React-Frontend-61DAFB)
![AWS](https://img.shields.io/badge/AWS-Cloud-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Overview

AWS CloudWatch Cost Intelligence Platform is an AI-powered cloud cost monitoring and forecasting system that helps users analyze historical AWS spending, predict future costs, and estimate infrastructure expenses before deployment.

The platform integrates AWS CloudWatch, AWS Cost Explorer, and AWS Pricing APIs to provide real-time cost analytics, machine learning-based forecasting, and deployment cost simulation through an interactive dashboard.

---

## Features

### Cost Analytics

- Real-time AWS billing dashboard
- Daily cost analysis
- Service-wise cost breakdown
- Historical spending visualization

### AI Cost Forecasting

- Prophet-based forecasting
- ARIMA-based forecasting
- 30-day AWS cost prediction
- Forecast comparison
- Prediction summary

### CloudWatch Monitoring

- CloudWatch metric integration
- Resource utilization monitoring
- Historical metric analysis

### EC2 Cost Simulation

Estimate deployment cost before launching an EC2 instance.

Simulation parameters include:

- AWS Region
- Instance Type
- Operating System
- Storage
- Usage Hours

### Interactive Dashboard

- Cost trend visualization
- Forecast graphs
- Service distribution charts
- Simulation results

---

## Technology Stack

### Frontend

- React
- Vite
- Axios
- Chart.js

### Backend

- FastAPI
- SQLAlchemy
- SQLite
- Pandas
- NumPy

### Machine Learning

- Prophet
- ARIMA (Statsmodels)

### AWS Services

- AWS CloudWatch
- AWS Cost Explorer API
- AWS Pricing API
- Boto3

---

## Project Architecture

```
React Dashboard
        │
        ▼
FastAPI Backend
        │
 ┌──────────────┐
 │ Analytics    │
 │ Prediction   │
 │ Simulation   │
 └──────────────┘
        │
        ▼
AWS CloudWatch
AWS Cost Explorer
AWS Pricing API
        │
        ▼
SQLite Database
        │
        ▼
Prophet & ARIMA Models
```

---

## API Endpoints

### Analytics

- GET /analytics/daily-cost
- GET /analytics/service-breakdown

### Prediction

- GET /prediction/arima
- GET /prediction/summary
- GET /prediction/compare
- GET /prediction/next-30-days

### Simulation

- POST /simulation/ec2

---

## Installation

### Clone Repository

```bash
git clone https://github.com/sudharsantp/cloud-cost-optimizer.git
cd cloud-cost-optimizer
```

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env`

```
AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY
AWS_REGION=ap-south-1
```

Run backend

```bash
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Future Enhancements

- Cost anomaly detection
- Budget alerts
- Email notifications
- PDF and CSV report generation
- Multi-cloud support (Azure & GCP)
- Docker deployment

---

## License

MIT License

---

## Author

**Sudharsan T P**

GitHub: https://github.com/sudharsantp
