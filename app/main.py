import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.ingestion import ingest_pdf_bytes
from app.retrieval import ask_question

app = FastAPI(title="Chat with your docs")

class QuestionRequest(BaseModel):
    question: str
    
@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    file_bytes = await file.read()
    num_chunks = ingest_pdf_bytes(file_bytes, file.filename)
    return {"message": f"Successfully ingested {file.filename} ({num_chunks} chunks)"}

@app.post("/ask")
async def ask(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    answer, sources = ask_question(request.question)
    return {"answer": answer, "sources": sources}