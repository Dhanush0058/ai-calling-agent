from pathlib import Path
from typing import List
import uuid
from datetime import datetime, timezone

from app.knowledge.document_loader import load_document_text
from app.knowledge.chunker import chunk_text
from app.embedding.embedding_service import EmbeddingService
from app.vector.vector_service import VectorService
from app.core.config import settings
from app.knowledge.doc_index import add_document


class DocumentProcessor:
    COLLECTION = "knowledge_embeddings"

    def __init__(self, embedding_service: EmbeddingService | None = None, vector_service: VectorService | None = None):
        self.embedding_service = embedding_service or EmbeddingService()
        self.vector_service = vector_service or VectorService()

    def ingest(self, path: str, source_name: str | None = None, max_tokens: int = 200, overlap_tokens: int = 50, category: str | None = None) -> int:
        doc = load_document_text(path)
        # `doc` is a dict with 'text' and 'pages'
        pages = doc.get("pages") if isinstance(doc, dict) else [doc]

        if not pages:
            return 0

        doc_path = Path(source_name or path)
        document_id = uuid.uuid4().hex
        metadata = {
            "document_id": document_id,
            "source": source_name or path,
            "document_name": doc_path.name,
            "document_type": doc_path.suffix.lower().lstrip('.') or "text",
            "category": category,
            "upload_timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        }

        # Build chunks per page and keep mapping to page/chunk index
        all_chunks: List[str] = []
        chunk_map: List[dict] = []
        for page_idx, page_text in enumerate(pages):
            if not page_text or not page_text.strip():
                continue
            chunks = chunk_text(page_text, max_tokens=max_tokens, overlap_tokens=overlap_tokens)
            for cidx, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                chunk_map.append({"page": page_idx, "chunk_index": cidx})

        if not all_chunks:
            return 0

        # embed all chunks in batch
        embeddings = self.embedding_service.embed(all_chunks)

        stored = 0
        point_ids: List[str] = []
        for idx, emb in enumerate(embeddings):
            point_id = uuid.uuid4().hex
            mapping = chunk_map[idx]
            payload = {
                **metadata,
                "page_number": mapping.get("page"),
                "chunk_index": mapping.get("chunk_index"),
                "text": all_chunks[idx][:2000],
            }
            try:
                self.vector_service.store(self.COLLECTION, point_id, emb.vector, payload)
                stored += 1
                point_ids.append(point_id)
            except Exception:
                continue

        # record document in index with point ids
        index_entry = {
            **metadata,
            "page_count": len(pages),
            "chunk_count": len(all_chunks),
            "point_ids": point_ids,
        }
        add_document(document_id, index_entry)

        return stored
