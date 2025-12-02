# Semantic Notes Search

A RAG (Retrieval-Augmented Generation) system for semantic search over text documents. This project demonstrates how to build a production-ready semantic search engine using vector embeddings and similarity search.

## Features

- **Semantic Search**: Find documents based on meaning, not just keyword matching
- **Document Chunking**: Intelligent text splitting with overlap to preserve context
- **Vector Storage**: Efficient FAISS-based vector index for fast similarity search
- **REST API**: FastAPI-based API with web UI for easy interaction
- **Persistent Index**: Saves and loads vector index for quick startup

## Tech Stack

- **FastAPI**: Modern Python web framework for building APIs
- **Sentence Transformers**: Pre-trained models for generating semantic embeddings
- **FAISS**: Facebook AI Similarity Search library for efficient vector operations
- **Uvicorn**: ASGI server for running the FastAPI application
- **NumPy**: Numerical computing for vector operations

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd semantic-notes-search
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. **Add your documents**: Place `.md` or `.txt` files in the `notes/` directory

2. **Start the server**:
```bash
uvicorn app.api:app --reload
```

3. **Build the index**: 
   - Visit `http://localhost:8000/ui` for the web interface, or
   - Use the API: `POST http://localhost:8000/index`

4. **Search**:
   - Use the web UI at `http://localhost:8000/ui`, or
   - Use the API: `GET http://localhost:8000/search?q=your+query&k=5`

## API Endpoints

- `GET /health` - Health check endpoint
- `POST /index` - Index documents from the notes folder
  ```json
  {
    "folder": "optional/path/to/folder"
  }
  ```
- `GET /search?q=<query>&k=<number>` - Semantic search
  - `q`: Search query (required)
  - `k`: Number of results (default: 5, max: 20)

## How It Works

1. **Document Processing**: Text files are split into chunks with overlap to preserve context
2. **Embedding Generation**: Each chunk is converted to a vector embedding using a sentence transformer model
3. **Indexing**: Embeddings are stored in a FAISS index for fast similarity search
4. **Search**: Query is embedded and compared against indexed vectors using cosine similarity
5. **Retrieval**: Top-k most similar chunks are returned with their source documents

## Project Structure

```
semantic-notes-search/
├── app/
│   ├── api.py          # FastAPI application and endpoints
│   ├── chunk.py        # Document chunking logic
│   ├── embed.py        # Embedding generation
│   ├── search.py       # Search functionality
│   ├── store.py        # FAISS vector store
│   └── static/
│       └── index.html  # Web UI
├── notes/              # Place your documents here
├── data/               # Generated index files (gitignored)
└── requirements.txt    # Python dependencies
```

## License

MIT

