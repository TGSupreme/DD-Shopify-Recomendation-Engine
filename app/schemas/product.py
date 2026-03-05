from pydantic import BaseModel
from typing import List, Optional

class ProductOption(BaseModel):
    name: str
    values: List[str]

class Product(BaseModel):

    id: str
    store_id: str
    title: str
    product_type: Optional[str] = None
    vendor: str
    tags: List[str] = []
    options: List[ProductOption] = []
    price: float

class SearchRequest(BaseModel):
    query: str
    store_id: str
    top_k: int = 10

class BatchSyncRequest(BaseModel):
    store_id: str
    products: List[Product]
