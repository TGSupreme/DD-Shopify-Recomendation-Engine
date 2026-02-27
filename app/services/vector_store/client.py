import numpy as np
from typing import List, Dict, Any, Optional
from pinecone import Pinecone
from app.core.config import settings

class VectorStoreClient:
    """Pinecone Integration for Vector CRUD operations."""
    
    def __init__(self):
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.index = self.pc.Index(settings.PINECONE_INDEX_NAME)

    async def upsert_vector(self, id: str, vector: np.ndarray, metadata: Dict[str, Any]):
        """Upsert a single vector to Pinecone."""
        self.index.upsert(vectors=[{"id": id, "values": vector.tolist(), "metadata": metadata}])

    async def fetch_vectors(self, ids: List[str]) -> Dict[str, np.ndarray]:
        """Fetch multiple vectors from Pinecone by their IDs."""
        if not ids:
            return {}
        response = self.index.fetch(ids=ids)
        vectors = {}
        for id, data in response.get("vectors", {}).items():
            vectors[id] = np.array(data["values"])
        return vectors

    async def query_nearest(self, vector: np.ndarray, top_k: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Query Pinecone for the nearest neighbor vectors."""
        query_response = self.index.query(
            vector=vector.tolist(),
            top_k=top_k,
            include_metadata=True,
            filter=filters
        )
        return query_response.get("matches", [])
