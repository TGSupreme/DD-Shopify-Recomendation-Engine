from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # API Keys
    OPENAI_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    JINA_API_KEY: Optional[str] = None
    PINECONE_API_KEY: Optional[str] = None
    PINECONE_INDEX_NAME: Optional[str] = None
    
    # Embedding Configuration
    EMBEDDING_PROVIDER: str = "openai" # "openai", "gemini", or "jina"
    
    # Recommendation Weights
    WEIGHT_PURCHASED: float = 0.7
    WEIGHT_CART: float = 0.2
    WEIGHT_VIEWED: float = 0.1

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
