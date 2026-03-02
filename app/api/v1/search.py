from fastapi import APIRouter, HTTPException
from app.schemas.response import RecommendationResponse, RecommendationItem
from app.schemas.product import SearchRequest
from app.services.embedding import embed_query
from app.services.vector_store import query_nearest

router = APIRouter()

@router.post("/", response_model=RecommendationResponse)
async def search(request: SearchRequest):
    """Semantic search for products within a specific Shopify store."""
    try:
        # 1. Generate search vector
        search_vector = await embed_query(request.query)
        
        # 2. Query Pinecone for the nearest matches within the store's namespace
        matches = await query_nearest(
            search_vector, 
            namespace=request.store_id, 
            top_k=request.top_k
        )
        
        # 3. Transform into RecommendationItem objects
        items = [RecommendationItem(product_id=m["id"], score=m["score"]) for m in matches]
        
        return RecommendationResponse(items=items)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
