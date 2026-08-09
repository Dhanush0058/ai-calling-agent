import os
import tempfile

from app.knowledge.document_processor import DocumentProcessor
from app.knowledge.knowledge_retriever import KnowledgeRetriever


class MockEmbedding:
    def embed(self, texts):
        # simple deterministic embedding: vector of token counts
        results = []
        for t in texts:
            tokens = t.split()
            results.append(type("E", (), {"vector": [float(len(tokens))]})())
        return results


class MockVector:
    def __init__(self):
        self.storage = {}

    def store(self, collection_name, point_id, vector, payload=None):
        self.storage[point_id] = {"vector": vector, "payload": payload, "collection": collection_name}
        return point_id

    def search(self, collection_name, vector, limit=5):
        # rank by absolute difference to scalar vector[0]
        if not self.storage:
            return []
        target = vector[0]
        items = []
        for pid, v in self.storage.items():
            if v.get("collection") != collection_name:
                continue
            score = 1.0 / (1.0 + abs(v["vector"][0] - target))
            # mimic Qdrant ScoredPoint-like objects
            items.append(type("H", (), {"id": pid, "payload": v.get("payload"), "score": score})())
        items.sort(key=lambda x: x.score, reverse=True)
        return items[:limit]


def test_ingest_and_retrieve(tmp_path):
    # create a simple text file
    p = tmp_path / "doc.txt"
    p.write_text("Hello world. This is a test document. It has several sentences to chunk.")

    emb = MockEmbedding()
    vec = MockVector()

    proc = DocumentProcessor(embedding_service=emb, vector_service=vec)
    stored = proc.ingest(str(p))
    assert stored > 0

    retriever = KnowledgeRetriever()
    retriever.embedding_service = emb
    retriever.vector_service = vec

    hits = retriever.retrieve("test document", top_k=3)
    assert isinstance(hits, list)
    assert len(hits) > 0
