from __future__ import annotations
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer

_model = None


def get_model():
    """Lazy-load the sentence transformer model."""
    global _model
    if _model is None:
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return _model


def embed_texts(texts: List[str]) -> np.ndarray:
    """Generate L2-normalized embeddings for semantic similarity search."""
    model = get_model()
    vecs = model.encode(texts, normalize_embeddings=True, convert_to_numpy=True)
    return np.array(vecs, dtype="float32")
