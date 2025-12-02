from __future__ import annotations
from typing import List, Dict
from .embed import embed_texts
from .store import FaissStore


def top_k(store: FaissStore, query: str, k: int = 5) -> List[Dict]:
    """Perform semantic search and return top-k results."""
    qvec = embed_texts([query])
    return store.search(qvec, k)
