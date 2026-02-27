from fastapi import APIRouter, Depends, HTTPException
from app.schemas.product import Product
from app.schemas.response import SyncResponse
from app.utils.formatter import format_product_context
from app.api.deps import get_embedding_provider, get_vector_store
from app.services.embedding.base import BaseEmbeddingProvider
from app.services.vector_store.client import VectorStoreClient

router = APIRouter()

@router.post("/", response_model=SyncResponse)
async def sync_product(
    product: Product,
    embedding_provider: BaseEmbeddingProvider = Depends(get_embedding_provider),
    vector_store: VectorStoreClient = Depends(get_vector_store)
):
    """Keep Pinecone in sync with Shopify/MongoDB."""
    try:
        # 1. Format the text for embedding
        content_string = format_product_context(product)
        
        # 2. Generate embedding vector
        vector = await embedding_provider.embed_query(content_string)
        
        # 3. Prepare Metadata
        metadata = {
            "title": product.title,
            "price": product.price,
            "category": product.category,
            "availability": product.availability,
            "gender": product.gender,
            **product.extra_metadata
        }
        
        # 4. Upsert to Pinecone
        await vector_store.upsert_vector(product.id, vector, metadata)
        
        return SyncResponse(message=f"Product {product.id} synced successfully", upserted_count=1)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
