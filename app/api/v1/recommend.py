from fastapi import APIRouter, Depends, HTTPException
from app.schemas.history import UserHistory
from app.schemas.response import RecommendationResponse
from app.api.deps import get_user_recommender, get_item_recommender
from app.services.recommender.user import UserRecommender
from app.services.recommender.item import ItemRecommender

router = APIRouter()

@router.post("/user", response_model=RecommendationResponse)
async def recommend_for_user(
    history: UserHistory,
    user_recommender: UserRecommender = Depends(get_user_recommender)
):
    """Generate 'For You' personalized recommendations."""
    try:
        items = await user_recommender.get_recommendations(history)
        return RecommendationResponse(items=items)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/similar/{product_id}", response_model=RecommendationResponse)
async def recommend_similar(
    product_id: str,
    item_recommender: ItemRecommender = Depends(get_item_recommender)
):
    """Find 'Related Items' for a product page."""
    try:
        items = await item_recommender.get_recommendations(product_id)
        return RecommendationResponse(items=items)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
