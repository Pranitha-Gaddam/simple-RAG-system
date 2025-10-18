from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any, Tuple
import json
import numpy as np
import faiss

class FaissStore:
    """Persist FAISS index + metadata (chunk texts, sources) under data/."""
    def __init__(self, index_dir: Path):
        self.index_dir = index_dir
        self.index_file = index_dir / "index.faiss"
        self.meta_file = index_dir / "meta.json"
        self.index = None
        self.meta: List[Dict[str, Any]] = []

    # ---------- persistence ----------
    def _save(self):
        self.index_dir.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(self.index_file))
        self.meta_file.write_text(json.dumps(self.meta, ensure_ascii=False))

    def _load(self) -> bool:
        if self.index_file.exists() and self.meta_file.exists():
            self.index = faiss.read_index(str(self.index_file))
            self.meta = json.loads(self.meta_file.read_text())
            return True
        return False

    # ---------- build/search ----------
    def build(self, embeddings: np.ndarray, metadatas: List[Dict[str, Any]]):
        dim = embeddings.shape[1]
        # Using inner product (IP). With normalized vectors, IP ≈ cosine sim.
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(embeddings)
        self.meta = metadatas
        self._save()

    def search(self, query_vec: np.ndarray, k: int) -> List[Dict[str, Any]]:
        if self.index is None:
            if not self._load():
                raise RuntimeError("Index not built yet. Call /index first.")
        D, I = self.index.search(query_vec.astype("float32"), k)
        out = []
        for score, idx in zip(D[0], I[0]):
            if idx == -1:
                continue
            m = self.meta[int(idx)]
            out.append({"score": float(score), **m})
        return out
