from typing import List
from fastapi import APIRouter, HTTPException
from app.schemas.product import Product, BatchSyncRequest
from app.schemas.response import SyncResponse
from app.utils.formatter import format_product_context
from app.services.embedding import embed_query, embed_documents
from app.services.vector_store import upsert_vector, upsert_vectors

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
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/bulk", response_model=SyncResponse)
async def sync_products_bulk(request: BatchSyncRequest):
    """Perform bulk syncing of multiple products within a single Shopify store namespace."""
    try:
        if not request.products:
            return SyncResponse(message="No products provided", upserted_count=0)

        # 1. Format all product context strings for batch embedding
        content_strings = [format_product_context(p) for p in request.products]
        print("Product context formatting completed")

        # 2. Generate embeddings in a single batch call
        vectors = await embed_documents(content_strings)
        print("Embeddings generated")

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
        print("Vectors prepared for Pinecone")

        # 4. Upsert everything to Pinecone
        await upsert_vectors(vectors_to_upsert, namespace=request.store_id)
        print("Vectors successfully upserted to Pinecone")
        
        return SyncResponse(
            message=f"Successfully synced {len(request.products)} products for store {request.store_id}",
            upserted_count=len(request.products)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
