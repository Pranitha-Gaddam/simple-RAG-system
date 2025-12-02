# RAG Semantic Search - Base Implementation

A base-level implementation of RAG (Retrieval-Augmented Generation) for semantic document search. This project demonstrates the core concepts of RAG: document indexing, vector embeddings, and semantic similarity search. Perfect for learning how RAG systems work or as a starting point for more advanced implementations.

## What is RAG?

**RAG (Retrieval-Augmented Generation)** combines information retrieval with AI to find relevant documents based on meaning, not just keywords. 

**How it works:**
1. **Indexing**: Documents are split into chunks and converted to vector embeddings (mathematical representations that capture semantic meaning)
2. **Search**: Your query is also converted to a vector and compared against all document chunks
3. **Retrieval**: The system returns the top-k most relevant chunks based on semantic similarity

Unlike traditional keyword search, RAG understands context and meaning. For example, searching for "AI learning" will find documents about "machine learning" even though the exact words don't match!

## Features

- **Semantic Search**: Find documents based on meaning, not just keyword matching
- **Document Chunking**: Intelligent text splitting with overlap to preserve context
- **Vector Storage**: Efficient FAISS-based vector index for fast similarity search
- **Web Interface**: User-friendly UI with clear explanations of what's happening
- **REST API**: FastAPI-based API for programmatic access
- **Persistent Index**: Saves and loads vector index for quick startup
- **Example Documents**: Includes sample documents to get you started

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

## Quick Start

1. **Start the server** (choose one method):
   - **Using the run script**:
     ```bash
     ./run.sh
     ```
   - **Or directly with uvicorn**:
     ```bash
     uvicorn app.api:app --reload
     ```

   The server will start on `http://localhost:8000`

2. **Build the index**: 
   - **Web UI**: Visit `http://localhost:8000/ui` and click "Build Index"
     - This processes all documents in the `notes/` folder
     - Documents are split into chunks and converted to vector embeddings
     - A searchable index is created and saved
   - **API**: 
     ```bash
     curl -X POST http://localhost:8000/index -H "Content-Type: application/json" -d '{}'
     ```

3. **Search your documents**:
   - **Web UI**: Enter your query in the search box and click "Search"
     - The system finds the top-k most relevant document chunks using semantic similarity
     - Results are displayed with relevance scores and source information
   - **API**: 
     ```bash
     curl "http://localhost:8000/search?q=machine+learning&k=5"
     ```

## Usage

### Using the Web Interface

1. **Start the server** and visit `http://localhost:8000/ui`
2. **Build Index**: Click "Build Index" to process all documents in the `notes/` folder
   - The system will split documents into chunks and generate embeddings
   - You'll see how many chunks were indexed
3. **Search**: Enter a natural language query and click "Search"
   - Results show relevant document chunks with relevance scores
   - Each result displays the source file and the matching text

### Adding Your Own Documents

The project comes with 8 example documents in the `notes/` directory. You can:
- Add your own `.txt` files to the `notes/` folder
- Edit existing documents
- After making changes, **rebuild the index** to include them in searches

All documents should be plain text format for best results.

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
  
  Example response:
  ```json
  {
    "results": [
      {
        "score": 0.85,
        "id": "notes/machine-learning.txt#chunk0",
        "source": "notes/machine-learning.txt",
        "text": "Machine learning is a subset of artificial intelligence..."
      }
    ]
  }
  ```

## How It Works (Technical Details)

This implementation demonstrates the core RAG pipeline:

1. **Document Processing**: Plain text files (`.txt`) are loaded from the `notes/` folder
2. **Chunking**: Documents are split into chunks (~1200 chars) with overlap (~200 chars) to preserve context
3. **Embedding Generation**: Each chunk is converted to a 384-dimensional vector using the `all-MiniLM-L6-v2` sentence transformer model
4. **Indexing**: Embeddings are stored in a FAISS index (using inner product similarity with normalized vectors, which approximates cosine similarity)
5. **Search**: 
   - User query is converted to a vector embedding
   - Query vector is compared against all indexed chunks using similarity search
   - Top-k most similar chunks are retrieved
6. **Retrieval**: Results are returned with similarity scores, source files, and chunk text

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
├── notes/              # Place your documents here (includes example docs)
├── data/               # Generated index files (gitignored)
├── requirements.txt    # Python dependencies
└── run.sh              # Convenience script to start the server
```

## Example Documents

The project includes 8 example documents covering related topics:
- **machine-learning.txt** - Fundamentals of ML, supervised/unsupervised learning
- **vector-embeddings.txt** - How embeddings work and semantic similarity
- **rag-systems.txt** - RAG architecture and implementation
- **api-design.txt** - RESTful API best practices
- **neural-networks.txt** - Deep learning and neural network basics
- **natural-language-processing.txt** - NLP fundamentals and transformers
- **information-retrieval.txt** - Search systems and ranking algorithms
- **database-systems.txt** - Database types including vector databases

These documents are intentionally related and overlapping to demonstrate how semantic search finds connections between concepts.

## Example Queries

Try these semantic search queries to see RAG in action and test cross-document relationships:
- "How does machine learning work?"
- "What are vector embeddings?"
- "Explain RAG systems"
- "How do neural networks learn?"
- "What is natural language processing?"
- "How do databases store vectors?"
- "Information retrieval methods"
- "API design best practices"

**Notice**: The system finds relevant content even when the exact words don't match! Try queries like "AI learning algorithms" and see how it connects to machine learning and neural networks. This demonstrates the power of semantic search - it understands meaning and relationships, not just keywords.

## Development

To run in development mode with auto-reload:
```bash
uvicorn app.api:app --reload --host 0.0.0.0 --port 8000
```

To check API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Deployment / Hosting

This application can be hosted online on various platforms. Here are some options:

### Platform Requirements
- Python 3.8+ support
- Persistent file storage (for `notes/` and `data/` folders)
- At least 512MB RAM (for model loading)
- ~200MB disk space (for dependencies and model)

### Hosting Options

**1. Railway** (Recommended - Easy setup)
- Connect your GitHub repo
- Railway auto-detects Python apps
- Free tier available
- Persistent storage included

**2. Render**
- Connect GitHub repo
- Use "Web Service" type
- Set build command: `pip install -r requirements.txt`
- Set start command: `uvicorn app.api:app --host 0.0.0.0 --port $PORT`
- Free tier available

**3. Heroku**
- Uses `Procfile` (already included)
- Set stack: `heroku stack:set heroku-22`
- Free tier discontinued, but paid plans available

**4. DigitalOcean App Platform**
- Connect GitHub repo
- Auto-detects FastAPI
- Paid plans start at $5/month

**5. VPS (DigitalOcean, AWS EC2, etc.)**
- Full control over environment
- Install dependencies: `pip install -r requirements.txt`
- Run with: `uvicorn app.api:app --host 0.0.0.0 --port 8000`
- Use systemd or supervisor for process management

### Important Notes for Hosting

1. **Model Download**: The sentence transformer model (~80MB) downloads automatically on first use. This may take a minute on first request.

2. **Persistent Storage**: Ensure `notes/` and `data/` folders persist across deployments. Some platforms reset the filesystem on each deploy.

3. **Environment Variables**: The app uses relative paths. If needed, you can modify `app/api.py` to use environment variables for custom paths.

4. **CORS**: Currently set to allow all origins (`*`). For production, consider restricting to your domain.

5. **Production Server**: For production, consider using gunicorn with uvicorn workers:
   ```bash
   pip install gunicorn
   gunicorn app.api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
   ```

### Quick Deploy Checklist
- [ ] Push code to GitHub
- [ ] Connect repo to hosting platform
- [ ] Ensure `notes/` folder is included in deployment
- [ ] Set PORT environment variable (if required by platform)
- [ ] Build and deploy
- [ ] Test the `/health` endpoint
- [ ] Build index via `/ui` or `/index` endpoint

## License

MIT

