from typing import Sequence
import requests

try:
    from sentence_transformers import SentenceTransformer
except Exception:  # pragma: no cover - optional dependency in constrained environments
    SentenceTransformer = None

from app.core.config import settings
from app.embedding.embedding_result import EmbeddingResult


class BGEEmbedding:

    MODEL_NAME = "BAAI/bge-m3"
    FALLBACK_DIMENSIONS = 1024

    def __init__(self):
        # If BGE endpoint and API key are configured, use a remote embedding service.
        self.bge_url = getattr(settings, "BGE_API_URL", None)
        self.bge_key = getattr(settings, "BGE_API_KEY", None)
        self.model = None
        self.remote = bool(self.bge_url and self.bge_key)

    def _load_local_model(self):
        if self.model is not None:
            return self.model
        if SentenceTransformer is None:
            raise RuntimeError("sentence-transformers is not available")
        self.model = SentenceTransformer(self.MODEL_NAME)
        return self.model

    def _fallback_vector(self, text_count: int) -> list[EmbeddingResult]:
        vector = [0.0] * self.FALLBACK_DIMENSIONS
        return [
            EmbeddingResult(
                vector=vector[:],
                model="fallback",
                dimensions=len(vector),
                provider="fallback",
            )
            for _ in range(text_count)
        ]

    def embed(self, texts: Sequence[str]) -> list[EmbeddingResult]:
        if self.remote:
            try:
                headers = {"Authorization": f"Bearer {self.bge_key}", "Content-Type": "application/json"}
                resp = requests.post(self.bge_url, json={"texts": list(texts)}, headers=headers, timeout=30)
                resp.raise_for_status()
                data = resp.json()
                vectors = data.get("embeddings", [])

                results = []
                for vector in vectors:
                    results.append(
                        EmbeddingResult(
                            vector=vector,
                            model=self.MODEL_NAME,
                            dimensions=len(vector),
                            provider="bge",
                        )
                    )
                return results
            except Exception:
                # Remote call failed — fallback to local model below.
                pass

        try:
            model = self._load_local_model()
            vectors = model.encode(list(texts), convert_to_numpy=True, normalize_embeddings=True)
        except Exception:
            return self._fallback_vector(len(list(texts)))

        results = []
        seq = vectors.tolist() if hasattr(vectors, "tolist") else list(vectors)
        for vector in seq:
            results.append(
                EmbeddingResult(
                    vector=vector,
                    model="all-MiniLM-L6-v2",
                    dimensions=len(vector),
                    provider="local",
                )
            )
        return results

    def store(self, summary: str, embedding: list[float], metadata: dict | None = None) -> str:
        # Placeholder for vector database storage. Keep API consistent with other adapters.
        import uuid

        return uuid.uuid4().hex

