# simulation.py
from pydantic import BaseModel


class EC2SimulationRequest(BaseModel):
    instance_type: str
    region: str
    quantity: int
    hours: int


class EC2SimulationResponse(BaseModel):
    hourly_price: float
    estimated_cost: float
    currency: str