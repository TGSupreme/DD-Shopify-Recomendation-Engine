from fastapi import APIRouter, Depends
from app.schemas.product import Product
from app.schemas.response import SyncResponse

router = APIRouter()

@router.post("/sync", response_model=SyncResponse)
async def sync_product(product: Product):
    """Keep Pinecone in sync with Shopify/MongoDB."""
    # Logic to be implemented in logic phase
    return SyncResponse(message="Product synced successfully", upserted_count=1)
