from typing import Sequence

try:
    from sentence_transformers import SentenceTransformer
except Exception:  # pragma: no cover - optional dependency in constrained environments
    SentenceTransformer = None

from app.embedding.embedding_result import EmbeddingResult


class LocalEmbedding:

    MODEL_NAME = "all-MiniLM-L6-v2"

    def __init__(self):
        self.model = None

    def _load_model(self):
        if self.model is not None:
            return self.model
        if SentenceTransformer is None:
            raise RuntimeError("sentence-transformers is not available")
        self.model = SentenceTransformer(self.MODEL_NAME)
        return self.model

    def embed(self, texts: Sequence[str]) -> list[EmbeddingResult]:
        try:
            model = self._load_model()
            vectors = model.encode(list(texts), convert_to_numpy=True, normalize_embeddings=True)
        except Exception:
            zero_vector = [0.0] * 384
            return [
                EmbeddingResult(
                    vector=zero_vector[:],
                    model="fallback",
                    dimensions=len(zero_vector),
                    provider="fallback",
                )
                for _ in texts
            ]

        results = []
        for vector in vectors.tolist():
            results.append(
                EmbeddingResult(
                    vector=vector,
                    model=self.MODEL_NAME,
                    dimensions=len(vector),
                    provider="local",
                )
            )
        return results

    def store(self, summary: str, embedding: list[float], metadata: dict | None = None) -> str:
        # Placeholder for vector database storage. Keep consistent with prior API.
        import uuid

        return uuid.uuid4().hex

