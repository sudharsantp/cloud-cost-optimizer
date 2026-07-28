from app.services.health_score import CostHealthScore

health = CostHealthScore(
    forecast_cost=7500,
    budget=8000,
    idle_resources=2,
    anomaly_count=1,
    estimated_savings=350,
    utilization=72
)

result = health.calculate()

print(result)