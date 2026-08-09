from unittest.mock import MagicMock, patch


def test_ai_chat_with_multi_collection_retrieval(client, auth_headers, created_customer):
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
            json={"transcript": "Customer reported a router replacement and billing issue."},
        )
        assert end_resp.status_code == 200

    with patch("app.rag.retriever.EmbeddingService.embed", return_value=[MagicMock(vector=[0.1, 0.2, 0.3])]), patch(
        "app.rag.retriever.VectorService.search",
        side_effect=[
            [type("Hit", (), {"payload": {"call_id": str(call["id"])}, "score": 0.87})()],
            [type("Hit", (), {"payload": {"call_id": str(call["id"])}, "score": 0.91})()],
        ],
    ), patch("app.integrations.llm_client.LLMClient.chat", return_value="RAG response"):
        resp = client.post(
            "/ai/chat",
            headers=auth_headers,
            params={"message": "What happened in my last similar complaint?"},
        )

    assert resp.status_code == 200
    payload = resp.json()
    assert payload["response"] == "RAG response"
