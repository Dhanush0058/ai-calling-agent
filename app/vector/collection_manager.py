from qdrant_client.http import models as rest


class CollectionManager:

    def __init__(self, client):
        self.client = client

    @staticmethod
    def _extract_vector_size(existing_collection):
        try:
            config = getattr(existing_collection, "config", None)
            params = getattr(config, "params", None)
            vectors = getattr(params, "vectors", None)
            if hasattr(vectors, "size"):
                return int(vectors.size)
            if isinstance(vectors, dict):
                return int(vectors.get("size") or vectors.get("params", {}).get("size"))
            if hasattr(vectors, "params"):
                nested = getattr(vectors, "params", None)
                if hasattr(nested, "size"):
                    return int(nested.size)
        except Exception:
            pass
        return None

    def ensure_collection(self, collection_name: str, vector_size: int):
        try:
            existing = self.client.client.get_collection(collection_name)
        except Exception:
            existing = None

        existing_size = self._extract_vector_size(existing)
        if existing is not None and existing_size is not None and existing_size != vector_size:
            try:
                self.client.client.delete_collection(collection_name)
            except Exception:
                pass
            existing = None

        if existing is None:
            try:
                self.client.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=rest.VectorParams(size=vector_size, distance=rest.Distance.COSINE),
                )
            except Exception:
                # Gracefully ignore if Qdrant is unavailable during tests or local startup.
                return
