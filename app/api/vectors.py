from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.dependencies import get_db
from app.embedding.embedding_service import EmbeddingService
from app.vector.vector_service import VectorService


router = APIRouter(
    prefix="/vectors",
    tags=["Vectors"],
)


class VectorSearchRequest(BaseModel):
    query: str
    limit: int = 5


class VectorSearchHit(BaseModel):
    id: str
    score: float | None = None
    payload: dict[str, Any] | None = None


class VectorSearchResponse(BaseModel):
    query: str
    results: list[VectorSearchHit]


@router.post("/search", response_model=VectorSearchResponse)
def search_vectors(
    request: VectorSearchRequest,
    db: Session = Depends(get_db),
):
    embedding_service = EmbeddingService()
    query_embedding = embedding_service.embed([request.query])[0]

    vector_service = VectorService()
    hits = vector_service.search(
        settings.QDRANT_COLLECTION,
        query_embedding.vector,
        request.limit,
    )

    if hits is None:
        raise HTTPException(status_code=500, detail="Vector search failed")

    results = []
    for hit in hits:
        results.append(
            VectorSearchHit(
                id=str(getattr(hit, "id", "")),
                score=getattr(hit, "score", None),
                payload=getattr(hit, "payload", None),
            )
        )

    return VectorSearchResponse(query=request.query, results=results)
