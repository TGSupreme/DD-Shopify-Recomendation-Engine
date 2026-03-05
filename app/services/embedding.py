from typing import List
import numpy as np
from app.core.config import settings

# Global client cache to avoid re-initialization
_embedding_client = None

def get_embedding_client():
    global _embedding_client
    if _embedding_client is None:
        provider = settings.EMBEDDING_PROVIDER.lower()
        if provider == "openai":
            from langchain_openai import OpenAIEmbeddings
            _embedding_client = OpenAIEmbeddings(
                openai_api_key=settings.OPENAI_API_KEY,
                model="text-embedding-3-small"
            )
        elif provider == "gemini":
            from langchain_google_genai import GoogleGenerativeAIEmbeddings
            _embedding_client = GoogleGenerativeAIEmbeddings(
                google_api_key=settings.GOOGLE_API_KEY,
                model="models/gemini-embedding-001"
            )
        else:
            raise ValueError(f"Unsupported embedding provider: {provider}")
    return _embedding_client

class EmbeddingServiceError(Exception):
    """Raised when the embedding provider fails due to auth, quota, or network issues."""
    pass

async def embed_query(text: str) -> np.ndarray:
    """Embed a single query string."""
    try:
        client = get_embedding_client()
        embedding = await client.aembed_query(text)
        return np.array(embedding)
    except Exception as e:
        raise EmbeddingServiceError(f"Embedding service failed: {str(e)}")

async def embed_documents(texts: List[str]) -> List[np.ndarray]:
    """Embed a list of document strings."""
    try:
        client = get_embedding_client()
        embeddings = await client.aembed_documents(texts)
        return [np.array(e) for e in embeddings]
    except Exception as e:
        raise EmbeddingServiceError(f"Bulk embedding service failed: {str(e)}")
