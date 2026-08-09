import pytest
from pypdf import PdfWriter

from app.knowledge.document_loader import load_document_text


def test_load_document_text_raises_on_pdf_with_no_extractable_text(tmp_path):
    pdf_path = tmp_path / "empty.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    with pdf_path.open("wb") as fh:
        writer.write(fh)

    with pytest.raises(RuntimeError, match="PDF contains no extractable text"):
        load_document_text(str(pdf_path))
