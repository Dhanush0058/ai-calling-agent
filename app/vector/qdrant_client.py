import uuid

from qdrant_client import QdrantClient as QdrantPyClient
from qdrant_client.http import models as rest

from app.core.config import settings


class QdrantClient:

    def __init__(self):
        if not settings.QDRANT_URL:
            self.client = None
            return

        qdrant_kwargs = {
            "url": settings.QDRANT_URL,
            "check_compatibility": False,
        }
        if settings.QDRANT_API_KEY:
            qdrant_kwargs["api_key"] = settings.QDRANT_API_KEY

        self.client = QdrantPyClient(**qdrant_kwargs)

    def _is_available(self) -> bool:
        if self.client is None:
            return False
        try:
            self.client.get_collections()
            return True
        except Exception:
            return False

    def _normalize_point_id(self, point_id: str):
        if isinstance(point_id, int):
            return point_id

        candidate = str(point_id)
        try:
            return uuid.UUID(candidate)
        except ValueError:
            return uuid.uuid5(uuid.NAMESPACE_DNS, candidate)

    def _ensure_collection(self, collection_name: str, vector_size: int):
        try:
            existing = self.client.get_collection(collection_name)
            config = getattr(existing, "config", None)
            params = getattr(config, "params", None)
            vectors = getattr(params, "vectors", None)
            size = None
            if hasattr(vectors, "size"):
                size = int(vectors.size)
            elif isinstance(vectors, dict):
                size = int(vectors.get("size") or vectors.get("params", {}).get("size"))
            if size is not None and size != vector_size:
                try:
                    self.client.delete_collection(collection_name)
                except Exception:
                    pass
            else:
                return
        except Exception:
            pass

        try:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=rest.VectorParams(size=vector_size, distance=rest.Distance.COSINE),
            )
        except Exception:
            pass

    def upsert(self, collection_name: str, point_id: str, vector: list[float], payload: dict | None = None):
        if not self._is_available():
            return str(point_id)

        self._ensure_collection(collection_name, len(vector))
        normalized_id = self._normalize_point_id(point_id)
        point = rest.PointStruct(id=normalized_id, vector=vector, payload=payload or {})
        self.client.upsert(collection_name=collection_name, points=[point])
        return str(normalized_id)

    def search(self, collection_name: str, vector: list[float], limit: int = 5):
        if not self._is_available():
            return []

        response = self.client.query_points(
            collection_name=collection_name,
            query=vector,
            limit=limit,
            with_payload=True,
        )
        return getattr(response, "points", [])

    def delete(self, collection_name: str, point_id: str):
        if not self._is_available():
            return str(point_id)

        normalized_id = self._normalize_point_id(point_id)
        self.client.delete(collection_name=collection_name, ids=[normalized_id])
        return str(normalized_id)
