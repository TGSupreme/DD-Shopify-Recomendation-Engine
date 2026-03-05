from typing import List, Dict, Any
import numpy as np

from app.schemas.response import RecommendationItem
from app.schemas.history import UserHistory
from app.services.embedding import embed_query
from app.services.vector_store import fetch_vectors, query_nearest, list_namespaces
from app.utils.math_ops import normalize_vector
from app.core.config import settings

class NamespaceNotFoundError(Exception):
    """Raised when a specific Pinecone namespace (store_id) does not exist."""
    pass

class ProductNotFoundError(Exception):
    """Raised when a specific product_id is not found in the namespace."""
    pass

async def calculate_user_vector(purchased: List[np.ndarray], cart: List[np.ndarray], viewed: List[np.ndarray]) -> np.ndarray:
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

async def get_user_recommendations(history: UserHistory, top_k: int = settings.TOP_K) -> List[RecommendationItem]:
    """Generate 'For You' personalized recommendations based on user history."""
    # 1. Verify store exists
    namespaces = await list_namespaces()
    if history.store_id not in namespaces:
        raise NamespaceNotFoundError(f"Store '{history.store_id}' not found.")

    # 2. Fetch vectors for all products in the history
    all_ids = history.purchased + history.add_to_cart + history.viewed
    existing_vectors = await fetch_vectors(all_ids, namespace=history.store_id)
    
    # 3. Extract specific vectors for each category
    purchased_vecs = [existing_vectors[id] for id in history.purchased if id in existing_vectors]
    cart_vecs = [existing_vectors[id] for id in history.add_to_cart if id in existing_vectors]
    viewed_vecs = [existing_vectors[id] for id in history.viewed if id in existing_vectors]
    
    # 4. Calculate the User Interest Vector
    user_vector = await calculate_user_vector(purchased_vecs, cart_vecs, viewed_vecs)
    
    if user_vector.size == 0:
        return []

    # 5. Query Pinecone for the Top N matches
    matches = await query_nearest(user_vector, namespace=history.store_id, top_k=top_k)
    
    # 6. Transform results into the standard response format
    return [RecommendationItem(product_id=m["id"], score=m["score"]) for m in matches]

async def get_item_recommendations(product_id: str, store_id: str, top_k: int = settings.TOP_K) -> List[RecommendationItem]:
    """Find the nearest neighbors in Pinecone based on the product's vector."""
    # 1. Verify store exists
    namespaces = await list_namespaces()
    if store_id not in namespaces:
        raise NamespaceNotFoundError(f"Store '{store_id}' not found.")

    # 2. Fetch the product's existing vector
    vectors = await fetch_vectors([product_id], namespace=store_id)
    if not vectors or product_id not in vectors:
        raise ProductNotFoundError(f"Product '{product_id}' not found in store '{store_id}'.")
    
    # 3. Query Pinecone for similar products
    matches = await query_nearest(vectors[product_id], namespace=store_id, top_k=top_k)
    
    # 4. Transform results into the standard response format
    return [RecommendationItem(product_id=m["id"], score=m["score"]) for m in matches]

async def get_similar_by_vector(vector: np.ndarray, namespace: str, top_k: int = settings.TOP_K) -> List[RecommendationItem]:
    """Find the nearest neighbors based on a raw vector."""
    # 1. Verify store exists
    namespaces = await list_namespaces()
    if namespace not in namespaces:
        raise NamespaceNotFoundError(f"Store '{namespace}' not found.")

    matches = await query_nearest(vector, namespace=namespace, top_k=top_k)
    return [RecommendationItem(product_id=m["id"], score=m["score"]) for m in matches]
