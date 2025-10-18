from __future__ import annotations
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from typing import Optional, List, Dict

from .chunk import build_docs_from_folder
from .embed import embed_texts
from .store import FaissStore
from .search import top_k
from fastapi.staticfiles import StaticFiles
from fastapi import Body

APP_TITLE = "Semantic Notes Search"
NOTES_DIR = Path(__file__).resolve().parent.parent / "notes"  # default notes/
INDEX_DIR = Path(__file__).resolve().parent.parent / "data"

app = FastAPI(title=APP_TITLE, version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)
app.mount(
    "/ui",
    StaticFiles(directory=str(Path(__file__).parent / "static"), html=True),
    name="ui",
)

store = FaissStore(INDEX_DIR)

class IndexRequest(BaseModel):
    folder: Optional[str] = None   # if not provided, use default notes/

class IndexResponse(BaseModel):
    chunks_indexed: int

class SearchResponse(BaseModel):
    results: List[Dict]

@app.get("/health")
def health():
    return {"ok": True, "notes_dir": str(NOTES_DIR)}

@app.post("/index", response_model=IndexResponse)
def index(req: Optional[IndexRequest] = Body(default=None)):
    folder = Path(req.folder) if (req and req.folder) else NOTES_DIR
    docs = build_docs_from_folder(folder)
    if not docs:
        return IndexResponse(chunks_indexed=0)
    texts = [d["text"] for d in docs]
    vecs = embed_texts(texts)
    store.build(vecs, docs)
    return IndexResponse(chunks_indexed=len(docs))

@app.get("/search", response_model=SearchResponse)
def search(q: str = Query(..., description="Your search query"),
           k: int = Query(5, ge=1, le=20)):
    results = top_k(store, q, k)
    return SearchResponse(results=results)
