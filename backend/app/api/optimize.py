from fastapi import APIRouter

from app.services.recommendation_engine import engine

router = APIRouter()


@router.get("/")
def get_recommendations():
    return engine.generate_recommendations()