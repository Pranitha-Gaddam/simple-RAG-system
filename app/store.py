from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any
import json
import numpy as np
import faiss


class FaissStore:
    """FAISS vector store for persisting embeddings and metadata."""
    
    def __init__(self, index_dir: Path):
        self.index_dir = index_dir
        self.index_file = index_dir / "index.faiss"
        self.meta_file = index_dir / "meta.json"
        self.index = None
        self.meta: List[Dict[str, Any]] = []

    def _save(self):
        """Persist index and metadata to disk."""
        self.index_dir.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(self.index_file))
        self.meta_file.write_text(json.dumps(self.meta, ensure_ascii=False))

    def _load(self) -> bool:
        """Load index and metadata from disk if they exist."""
        if self.index_file.exists() and self.meta_file.exists():
            self.index = faiss.read_index(str(self.index_file))
            self.meta = json.loads(self.meta_file.read_text())
            return True
        return False

    def build(self, embeddings: np.ndarray, metadatas: List[Dict[str, Any]]):
        """Build and save FAISS index from embeddings."""
        dim = embeddings.shape[1]
        # Inner product with normalized vectors approximates cosine similarity
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(embeddings)
        self.meta = metadatas
        self._save()

    def search(self, query_vec: np.ndarray, k: int) -> List[Dict[str, Any]]:
        """Search for top-k similar vectors."""
        if self.index is None:
            if not self._load():
                raise RuntimeError("Index not built yet. Call /index first.")
        D, I = self.index.search(query_vec.astype("float32"), k)
        results = []
        for score, idx in zip(D[0], I[0]):
            if idx == -1:
                continue
            m = self.meta[int(idx)]
            results.append({"score": float(score), **m})
        return results
