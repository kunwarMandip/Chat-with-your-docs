import os
import io
from pypdf import PdfReader
import chromadb
from app.config import EMBEDDING_MODEL, CHROMA_DB_PATH, CHUNK_SIZE, CHUNK_OVERLAP

chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = chroma_client.get_or_create_collection(name="documents")

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks
    
def ingest_pdf_bytes(file_bytes, filename, session_id):
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    
    chunks = chunk_text(text)
    ids = [f"{filename}_{i}" for i in range(len(chunks))]
    metadatas = [{"source": filename, "chunk_index": i, "session_id": session_id} for i in range(len(chunks))]
    
    collection.add(ids=ids, documents=chunks, metadatas=metadatas)
    print(f"Ingested {len(chunks)} chunks from {filename}")
    return len(chunks)

#Only for local testing
def ingest_document(filepath):
    with open(filepath, "rb") as f:
        file_bytes = f.read()
    return ingest_pdf_bytes(file_bytes, os.path.basename(filepath))

if __name__ == "__main__":
    for filename in os.listdir("documents"):
        if filename.endswith(".pdf"):
            ingest_document(os.path.join("documents", filename))
    print("Total chunks now in the collection:", collection.count())