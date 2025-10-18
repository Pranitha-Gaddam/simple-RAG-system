from __future__ import annotations
from typing import List, Dict
from .embed import embed_texts
from .store import FaissStore

def top_k(store: FaissStore, query: str, k: int = 5) -> List[Dict]:
    qvec = embed_texts([query])  # shape (1, dim)
    return store.search(qvec, k)
