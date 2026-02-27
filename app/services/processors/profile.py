import numpy as np
from typing import List
from app.utils.math_ops import normalize_vector
from app.core.config import settings

class ProfileProcessor:
    """Logic worker for User Interest Vector calculation using NumPy."""
    
    async def calculate_user_vector(self, purchased: List[np.ndarray], cart: List[np.ndarray], viewed: List[np.ndarray]) -> np.ndarray:
        """Calculate weighted average user vector and normalize."""
        
        # 1. Initialize empty vectors if any list is empty
        v_purchased = np.mean(purchased, axis=0) if purchased else np.zeros(0)
        v_cart = np.mean(cart, axis=0) if cart else np.zeros(0)
        v_viewed = np.mean(viewed, axis=0) if viewed else np.zeros(0)
        
        # 2. Check for dimension size (all should be the same)
        all_vecs = [v for v in [v_purchased, v_cart, v_viewed] if v.size > 0]
        if not all_vecs:
            return np.zeros(0)
        
        dim = all_vecs[0].size
        v_purchased = v_purchased if v_purchased.size > 0 else np.zeros(dim)
        v_cart = v_cart if v_cart.size > 0 else np.zeros(dim)
        v_viewed = v_viewed if v_viewed.size > 0 else np.zeros(dim)

        # 3. Apply weights
        weighted_vector = (
            v_purchased * settings.WEIGHT_PURCHASED +
            v_cart * settings.WEIGHT_CART +
            v_viewed * settings.WEIGHT_VIEWED
        )
        
        # 4. Normalize for Cosine Similarity
        return normalize_vector(weighted_vector)
