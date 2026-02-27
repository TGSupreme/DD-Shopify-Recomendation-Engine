import numpy as np
from typing import List
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.services.embedding.base import BaseEmbeddingProvider
from app.core.config import settings

class GeminiProvider(BaseEmbeddingProvider):
    def __init__(self):
        self.client = GoogleGenerativeAIEmbeddings(
            google_api_key=settings.GOOGLE_API_KEY,
            model="models/embedding-001"
        )

    async def embed_query(self, text: str) -> np.ndarray:
        """Embed a single query string using Google Gemini."""
        embedding = await self.client.aembed_query(text)
        return np.array(embedding)

    async def embed_documents(self, texts: List[str]) -> List[np.ndarray]:
        """Embed a list of document strings using Google Gemini."""
        embeddings = await self.client.aembed_documents(texts)
        return [np.array(e) for e in embeddings]
