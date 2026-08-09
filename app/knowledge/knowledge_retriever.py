from typing import List, Dict

from app.embedding.embedding_service import EmbeddingService
from app.vector.vector_service import VectorService


class KnowledgeRetriever:

    DEFAULT_COLLECTIONS = ["knowledge_embeddings"]

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_service = VectorService()

    def retrieve(self, query: str, top_k: int = 5, collections: List[str] | None = None) -> List[Dict]:
        collections = collections or self.DEFAULT_COLLECTIONS

        result = self.embedding_service.embed([query])[0]

        combined: List[Dict] = []
        for coll in collections:
            hits = self.vector_service.search(coll, result.vector, top_k)
            if not hits:
                continue
            for hit in hits:
                payload = getattr(hit, "payload", {})
                score = getattr(hit, "score", None)
                combined.append({
                    "id": getattr(hit, "id", None),
                    "collection": coll,
                    "payload": payload,
                    "score": score,
                    "text": payload.get("text") if isinstance(payload, dict) else None,
                })

        # sort combined by score desc and return top_k
        combined_sorted = sorted([c for c in combined if c.get("score") is not None], key=lambda x: x["score"], reverse=True)
        return combined_sorted[:top_k]
