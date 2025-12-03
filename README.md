# RAG Semantic Search - Base Implementation

A simple Retrieval-Augmented Generation (RAG) project for semantic document search.
It indexes text files, converts them into vector embeddings, and lets you search by meaning, not just keywords.

Perfect for learning how RAG systems work or as a starting point for more advanced implementations!

Try it out [here](https://web-production-ffab.up.railway.app/ui/)

### What this does

- Converts documents into vector embeddings
- Stores them in a FAISS index
- Lets you search documents using natural language
- Returns the most semantically relevant chunks

### Tech Stack
- FastAPI
- Sentence Transformers
- FAISS
- NumPy
- Uvicorn

## Run locally (can add your own documents)

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

### Quick Start

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
   - **or via API**: 
     ```bash
     curl -X POST http://localhost:8000/index -H "Content-Type: application/json" -d '{}'
     ```

3. **Search your documents**:
   - **Web UI**: Enter your query in the search box and click "Search"
     - The system finds the top-k most relevant document chunks
   - **or via API**: 
     ```bash
     curl "http://localhost:8000/search?q=machine+learning&k=5"
     ```

### Adding Your Own Documents

The project comes with 8 example documents in the `notes/` directory. You can:
- Add your own `.txt` files to the `notes/` folder
- Edit existing documents
- After making changes, **rebuild the index** to include them in searches

All documents should be plain text format for best results.

### How It Works (Technical Details)

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

**Notice**: The system finds relevant content even when the exact words don't match! Try queries like "AI learning algorithms" and see how it connects to machine learning and neural networks. Semantic search understands meaning and relationships, not just keywords.
