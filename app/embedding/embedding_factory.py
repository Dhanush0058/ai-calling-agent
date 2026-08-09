from app.core.config import settings


def get_embedding_provider():
    provider = getattr(settings, "EMBEDDING_PROVIDER", None) or "local"
    return provider.lower()

import os

from app.embedding.bge_embedding import BGEEmbedding


class EmbeddingFactory:

    @staticmethod
    def get_provider():
        provider = os.getenv("EMBEDDING_PROVIDER", "bge")
        if provider == "bge":
            return BGEEmbedding()

        # Add more providers here (openai, gemini, etc.)
        return BGEEmbedding()

