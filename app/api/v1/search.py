from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas.response import RecommendationResponse, RecommendationItem
from app.api.deps import get_embedding_provider, get_vector_store
from app.services.embedding.base import BaseEmbeddingProvider
from app.services.vector_store.client import VectorStoreClient

router = APIRouter()

@router.post("/", response_model=RecommendationResponse)
async def search(
    query: str = Query(..., description="The natural language search query"),
    embedding_provider: BaseEmbeddingProvider = Depends(get_embedding_provider),
    vector_store: VectorStoreClient = Depends(get_vector_store)
):
    """Semantic search for products based on natural language."""
    try:
        # 1. Generate search vector
        search_vector = await embedding_provider.embed_query(query)
        
        # 2. Query Pinecone for the nearest matches
        matches = await vector_store.query_nearest(search_vector, top_k=10)
        
        # 3. Transform into RecommendationItem objects
        items = [RecommendationItem(product_id=m["id"], score=m["score"]) for m in matches]
        
        return RecommendationResponse(items=items)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
