# RAG Assistant

Retrieval-Augmented Generation system for querying scientific PDFs using pgvector and Ollama.

## Features

- 📄 PDF ingestion with intelligent chunking
- 🔍 Vector search with pgvector (cosine distance)
- 🤖 Local LLM via Ollama (llama3.2:3b)
- 🌐 Web interface with Gradio
- ⚡ Streaming responses

Batarin Kirill

## Demonstration

Gradio:
<video src="https://github.com/batarikiri/my_rag/blob/main/demo_5x.webm?raw=true" controls width="700"></video>
Terminal:
<video src="demo_3x.webm" controls width="700"></video>

## Features

- 📄 PDF ingestion with intelligent chunking
- 🔍 Vector search with pgvector  
- 🤖 Local LLM via Ollama (llama3.2:3b)
- 🌐 Web interface with Gradio

## Quick Start

```bash
# Clone
git clone https://github.com/batarikiri/my_rag.git
cd my_rag

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start PostgreSQL with pgvector
docker compose up -d

# Start Ollama (in separate terminal)
ollama serve

# Initialize database
python scripts/init_db.py

# Place your PDFs in data/pdf/ and index
python scripts/ingest.py

# Run web interface
python app.py
# Open http://localhost:7860

# Run in Terminal
python scripts/ask.py


