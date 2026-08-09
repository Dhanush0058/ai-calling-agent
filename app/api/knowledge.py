from pathlib import Path

from fastapi import APIRouter, UploadFile, File, Form, Request
from fastapi import HTTPException
from pydantic import BaseModel
import shutil
import tempfile

from app.knowledge.document_processor import DocumentProcessor
from app.knowledge.knowledge_service import KnowledgeService
from app.knowledge.doc_index import get_documents, get_document, delete_document
from app.vector.vector_service import VectorService

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


class QueryRequest(BaseModel):
    question: str
    top_k: int = 5


@router.post("/upload")
def upload(file: UploadFile = File(...), source_name: str = Form(None)):
    # Save upload to temp file using the original extension so file loaders detect the correct format
    suffix = Path(file.filename).suffix or "_upload"
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as fh:
            shutil.copyfileobj(file.file, fh)
            tmp_path = fh.name
    finally:
        file.file.close()

    proc = DocumentProcessor()
    try:
        count = proc.ingest(tmp_path, source_name or file.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"stored_chunks": count}


@router.post("/ingest")
def ingest(file: UploadFile = File(...), source_name: str = Form(None)):
    return upload(file=file, source_name=source_name)


@router.get("/documents")
def list_documents():
    docs = get_documents()
    # return as list
    return {"documents": list(docs.values())}


@router.get("/documents/{doc_id}")
def get_document_api(doc_id: str):
    doc = get_document(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="document not found")
    return doc


@router.delete("/documents/{doc_id}")
def delete_document_api(doc_id: str):
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
async def query(request: Request, question: str | None = Form(None), top_k: int | None = Form(None)):
    payload = None
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        payload = await request.json()

    if isinstance(payload, dict):
        question_value = payload.get("question")
        top_k_value = payload.get("top_k", 5)
    else:
        question_value = question
        top_k_value = top_k if top_k is not None else 5

    if not question_value:
        raise HTTPException(status_code=400, detail="question is required")

    svc = KnowledgeService()
    result = svc.answer(str(question_value), int(top_k_value))
    return result
