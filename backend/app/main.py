from fastapi import FastAPI
from app.api import cost, budget, anomaly, optimize, sync, analytics, prediction,simulation
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="CloudWatch Billing Sentinel",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(cost.router, prefix="/cost", tags=["Cost"])
app.include_router(budget.router, prefix="/budget", tags=["Budget"])
app.include_router(anomaly.router, prefix="/anomaly", tags=["Anomaly"])
app.include_router(optimize.router, prefix="/optimize", tags=["Optimization"])
app.include_router(sync.router, prefix="/sync", tags=["AWS Sync"])
app.include_router(
    analytics.router,
    prefix="/analytics",
    tags=["Analytics"]
)

app.include_router(
    prediction.router,
    prefix="/prediction",
    tags=["Prediction"]
)

app.include_router(
    simulation.router,
    prefix="/simulation",
    tags=["Simulation"]
)


@app.get("/")
def root():
    return {
        "project": "CloudWatch Billing Sentinel",
        "version": "1.0.0",
        "status": "Running"
    }