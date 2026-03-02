from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class Product(BaseModel):
    id: str
    store_id: str
    title: str
    color: Optional[str] = None
    material: Optional[str] = None
    tags: List[str] = []
    price: Optional[float] = None
    category: Optional[str] = None
    availability: Optional[bool] = None
    gender: Optional[str] = None
    extra_metadata: Dict[str, Any] = Field(default_factory=dict)

class SearchRequest(BaseModel):
    query: str
    store_id: str
    top_k: int = 10

class BatchSyncRequest(BaseModel):
    store_id: str
    products: List[Product]
