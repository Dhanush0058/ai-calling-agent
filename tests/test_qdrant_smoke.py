import os
import tempfile

import pytest

from app.vector.vector_service import VectorService
from app.knowledge.document_processor import DocumentProcessor
from app.embedding.embedding_result import EmbeddingResult


@pytest.mark.skipif(not os.getenv("QDRANT_URL"), reason="QDRANT_URL not configured")
def test_live_qdrant_smoke(monkeypatch):
    # Stub embedding service used by DocumentProcessor to avoid heavy model loads
    class DummyEmbeddingService:
        def embed(self, texts):
            # return a fixed low-dim vector for each text
            return [EmbeddingResult(vector=[0.1, 0.2, 0.3, 0.4], model="stub", dimensions=4, provider="test") for _ in texts]

    # Monkeypatch the embedding service inside the document processor
    monkeypatch.setattr("app.knowledge.document_processor.EmbeddingService", DummyEmbeddingService)

    # Write a temporary text file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="wb") as fh:
        fh.write(b"This is a smoke test document. It has some text to index.")
        path = fh.name

    try:
        proc = DocumentProcessor()
        stored = proc.ingest(path, source_name="smoke.txt", max_tokens=50, overlap_tokens=10)
        assert stored > 0

        vs = VectorService()
        # search using same vector as the stub
        hits = vs.search(DocumentProcessor.COLLECTION, [0.1, 0.2, 0.3, 0.4], limit=5)
        assert isinstance(hits, list)
        assert len(hits) >= 1
    finally:
        try:
            os.remove(path)
        except Exception:
            pass
