from typing import List, Callable
import re
from app.core.config import settings

_sentence_splitter = re.compile(r"(?<=[.!?])\s+")


def _simple_tokenize(text: str) -> List[str]:
    return text.split()


def _tokens_to_text(tokens: List[str]) -> str:
    return " ".join(tokens).strip()


# Lazy-loaded HF tokenizer to avoid heavy imports at module import time
_HF_TOKENIZER = None
_HF_TOKENIZER_NAME = getattr(settings, "BGE_TOKENIZER_NAME", None)


def get_hf_tokenizer():
    global _HF_TOKENIZER
    if _HF_TOKENIZER is not None:
        return _HF_TOKENIZER

    if not _HF_TOKENIZER_NAME:
        return None

    try:
        from transformers import AutoTokenizer

        _HF_TOKENIZER = AutoTokenizer.from_pretrained(_HF_TOKENIZER_NAME, use_fast=True)
        return _HF_TOKENIZER
    except Exception:
        _HF_TOKENIZER = None
        return None


def _hf_tokenize(text: str) -> List[int]:
    tk = get_hf_tokenizer()
    if tk is None:
        # fallback to simple byte-ish tokens to keep lengths sensible
        return [len(t) for t in text.split()]
    try:
        return tk.encode(text, add_special_tokens=False)
    except Exception:
        return [len(t) for t in text.split()]


def _hf_decode(token_ids: List[int]) -> str:
    tk = get_hf_tokenizer()
    if tk is None:
        # best-effort fallback
        return " ".join(str(t) for t in token_ids)
    try:
        return tk.decode(token_ids, skip_special_tokens=True)
    except Exception:
        return " ".join(str(t) for t in token_ids)


def chunk_text(text: str, max_tokens: int | None = None, overlap_tokens: int | None = None, tokenizer: Callable[[str], List[str]] | None = None) -> List[str]:
    """
    Token-aware chunker. Tries to respect sentence boundaries while keeping chunks
    under `max_tokens`. If `tokenizer` is not provided, falls back to simple
    whitespace tokenization. Returns a list of text chunks.
    """
    if not text:
        return []

    if max_tokens is None:
        max_tokens = settings.CHUNK_MAX_TOKENS
    if overlap_tokens is None:
        overlap_tokens = settings.CHUNK_OVERLAP_TOKENS

    use_hf = get_hf_tokenizer() is not None

    if tokenizer is None:
        # If HF tokenizer available, use it for sentence-level tokenization; otherwise use simple
        tokenizer = (lambda s: _hf_tokenize(s) if get_hf_tokenizer() is not None else _simple_tokenize(s))

    # Split into sentences first to keep natural boundaries
    sentences = [s.strip() for s in _sentence_splitter.split(text.strip()) if s.strip()]
    if not sentences:
        # Fallback: split by tokens directly
        tokens = tokenizer(text)
        if not tokens:
            return []
        chunks = []
        step = max_tokens - overlap_tokens if max_tokens > overlap_tokens else max_tokens
        for i in range(0, len(tokens), step):
            chunk_tokens = tokens[i : i + max_tokens]
            if use_hf:
                chunks.append(_hf_decode(chunk_tokens))
            else:
                chunks.append(_tokens_to_text(chunk_tokens))
        return chunks

    # Convert sentences to token id lists (or token lists)
    sentence_tokens = [tokenizer(s) for s in sentences]

    chunks: List[str] = []
    current_tokens: List[int] | List[str] = []

    def flush_current():
        nonlocal current_tokens
        if current_tokens:
            if use_hf:
                chunks.append(_hf_decode(current_tokens))
            else:
                chunks.append(_tokens_to_text(current_tokens))
            current_tokens = []

    for idx, toks in enumerate(sentence_tokens):
        tlen = len(toks)
        if not current_tokens:
            # If single sentence exceeds max_tokens, split it
            if tlen > max_tokens:
                for i in range(0, tlen, max_tokens):
                    part = toks[i : i + max_tokens]
                    if use_hf:
                        chunks.append(_hf_decode(part))
                    else:
                        chunks.append(_tokens_to_text(part))
                continue
            current_tokens = toks.copy()
            continue

        if len(current_tokens) + tlen <= max_tokens:
            # Append sentence tokens into current chunk
            current_tokens.extend(toks)
            continue

        # Flush current and build overlap
        flush_current()
        # Build overlap using last sentences up to overlap_tokens
        overlap: List[int] | List[str] = []
        total = 0
        for s_tokens in reversed(sentence_tokens[:idx]):
            s_len = len(s_tokens)
            if total + s_len > overlap_tokens:
                break
            overlap = s_tokens + overlap
            total += s_len

        current_tokens = overlap.copy()

        # Now handle sentence that may itself be longer than max_tokens
        if tlen > max_tokens:
            # flush overlap if any
            if current_tokens:
                flush_current()
                current_tokens = []
            for i in range(0, tlen, max_tokens):
                part = toks[i : i + max_tokens]
                if use_hf:
                    chunks.append(_hf_decode(part))
                else:
                    chunks.append(_tokens_to_text(part))
            continue

        # Start new chunk with overlap + this sentence
        current_tokens.extend(toks)

    if current_tokens:
        flush_current()

    return [c for c in chunks if c]
