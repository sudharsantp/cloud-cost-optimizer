from fastapi import APIRouter

from app.schemas.simulation import (
    EC2SimulationRequest,
    EC2SimulationResponse
)

from app.services.aws_pricing import (
    get_ec2_hourly_price
)

router = APIRouter()


@router.post(
    "/ec2",
    response_model=EC2SimulationResponse
)
def simulate_ec2(
    request: EC2SimulationRequest
):

    hourly_price = get_ec2_hourly_price(
        request.instance_type,
        request.region
    )

    if hourly_price is None:
        return {
            "hourly_price": 0,
            "estimated_cost": 0,
            "currency": "USD"
        }

    estimated_cost = (
        hourly_price
        * request.quantity
        * request.hours
    )

    return {
        "hourly_price": hourly_price,
        "estimated_cost": round(
            estimated_cost,
            2
        ),
        "currency": "USD"
    }