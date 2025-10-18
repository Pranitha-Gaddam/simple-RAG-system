from __future__ import annotations
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer

# Lazy-load the model once; it's ~80MB
_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return _model

def embed_texts(texts: List[str]) -> np.ndarray:
    """Return L2-normalized embeddings (float32) for cosine similarity."""
    model = get_model()
    vecs = model.encode(texts, normalize_embeddings=True, convert_to_numpy=True)
    return np.array(vecs, dtype="float32")
