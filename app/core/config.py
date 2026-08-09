from dotenv import load_dotenv
import os


load_dotenv()


class Settings:
    APP_NAME = os.getenv("APP_NAME")
    APP_VERSION = os.getenv("APP_VERSION")
    DEBUG = os.getenv("DEBUG")
    HOST = os.getenv("HOST")
    PORT = os.getenv("PORT")
    
    DATABASE_URL = os.getenv("DATABASE_URL")

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_API_URL = os.getenv("OPENROUTER_API_URL")
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-oss-20b:free")
    OPENROUTER_REASONING = os.getenv("OPENROUTER_REASONING", "false").lower() in ("1", "true", "yes")

    # Embedding configuration
    EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "bge")  # 'local' or 'bge'
    BGE_API_KEY = os.getenv("BGE_API_KEY")
    BGE_API_URL = os.getenv("BGE_API_URL")  # e.g. provider endpoint that accepts texts
    # Tokenizer / chunker defaults
    BGE_TOKENIZER_NAME = os.getenv("BGE_TOKENIZER_NAME", "BAAI/bge-m3")
    CHUNK_MAX_TOKENS = int(os.getenv("CHUNK_MAX_TOKENS", "400"))
    CHUNK_OVERLAP_TOKENS = int(os.getenv("CHUNK_OVERLAP_TOKENS", "50"))

    # Qdrant configuration for vector storage
    QDRANT_URL = os.getenv("QDRANT_URL") or None
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY") or None
    QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "call_embeddings")
    QDRANT_COLLECTIONS = [c.strip() for c in os.getenv("QDRANT_COLLECTIONS", "call_embeddings,knowledge_embeddings").split(",") if c.strip()]


settings = Settings()