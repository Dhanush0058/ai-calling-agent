import pytest

from app.knowledge.chunker import chunk_text


def test_chunk_text_preserves_sentences_and_overlap():
    text = (
        "Sentence one. Sentence two. Sentence three? "
        "Sentence four! Sentence five. Sentence six."
    )

    # use smaller max_tokens so text splits into multiple chunks
    chunks = chunk_text(text, max_tokens=10, overlap_tokens=3)

    assert len(chunks) >= 2
    assert all(chunk.endswith(('.', '?', '!')) or chunk.endswith('six.') for chunk in chunks)
    assert any('Sentence three?' in chunk and 'Sentence four!' in chunk for chunk in chunks)
    assert chunks[0] != chunks[1]


def test_chunk_text_handles_long_sentence():
    text = ("word " * 1200).strip()

    chunks = chunk_text(text, max_tokens=500, overlap_tokens=100)

    assert len(chunks) == 3
    # ensure token counts are within bounds
    assert all(len(c.split()) <= 500 for c in chunks)
    assert " ".join(c for c in chunks) == text
