from fastapi import APIRouter, HTTPException
from app.schemas.history import UserHistory
from app.schemas.response import RecommendationResponse
from app.services.recommender import (
    get_user_recommendations, 
    get_item_recommendations,
    NamespaceNotFoundError,
    ProductNotFoundError
)

router = APIRouter()

@router.post("/user", response_model=RecommendationResponse)
async def recommend_for_user(history: UserHistory):
    """Generate 'For You' personalized recommendations."""
    try:
        items = await get_user_recommendations(history)
        return RecommendationResponse(items=items)
    except NamespaceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/similar/{product_id}", response_model=RecommendationResponse)
async def recommend_similar(product_id: str, store_id: str):
    """Find 'Related Items' for a product page within a specific store."""
    try:
        items = await get_item_recommendations(product_id, store_id=store_id)
        return RecommendationResponse(items=items)
    except (NamespaceNotFoundError, ProductNotFoundError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
