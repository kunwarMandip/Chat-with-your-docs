# Chat With Your Docs

A RAG (Retrieval-Augmented Generation) application that lets you upload PDF documents and ask questions about them in plain English, with answers grounded in the actual document content and sourced back to the file they came from.

**Live demo:** https://your-app.streamlit.app
**Backend API:** https://chat-with-your-docs-mnsg.onrender.com/docs

## How it works
1. Upload a PDF — it's split into chunks and embedded using Chroma's built-in ONNX-based embedding model
2. Ask a question — it's embedded the same way, and the most relevant chunks are retrieved by vector similarity
3. Those chunks are passed to an LLM (via Groq's free API) as context, which answers using only that content

## Tech stack
- **Backend:** FastAPI, ChromaDB (vector store), Groq API (LLM inference)
- **Frontend:** Streamlit
- **Testing:** pytest
- **Deployment:** Render (backend), Streamlit Community Cloud (frontend)

## Running locally
1. `python -m venv venv` then activate it
2. `pip install -r requirements.txt`
3. Add your `GROQ_API_KEY` to a `.env` file
4. `python -m app.ingestion` to index documents in `/documents`
5. `uvicorn app.main:app --reload --port 8080` to start the API
6. `streamlit run frontend/app.py` to start the UI

## Known limitations
- Render's free tier resets its filesystem on restart, so ingested documents don't persist across cold starts — fine for a live demo, not production-grade persistence.