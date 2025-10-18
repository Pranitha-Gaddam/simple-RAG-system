from __future__ import annotations
from pathlib import Path
from typing import List, Dict
import re

ALLOWED_EXTS = {".md", ".txt"}

def load_text_files(folder: Path) -> List[Path]:
    paths: List[Path] = []
    for p in folder.rglob("*"):
        if p.suffix.lower() in ALLOWED_EXTS and p.is_file():
            paths.append(p)
    return paths

def split_to_chunks(text: str, max_chars: int = 1200, overlap: int = 200) -> List[str]:
    """Simple paragraph-based chunking with overlap.
    Why overlap? It preserves context across chunk boundaries.
    """
    paras = re.split(r"\n\s*\n", text.strip())
    chunks, buf = [], ""
    for p in paras:
        if len(buf) + len(p) + 2 < max_chars:
            buf = (buf + "\n\n" + p).strip()
        else:
            if buf:
                chunks.append(buf)
            buf = p
    if buf:
        chunks.append(buf)

    if overlap and len(chunks) > 1:
        merged = []
        for i, c in enumerate(chunks):
            prev_tail = chunks[i-1][-overlap:] if i > 0 else ""
            merged.append((prev_tail + "\n" + c).strip())
        return merged
    return chunks

def build_docs_from_folder(folder: Path) -> List[Dict]:
    """Turn notes into a list of {id, source, text} chunks."""
    docs: List[Dict] = []
    for fp in load_text_files(folder):
        text = fp.read_text(encoding="utf-8", errors="ignore")
        for i, ch in enumerate(split_to_chunks(text)):
            docs.append({"id": f"{fp}#chunk{i}", "source": str(fp), "text": ch})
    return docs
