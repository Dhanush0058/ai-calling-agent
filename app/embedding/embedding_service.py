from typing import Sequence
import uuid

from app.core.config import settings
from app.embedding.embedding_factory import get_embedding_provider
from app.embedding.embedding_result import EmbeddingResult


class EmbeddingService:

    def __init__(self):
        provider = get_embedding_provider()

        if provider == "local":
            from app.embedding.local_embedding import LocalEmbedding

            self.client = LocalEmbedding()
        elif provider in ("bge", "bg-m3", "bgm3"):
            try:
                from app.embedding.bge_embedding import BGEEmbedding

                self.client = BGEEmbedding()
            except Exception:
                from app.embedding.local_embedding import LocalEmbedding

                self.client = LocalEmbedding()
        else:
            from app.embedding.local_embedding import LocalEmbedding

            self.client = LocalEmbedding()

        self.vector_service = None
        if settings.QDRANT_URL:
            try:
                from app.vector.vector_service import VectorService

                self.vector_service = VectorService()
            except Exception:
                self.vector_service = None

    def embed(self, texts: Sequence[str]) -> list[EmbeddingResult]:
        return self.client.embed(texts)

    def store(self, summary: str, embedding: EmbeddingResult, metadata: dict | None = None) -> str:
        if self.vector_service is not None:
            point_id = uuid.uuid4().hex
            payload = {"summary": summary}
            if metadata:
                payload.update(metadata)
            try:
                return self.vector_service.store(
                    settings.QDRANT_COLLECTION,
                    point_id,
                    embedding.vector,
                    payload,
                )
            except Exception:
                pass

        if hasattr(self.client, "store"):
            return self.client.store(summary, embedding.vector, metadata)

        return uuid.uuid4().hex

