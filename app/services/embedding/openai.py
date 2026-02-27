import numpy as np
from typing import List
from langchain_openai import OpenAIEmbeddings
from app.services.embedding.base import BaseEmbeddingProvider
from app.core.config import settings

class OpenAIProvider(BaseEmbeddingProvider):
    def __init__(self):
        self.client = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY,
            model="text-embedding-3-small"
        )

    async def embed_query(self, text: str) -> np.ndarray:
        """Embed a single query string using OpenAI."""
        embedding = await self.client.aembed_query(text)
        return np.array(embedding)

    async def embed_documents(self, texts: List[str]) -> List[np.ndarray]:
        """Embed a list of document strings using OpenAI."""
        embeddings = await self.client.aembed_documents(texts)
        return [np.array(e) for e in embeddings]
