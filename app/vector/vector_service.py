from typing import Any

from app.vector.qdrant_client import QdrantClient
from app.vector.collection_manager import CollectionManager


class VectorService:

    def __init__(self):
        self.client = QdrantClient()
        self.collection_manager = CollectionManager(self.client)

    def store(self, collection_name: str, point_id: str, vector: list[float], payload: dict[str, Any] | None = None):
        self.collection_manager.ensure_collection(collection_name, vector_size=len(vector))
        return self.client.upsert(collection_name, point_id, vector, payload)

    def search(self, collection_name: str, vector: list[float], limit: int = 5):
        self.collection_manager.ensure_collection(collection_name, vector_size=len(vector))
        return self.client.search(collection_name, vector, limit)

    def delete(self, collection_name: str, point_id: str):
        return self.client.delete(collection_name, point_id)

    def update(self, collection_name: str, point_id: str, vector: list[float], payload: dict[str, Any] | None = None):
        self.collection_manager.ensure_collection(collection_name, vector_size=len(vector))
        return self.client.upsert(collection_name, point_id, vector, payload)
