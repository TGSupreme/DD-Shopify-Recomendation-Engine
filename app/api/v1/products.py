from fastapi import APIRouter, HTTPException
from app.schemas.product import ProductFetchRequest
from app.services.mongodb import mongodb_service
from typing import List, Dict, Any

router = APIRouter()

@router.post("/fetch", response_model=List[Dict[str, Any]])
async def fetch_products(request: ProductFetchRequest):
    """Fetch product details from MongoDB by providing a list of product IDs."""
    try:
        if not request.product_ids:
            return []
            
        products = await mongodb_service.get_products_by_ids(request.product_ids)
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch products: {str(e)}")
