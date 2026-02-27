from abc import ABC, abstractmethod
from typing import List
import numpy as np

class BaseEmbeddingProvider(ABC):
    @abstractmethod
    async def embed_query(self, text: str) -> np.ndarray:
        """Embed a single query string."""
        pass

    @abstractmethod
    async def embed_documents(self, texts: List[str]) -> List[np.ndarray]:
        """Embed a list of document strings."""
        pass
