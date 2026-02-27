from pydantic import BaseModel
from typing import List, Optional, Any

class RecommendationItem(BaseModel):
    product_id: str
    score: float

class RecommendationResponse(BaseModel):
    items: List[RecommendationItem]
    message: Optional[str] = None
    status: str = "success"

class SyncResponse(BaseModel):
    status: str = "success"
    message: Optional[str] = None
    upserted_count: int = 0
