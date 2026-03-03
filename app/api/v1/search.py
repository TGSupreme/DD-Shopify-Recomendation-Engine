from fastapi import APIRouter, HTTPException
from app.schemas.response import RecommendationResponse, RecommendationItem
from app.schemas.product import SearchRequest
from app.services.embedding import embed_query
from app.services.recommender import get_similar_by_vector, NamespaceNotFoundError

router = APIRouter()

@router.post("/", response_model=RecommendationResponse)
async def search(request: SearchRequest):
    """Semantic search for products within a specific Shopify store."""
    try:
        # 1. Generate search vector
        search_vector = await embed_query(request.query)
        
        # 2. Query Pinecone for the nearest matches within the store's namespace
        items = await get_similar_by_vector(
            search_vector, 
            namespace=request.store_id, 
            top_k=request.top_k
        )
        
        return RecommendationResponse(items=items)
    except NamespaceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
