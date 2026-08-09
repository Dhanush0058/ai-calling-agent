import os
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, Form, Request, Depends
from fastapi import HTTPException
from pydantic import BaseModel
import shutil
import tempfile

from app.core.dependencies import get_current_user
from app.knowledge.document_processor import DocumentProcessor
from app.knowledge.knowledge_service import KnowledgeService
from app.knowledge.doc_index import get_documents, get_document, delete_document
from app.models.user import User
from app.vector.vector_service import VectorService

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


class QueryRequest(BaseModel):
    question: str
    top_k: int = 5


@router.post("/upload")
def upload(
    file: UploadFile = File(...),
    source_name: str = Form(None),
    category: str | None = Form(None),
    uploader_id: int | None = Form(None),
    mime_type: str | None = Form(None),
    file_size: int | None = Form(None),
    current_user: User = Depends(get_current_user),
):
    suffix = Path(file.filename or "upload.txt").suffix or ".txt"
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as fh:
            shutil.copyfileobj(file.file, fh)
            tmp_path = fh.name
    finally:
        file.file.close()

    actual_file_size = file_size if file_size is not None else (os.path.getsize(tmp_path) if tmp_path else 0)
    proc = DocumentProcessor()
    try:
        metadata = {
            "category": category,
            "uploader_id": uploader_id if uploader_id is not None else current_user.id,
            "mime_type": mime_type or (file.content_type or "application/octet-stream"),
            "file_size": actual_file_size,
        }
        count = proc.ingest(tmp_path, source_name or file.filename, category=category, metadata=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)

    return {"stored_chunks": count}


@router.post("/ingest")
def ingest(
    file: UploadFile = File(...),
    source_name: str = Form(None),
    category: str | None = Form(None),
    uploader_id: int | None = Form(None),
    mime_type: str | None = Form(None),
    file_size: int | None = Form(None),
    current_user: User = Depends(get_current_user),
):
    return upload(
        file=file,
        source_name=source_name,
        category=category,
        uploader_id=uploader_id,
        mime_type=mime_type,
        file_size=file_size,
        current_user=current_user,
    )


@router.get("/documents")
def list_documents(current_user: User = Depends(get_current_user)):
    docs = get_documents()
    ordered = sorted(
        docs.values(),
        key=lambda doc: doc.get("upload_timestamp") or "",
        reverse=True,
    )
    return {"documents": ordered}


@router.get("/documents/{doc_id}")
def get_document_api(doc_id: str, current_user: User = Depends(get_current_user)):
    doc = get_document(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="document not found")
    return doc


@router.delete("/documents/{doc_id}")
def delete_document_api(doc_id: str, current_user: User = Depends(get_current_user)):
    doc = get_document(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="document not found")

    vs = VectorService()
    point_ids = doc.get("point_ids", [])
    collection_name = DocumentProcessor.COLLECTION
    for pid in point_ids:
        try:
            vs.delete(collection_name, pid)
        except Exception:
            continue

    delete_document(doc_id)
    return {"deleted": doc_id}


@router.post("/query")
async def query(
    request: Request,
    question: str | None = Form(None),
    top_k: int | None = Form(None),
    current_user: User = Depends(get_current_user),
):
    payload = None
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        payload = await request.json()

    if isinstance(payload, dict):
        question_value = payload.get("question")
        top_k_value = payload.get("top_k", 5)
        filters_value = payload.get("filters")
    else:
        question_value = question
        top_k_value = top_k if top_k is not None else 5
        filters_value = None

    if not question_value:
        raise HTTPException(status_code=400, detail="question is required")

    svc = KnowledgeService()
    result = svc.answer(str(question_value), int(top_k_value), filters=filters_value)
    return result
