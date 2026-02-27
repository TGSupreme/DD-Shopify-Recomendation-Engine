from typing import List, Optional
import numpy as np
from app.services.recommender.base import RecommenderStrategy
from app.schemas.response import RecommendationItem
from app.services.vector_store.client import VectorStoreClient

class ItemRecommender(RecommenderStrategy):
    """Similarity logic (Related products) for finding nearest neighbors."""
    
    def __init__(self):
        self.vector_store = VectorStoreClient()

    async def get_recommendations(self, product_id: str, top_k: int = 10) -> List[RecommendationItem]:
        """Find the nearest neighbors in Pinecone based on the product's vector."""
        # 1. Fetch the product's existing vector
        vectors = await self.vector_store.fetch_vectors([product_id])
        if not vectors or product_id not in vectors:
            return []
        
        # 2. Query Pinecone for similar products
        matches = await self.vector_store.query_nearest(vectors[product_id], top_k=top_k)
        
        # 3. Transform results into the standard response format
        return [RecommendationItem(product_id=m["id"], score=m["score"]) for m in matches]
        
    async def get_similar_by_vector(self, vector: np.ndarray, top_k: int = 10) -> List[RecommendationItem]:
        """Find the nearest neighbors based on a raw vector."""
        matches = await self.vector_store.query_nearest(vector, top_k=top_k)
        return [RecommendationItem(product_id=m["id"], score=m["score"]) for m in matches]
