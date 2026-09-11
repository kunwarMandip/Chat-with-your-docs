import os
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
from app.config import EMBEDDING_MODEL, CHROMA_DB_PATH, CHUNK_SIZE, CHUNK_OVERLAP

embedder = SentenceTransformer(EMBEDDING_MODEL)
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = chroma_client.get_or_create_collection(name="documents")

def load_pdf_text(filepath):
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def ingest_document(filepath):
    print(f"Loading {filepath}...")
    text = load_pdf_text(filepath)
    chunks = chunk_text(text)
    print(f"Split into {len(chunks)} chunks")

    embeddings = embedder.encode(chunks).tolist()

    filename = os.path.basename(filepath)
    ids = [f"{filename}_{i}" for i in range(len(chunks))]
    metadatas = [{"source": filename, "chunk_index": i} for i in range(len(chunks))]

    collection.add(ids=ids, embeddings=embeddings, documents=chunks, metadatas=metadatas)
    print(f"Ingested {len(chunks)} chunks from {filename}")

if __name__ == "__main__":
    for filename in os.listdir("documents"):
        if filename.endswith(".pdf"):
            ingest_document(os.path.join("documents", filename))
    print("Total chunks now in the collection:", collection.count())