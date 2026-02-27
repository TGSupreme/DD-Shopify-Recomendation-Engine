from typing import List, Dict, Any
import numpy as np
from app.services.recommender.base import RecommenderStrategy
from app.schemas.response import RecommendationItem
from app.services.embedding.factory import EmbeddingFactory
from app.services.vector_store.client import VectorStoreClient
from app.services.processors.profile import ProfileProcessor
from app.schemas.history import UserHistory

class UserRecommender(RecommenderStrategy):
    """Personalization logic (Weighted Averaging) for specific users."""
    
    def __init__(self):
        self.embedding_provider = EmbeddingFactory.get_provider()
        self.vector_store = VectorStoreClient()
        self.processor = ProfileProcessor()

    async def get_recommendations(self, history: UserHistory, top_k: int = 10) -> List[RecommendationItem]:
        """Generate 'For You' personalized recommendations based on user history."""
        # 1. Fetch vectors for all products in the history
        all_ids = history.purchased + history.add_to_cart + history.viewed
        existing_vectors = await self.vector_store.fetch_vectors(all_ids)
        
        # 2. Extract specific vectors for each category
        purchased_vecs = [existing_vectors[id] for id in history.purchased if id in existing_vectors]
        cart_vecs = [existing_vectors[id] for id in history.add_to_cart if id in existing_vectors]
        viewed_vecs = [existing_vectors[id] for id in history.viewed if id in existing_vectors]
        
        # 3. Calculate the User Interest Vector
        user_vector = await self.processor.calculate_user_vector(purchased_vecs, cart_vecs, viewed_vecs)
        
        if user_vector.size == 0:
            return []

        # 4. Query Pinecone for the Top N matches
        matches = await self.vector_store.query_nearest(user_vector, top_k=top_k)
        
        # 5. Transform results into the standard response format
        return [RecommendationItem(product_id=m["id"], score=m["score"]) for m in matches]
