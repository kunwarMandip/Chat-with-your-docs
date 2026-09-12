# RAG Chat With Your Docs

A RAG (Retrieval-Augmented Generation) application that lets you upload PDF documents and ask questions about them in plain English, with answers grounded in the actual document content and sourced back to the file they came from.

**Live demo:** https://your-app.streamlit.app
**Backend API:** https://chat-with-your-docs-mnsg.onrender.com/docs

## How it works
1. Upload a PDF — it's processed entirely in memory, split into chunks, and embedded using Chroma's built-in ONNX-based embedding model
2. Ask a question — it's embedded the same way, and the most relevant chunks for your specific session are retrieved by vector similarity
3. Those chunks are passed to an LLM (via Groq's free API) as context, which answers using only that content and cites which file it came from

## Tech stack
- **Backend:** FastAPI, ChromaDB (vector store + built-in embeddings), Groq API (LLM inference)
- **Frontend:** Streamlit
- **Testing:** pytest
- **Deployment:** Render (backend), Streamlit Community Cloud (frontend)

## Design notes
- PDFs are processed entirely in memory — no disk writes — since Render's free tier has an ephemeral filesystem
- Each browser session gets a random ID, and every chunk is tagged with it; questions only ever search within that session's own documents, so multiple concurrent users never see each other's data
- Uses Chroma's built-in ONNX embedding model rather than sentence-transformers/PyTorch, which caused out-of-memory crashes on Render's free 512MB tier

## Running locally
1. `python -m venv venv` then activate it
2. `pip install -r requirements.txt`
3. Add your `GROQ_API_KEY` to a `.env` file
4. `uvicorn app.main:app --reload --port 8080`
5. `streamlit run frontend/app.py`

## Known limitations
- Render's free tier resets its filesystem on restart, so ingested documents don't persist across cold starts
- Session isolation is per-browser-tab, not real user accounts — refreshing the page starts a fresh session
