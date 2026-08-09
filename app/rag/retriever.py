from typing import List

from sqlalchemy.orm import Session

from app.core.config import settings
from app.embedding.embedding_service import EmbeddingService
from app.tools.call_tools import CallTools
from app.vector.vector_service import VectorService
from app.models.call import Call


class Retriever:

    def __init__(self, db: Session):
        self.db = db
        self.vector_service = VectorService()
        self.embedding_service = EmbeddingService()

    def _normalize_score(self, raw_score: float | None) -> float:
        if raw_score is None:
            return 0.0
        # Simple min-max normalization across the current batch of hits.
        return max(0.0, min(1.0, float(raw_score)))

    def retrieve(self, question: str, top_k: int = 5) -> List[Call]:
        result = self.embedding_service.embed([question])[0]

        collections = settings.QDRANT_COLLECTIONS or [settings.QDRANT_COLLECTION]
        merged_hits: list[dict] = []

        for collection_name in collections:
            hits = self.vector_service.search(collection_name, result.vector, top_k)
            for hit in hits:
                payload = getattr(hit, "payload", {})
                if isinstance(payload, dict):
                    call_id = payload.get("call_id")
                    if call_id is None:
                        continue
                    try:
                        call_id_int = int(call_id)
                    except ValueError:
                        continue
                    merged_hits.append(
                        {
                            "call_id": call_id_int,
                            "score": self._normalize_score(getattr(hit, "score", None)),
                            "collection": collection_name,
                        }
                    )

        # merge and rank by normalized score desc; preserve the highest score per call_id
        ranked: dict[int, dict] = {}
        for hit in merged_hits:
            existing = ranked.get(hit["call_id"])
            if existing is None or hit["score"] > existing["score"]:
                ranked[hit["call_id"]] = hit

        ordered_call_ids = [item["call_id"] for item in sorted(ranked.values(), key=lambda x: x["score"], reverse=True)[:top_k]]

        calls: list[Call] = []
        for call_id in ordered_call_ids:
            call = CallTools.get_call_by_id(self.db, call_id)
            if call is not None:
                calls.append(call)

        return calls
