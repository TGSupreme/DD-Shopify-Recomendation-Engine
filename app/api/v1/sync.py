from typing import List
import logging
from fastapi import APIRouter, HTTPException, Query
from app.schemas.product import Product, BatchSyncRequest
from app.schemas.response import SyncResponse, DeleteResponse
from app.utils.formatter import format_product_context
from app.services.embedding import embed_query, embed_documents
from app.services.vector_store import (
    upsert_vector, 
    upsert_vectors, 
    delete_vector, 
    delete_namespace, 
    get_namespace_stats
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=SyncResponse)
async def sync_product(product: Product):
    """Keep Pinecone in sync with Shopify/MongoDB (Single Product)."""
    try:
        # 1. Format the text for embedding
        content_string = format_product_context(product)
        
        # 2. Generate embedding vector
        vector = await embed_query(content_string)
        
        # 3. Prepare Metadata
        metadata = {
            "title": product.title,
            "price": product.price,
            "product_type": product.product_type,
            "vendor": product.vendor,
            "tags": product.tags,
            # Flatten options for metadata if needed for filtering
            "options": [f"{opt.name}: {', '.join(opt.values)}" for opt in product.options]
        }
        
        # 4. Upsert to Pinecone
        await upsert_vector(product.id, vector, metadata, namespace=product.store_id)
        
        return SyncResponse(message=f"Product {product.id} synced successfully for store {product.store_id}", upserted_count=1)
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/bulk", response_model=SyncResponse)
async def sync_products_bulk(request: BatchSyncRequest):
    """Perform bulk syncing of multiple products within a single Shopify store namespace."""
    try:
        if not request.products:
            return SyncResponse(message="No products provided", upserted_count=0)

        # 1. Format all product context strings for batch embedding
        content_strings = [format_product_context(p) for p in request.products]
        logger.info("Product context formatting completed")

        # 2. Generate embeddings in a single batch call
        vectors = await embed_documents(content_strings)
        logger.info("Embeddings generated")

        # 3. Prepare list of Pinecone-format vectors with metadata
        vectors_to_upsert = []
        for i, product in enumerate(request.products):
            metadata = {
                "title": product.title,
                "price": product.price,
                "product_type": product.product_type,
                "vendor": product.vendor,
                "tags": product.tags,
                "options": [f"{opt.name}: {', '.join(opt.values)}" for opt in product.options]
            }
            vectors_to_upsert.append({
                "id": product.id,
                "values": vectors[i].tolist(),
                "metadata": metadata
            } )
        logger.info("Vectors prepared for Pinecone")

        # 4. Upsert everything to Pinecone Upsert in batches of 100
        batch_size = 100
        total_upserted = 0

        for i in range(0, len(vectors_to_upsert), batch_size):
            batch = vectors_to_upsert[i:i + batch_size]
            await upsert_vectors(batch, namespace=request.store_id)
            total_upserted += len(batch)
            logger.info(f"{total_upserted} Vectors successfully upserted to Pinecone")
            print("hello")
        
        return SyncResponse(
            message=f"Successfully synced {total_upserted} products for store {request.store_id}",  
            upserted_count=total_upserted
        )
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{product_id}", response_model=DeleteResponse)
async def delete_product(product_id: str, store_id: str = Query(...)):
    """Delete a single product's vector from a store's namespace."""
    try:
        await delete_vector(product_id, namespace=store_id)
        return DeleteResponse(
            message=f"Product {product_id} deleted successfully from store {store_id}",
            status="success",
            delete_count= 1
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/store/{store_id}", response_model=DeleteResponse)
async def delete_store(store_id: str):
    """Delete all vectors in a store's namespace (wipe store data)."""
    try:
        stats = await get_namespace_stats(namespace=store_id)
        deleted_count = stats.get("vector_count", 0)

        await delete_namespace(namespace=store_id)
        return DeleteResponse(
            message=f"All data for store {store_id} has been deleted",
            status="success",
            delete_count= deleted_count
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{store_id}")
async def get_sync_status(store_id: str):
    """Get the current synchronization status (vector count) for a store."""
    try:
        stats = await get_namespace_stats(namespace=store_id)
        return {
            "store_id": store_id,
            "vector_count": stats.get("vector_count", 0),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
