import json
from pathlib import Path
from typing import Dict, Any

INDEX_PATH = Path(__file__).parent / "doc_index.json"


def _ensure_index():
    if not INDEX_PATH.exists():
        INDEX_PATH.write_text(json.dumps({}))


def load_index() -> Dict[str, Any]:
    _ensure_index()
    try:
        return json.loads(INDEX_PATH.read_text())
    except Exception:
        return {}


def save_index(index: Dict[str, Any]) -> None:
    INDEX_PATH.write_text(json.dumps(index, indent=2))


def add_document(doc_id: str, metadata: Dict[str, Any]) -> None:
    index = load_index()
    index[doc_id] = metadata
    save_index(index)


def get_documents() -> Dict[str, Any]:
    return load_index()


def get_document(doc_id: str) -> Dict[str, Any] | None:
    index = load_index()
    return index.get(doc_id)


def delete_document(doc_id: str) -> None:
    index = load_index()
    if doc_id in index:
        del index[doc_id]
        save_index(index)
