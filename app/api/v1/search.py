from fastapi import APIRouter
from app.schemas.response import RecommendationResponse, RecommendationItem

router = APIRouter()

@router.post("/", response_model=RecommendationResponse)
async def search(query: str):
    """Semantic search for products based on natural language."""
    # Logic to be implemented in logic phase
    return RecommendationResponse(items=[RecommendationItem(product_id="search_test_id", score=0.90)])
