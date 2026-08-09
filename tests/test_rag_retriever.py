from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from app.rag.retriever import Retriever


class DummyHit:
    def __init__(self, payload, score):
        self.payload = payload
        self.score = score


def test_retrieve_uses_multiple_collections_and_merges_hits():
    retriever = Retriever(db=object())
    retriever.embedding_service = MagicMock()
    retriever.embedding_service.embed.return_value = [MagicMock(vector=[0.1, 0.2, 0.3])]

    retriever.vector_service = MagicMock()
    retriever.vector_service.search.side_effect = [
        [DummyHit({"call_id": "10"}, score=0.15)],
        [DummyHit({"call_id": "20"}, score=0.95)],
    ]

    with patch("app.rag.retriever.CallTools.get_call_by_id", side_effect=lambda db, call_id: SimpleNamespace(id=int(call_id))):
        calls = retriever.retrieve("what happened", top_k=5)

    assert [call.id for call in calls] == [20, 10]
    assert retriever.vector_service.search.call_count == 2
