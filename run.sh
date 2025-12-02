#!/bin/bash

# Simple script to run the semantic notes search server

echo "Starting Semantic Notes Search Server..."
echo "Server will be available at http://localhost:8000"
echo "Web UI: http://localhost:8000/ui"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

uvicorn app.api:app --reload --host 0.0.0.0 --port 8000

