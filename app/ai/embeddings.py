from typing import Sequence
import uuid

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer


class Embeddings:

    MODEL_NAME = "all-MiniLM-L6-v2"

    def __init__(self):
        self.model = SentenceTransformer(self.MODEL_NAME)

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        embeddings = self.model.encode(list(texts), convert_to_numpy=True, normalize_embeddings=True)
        return embeddings.tolist()

    def similarity(self, query_embedding: list[float], candidate_embeddings: Sequence[list[float]]) -> list[float]:
        query_array = np.asarray(query_embedding).reshape(1, -1)
        candidate_array = np.asarray(candidate_embeddings)
        scores = cosine_similarity(query_array, candidate_array)[0]
        return scores.tolist()

    def store(self, summary: str, embedding: list[float], metadata: dict | None = None) -> str:
        # Placeholder for vector database storage.
        # Replace this method with a real vector DB client integration.
        return uuid.uuid4().hex
