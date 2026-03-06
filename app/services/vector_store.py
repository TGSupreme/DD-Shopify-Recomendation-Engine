from typing import List, Dict, Any, Optional
import numpy as np
from pinecone import Pinecone
from app.core.config import settings

# Global client and index cache to avoid re-initialization
_pc_client = None
_pc_index = None

def get_index():
    global _pc_client, _pc_index
    if _pc_index is None:
        _pc_client = Pinecone(api_key=settings.PINECONE_API_KEY)
        _pc_index = _pc_client.Index(settings.PINECONE_INDEX_NAME)
    return _pc_index

async def upsert_vector(id: str, vector: np.ndarray, metadata: Dict[str, Any], namespace: str):
    """Upsert a single vector to Pinecone within a specific namespace."""
    index = get_index()
    index.upsert(
        vectors=[{"id": id, "values": vector.tolist(), "metadata": metadata}],
        namespace=namespace
    )

async def upsert_vectors(vectors_data: List[Dict[str, Any]], namespace: str):
    """Upsert multiple vectors to Pinecone within a specific namespace."""
    if not vectors_data:
        return
    index = get_index()
    index.upsert(vectors=vectors_data, namespace=namespace)

async def fetch_vectors(ids: List[str], namespace: str) -> Dict[str, np.ndarray]:
    """Fetch multiple vectors from Pinecone by their IDs within a namespace."""
    if not ids:
        return {}
    index = get_index()
    response = index.fetch(ids=ids, namespace=namespace)
    vectors = {}
    for id, data in response.get("vectors", {}).items():
        vectors[id] = np.array(data["values"])
    return vectors

async def query_nearest(vector: np.ndarray, namespace: str, top_k: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Query Pinecone for the nearest neighbor vectors within a specific namespace."""
    index = get_index()
    query_response = index.query(
        vector=vector.tolist(),
        top_k=top_k,
        include_metadata=True,
        filter=filters,
        namespace=namespace
    )
    return query_response.get("matches", [])

async def list_namespaces() -> List[str]:
    """Fetch all existing namespaces from Pinecone index stats."""
    index = get_index()
    stats = index.describe_index_stats()
    return list(stats.get("namespaces", {}).keys())

async def delete_vector(id: str, namespace: str):
    """Delete a single vector from Pinecone by its ID within a namespace."""
    index = get_index()
    index.delete(ids=[id], namespace=namespace)

async def delete_namespace(namespace: str):
    """Delete all vectors in a specific namespace."""
    index = get_index()
    index.delete(delete_all=True, namespace=namespace)

async def get_namespace_stats(namespace: str) -> Dict[str, Any]:
    """Get statistics for a specific namespace (e.g., vector count)."""
    index = get_index()
    stats = index.describe_index_stats()
    namespace_stats = stats.get("namespaces", {}).get(namespace, {"vector_count": 0})
    return namespace_stats

def verify_pinecone_connection():
    """Verify Pinecone API key and index existence on startup."""
    try:
        index = get_index()
        # This will trigger a network call to verify index existence
        index.describe_index_stats()
        return True
    except Exception as e:
        raise RuntimeError(f"Failed to connect to Pinecone: {str(e)}")
