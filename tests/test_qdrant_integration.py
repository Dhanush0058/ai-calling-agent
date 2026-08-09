import os

import pytest

from app.vector.qdrant_client import QdrantClient


@pytest.mark.skipif(not os.getenv("QDRANT_URL"), reason="QDRANT_URL not configured")
def test_qdrant_client_can_upsert_and_search():
    client = QdrantClient()
    collection = "test_collection"
    point_id = "integration-test-point"

    try:
        client.upsert(collection, point_id, [0.1, 0.2, 0.3], {"text": "integration test"})
        hits = client.search(collection, [0.1, 0.2, 0.3], limit=5)
    finally:
        try:
            client.delete(collection, point_id)
        except Exception:
            pass

    assert isinstance(hits, list)
