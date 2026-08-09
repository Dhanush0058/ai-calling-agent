from fastapi.testclient import TestClient


class DummyProcessor:
    def __init__(self, *args, **kwargs):
        pass

    def ingest(self, path, source_name=None, max_tokens=200, overlap_tokens=50, category=None):
        return 3


class DummyKnowledgeService:
    def __init__(self, *args, **kwargs):
        pass

    def answer(self, question, top_k=5):
        return {"response": "stubbed answer", "hits": [{"text": "policy snippet"}]}


def test_upload_route_accepts_file_and_returns_summary(monkeypatch):
    from app.main import app

    monkeypatch.setattr("app.api.knowledge.DocumentProcessor", DummyProcessor)

    client = TestClient(app)
    response = client.post(
        "/knowledge/upload",
        files={"file": ("sample.txt", b"hello world", "text/plain")},
        data={"source_name": "sample.txt"},
    )

    assert response.status_code == 200
    assert response.json() == {"stored_chunks": 3}


def test_query_route_accepts_json_body(monkeypatch):
    from app.main import app

    monkeypatch.setattr("app.api.knowledge.KnowledgeService", DummyKnowledgeService)

    client = TestClient(app)
    response = client.post(
        "/knowledge/query",
        json={"question": "What is policy?", "top_k": 2},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["response"] == "stubbed answer"
    assert payload["hits"][0]["text"] == "policy snippet"
