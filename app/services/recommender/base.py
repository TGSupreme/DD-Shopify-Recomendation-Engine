from abc import ABC, abstractmethod
from typing import List, Dict, Any
from app.schemas.response import RecommendationItem

class RecommenderStrategy(ABC):
    @abstractmethod
    async def get_recommendations(self, data: Any, top_k: int = 10) -> List[RecommendationItem]:
        """Fetch recommendations based on the provided strategy."""
        pass
