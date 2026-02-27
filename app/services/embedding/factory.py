from app.core.config import settings
from app.services.embedding.base import BaseEmbeddingProvider
from app.services.embedding.openai import OpenAIProvider
from app.services.embedding.gemini import GeminiProvider

class EmbeddingFactory:
    """Model switcher for Embedding Providers."""
    
    @staticmethod
    def get_provider() -> BaseEmbeddingProvider:
        """Fetch the embedding provider instance based on settings."""
        provider = settings.EMBEDDING_PROVIDER.lower()
        if provider == "openai":
            return OpenAIProvider()
        elif provider == "gemini":
            return GeminiProvider()
        else:
            raise ValueError(f"Unsupported embedding provider: {provider}")
