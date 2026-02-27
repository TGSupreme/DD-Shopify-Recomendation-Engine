from app.services.embedding.factory import EmbeddingFactory
from app.services.vector_store.client import VectorStoreClient
from app.services.recommender.user import UserRecommender
from app.services.recommender.item import ItemRecommender

def get_vector_store():
    return VectorStoreClient()

def get_embedding_provider():
    return EmbeddingFactory.get_provider()

def get_user_recommender():
    return UserRecommender()

def get_item_recommender():
    return ItemRecommender()
