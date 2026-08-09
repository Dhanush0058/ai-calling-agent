from unittest.mock import MagicMock, patch

from app.models.call import Call
from app.rag.retriever import Retriever
from app.rag.rag_service import RAGService


class DummyHit:
    def __init__(self, payload):
        self.payload = payload


def test_retriever_returns_call_objects_from_qdrant_hits():
    db = MagicMock()
    fake_call = Call()
    fake_call.id = 123
    fake_call.summary = "Customer reported a billing issue"
    fake_call.intent = "Billing"
    fake_call.sentiment = "Negative"
    fake_call.transcript = "The customer said the charge was incorrect."

    with patch("app.rag.retriever.EmbeddingService") as mock_embedding_service, patch(
        "app.rag.retriever.VectorService"
    ) as mock_vector_service, patch(
        "app.rag.retriever.CallTools.get_call_by_id"
    ) as mock_get_call:
        mock_embedding_service.return_value.embed.return_value = [MagicMock(vector=[0.1, 0.2, 0.3])]
        mock_vector_service.return_value.search.return_value = [DummyHit({"call_id": "123"})]
        mock_get_call.return_value = fake_call

        retriever = Retriever(db)
        result = retriever.retrieve("Have I reported this issue before?", top_k=5)

    assert len(result) == 1
    assert result[0].id == 123
    assert result[0].summary == "Customer reported a billing issue"
    mock_get_call.assert_called_once_with(db, 123)


def test_rag_service_builds_prompt_with_relevant_calls():
    fake_call = Call()
    fake_call.id = 1
    fake_call.summary = "A technician visit resolved the network outage."
    fake_call.intent = "Technical Support"
    fake_call.sentiment = "Positive"
    fake_call.transcript = "Customer reported no internet. Technician replaced the router."

    with patch("app.rag.rag_service.Retriever") as mock_retriever, patch(
        "app.rag.rag_service.Reranker.rerank", return_value=[fake_call]
    ), patch("app.integrations.llm_client.LLMClient.chat", return_value="stubbed response") as mock_chat:
        mock_retriever.return_value.retrieve.return_value = [fake_call]

        rag_service = RAGService(db=MagicMock(), customer_id=None)
        response = rag_service.process(
            "What happened during my last similar complaint?",
            tool_result="No tools used.",
        )

    assert response == {"response": "stubbed response"}
    assert mock_chat.called
    prompt_text = mock_chat.call_args.args[0]
    assert "Relevant Calls:" in prompt_text
    assert "A technician visit resolved the network outage." in prompt_text
    assert "What happened during my last similar complaint?" in prompt_text
