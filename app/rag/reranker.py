from typing import List

from app.models.call import Call


class Reranker:

    def __init__(self):
        pass

    def rerank(self, calls: List[Call], query: str) -> List[Call]:
        # Placeholder for future semantic reranking; for now preserve the order
        # returned by the retriever. The retriever already normalizes and merges
        # scores across vector collections.
        return calls
