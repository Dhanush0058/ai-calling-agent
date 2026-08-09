from unittest.mock import MagicMock, patch

from app.rag.retriever import Retriever


class DummyHit:
    def __init__(self, payload):
        self.payload = payload


def test_vectors_search_endpoint(client, auth_headers, created_customer):
    # Patch LLM so downstream processing (sentiment/summary) doesn't call external API
    with patch("app.integrations.llm_client.LLMClient.chat", return_value="(stub)"):
        # Create a call, then end it so it's present in DB
        call_resp = client.post(
            "/calls",
            headers=auth_headers,
            json={"customer_id": created_customer["id"]},
        )
        assert call_resp.status_code == 201
        call = call_resp.json()

        end_resp = client.put(
            f"/calls/{call['id']}",
            headers=auth_headers,
            json={"transcript": "Customer reported a billing error."},
        )
        assert end_resp.status_code == 200

    # Mock embedding and vector search to return our call id
    with patch("app.api.vectors.EmbeddingService.embed", return_value=[MagicMock(vector=[0.1, 0.2, 0.3])]), patch(
        "app.api.vectors.VectorService.search",
        return_value=[DummyHit({"call_id": str(call["id"])})],
    ):
        resp = client.post(
            "/vectors/search",
            json={"query": "Have I reported this issue before?", "limit": 5},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["query"] == "Have I reported this issue before?"
    assert len(data["results"]) >= 1
    assert data["results"][0]["payload"]["call_id"] == str(call["id"]) 


def test_ai_chat_rag_flow(client, auth_headers, created_customer):
    from unittest.mock import patch

    # Create and end a call to have data in DB; mock LLM so processing doesn't call external API
    with patch("app.integrations.llm_client.LLMClient.chat", return_value="(stub)"):
        call_resp = client.post(
            "/calls",
            headers=auth_headers,
            json={"customer_id": created_customer["id"]},
        )
        assert call_resp.status_code == 201
        call = call_resp.json()

        end_resp = client.put(
            f"/calls/{call['id']}",
            headers=auth_headers,
            json={"transcript": "Customer reported no internet; technician replaced router."},
        )
        assert end_resp.status_code == 200

    # Patch Retriever's internal search/embed and Gemini to keep test deterministic
    with patch("app.rag.retriever.EmbeddingService.embed", return_value=[MagicMock(vector=[0.1, 0.2, 0.3])]), patch(
        "app.rag.retriever.VectorService.search", return_value=[DummyHit({"call_id": str(call["id"])})]
    ), patch("app.integrations.llm_client.LLMClient.chat", return_value="RAG response"):
        resp = client.post(
            "/ai/chat",
            params={"message": "What happened during my last similar complaint?"},
            headers=auth_headers,
        )

    assert resp.status_code == 200
    payload = resp.json()
    assert "response" in payload
    assert payload["response"] == "RAG response"
