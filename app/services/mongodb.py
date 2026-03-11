from pymongo import MongoClient
from app.core.config import settings
from typing import List, Dict, Any
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

class MongoDBService:
    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBService, cls).__new__(cls)
            if settings.MONGODB_URI:
                try:
                    cls._client = MongoClient(settings.MONGODB_URI)
                    logger.info("MongoDB client initialized successfully.")
                except Exception as e:
                    logger.error(f"Failed to initialize MongoDB client: {str(e)}")
            else:
                logger.warning("MONGODB_URI not found in configuration.")
        return cls._instance

    @property
    def db(self):
        if self._client is not None:
            return self._client[settings.MONGODB_DB_NAME]
        return None

    @property
    def collection(self):
        if self.db is not None:
            return self.db[settings.MONGODB_COLLECTION]
        return None

    async def get_products_by_ids(self, product_ids: List[str]) -> List[Dict[str, Any]]:
        """Fetch multiple products from MongoDB by their IDs."""
        if self.collection is None:
            logger.error("MongoDB collection not initialized.")
            return []

        try:
            # Query by 'id' field and exclude '_id' from results
            query = {"id": {"$in": product_ids}}
            projection = {"_id": 0}
            cursor = self.collection.find(query, projection)
            
            products = list(cursor)
            return products
        except Exception as e:
            logger.error(f"Error fetching products from MongoDB: {str(e)}")
            return []

mongodb_service = MongoDBService()
