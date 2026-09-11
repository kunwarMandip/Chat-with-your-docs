import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.ingestion import ingest_document
from app.retrieval import ask_question

app = FastAPI(title="Chat with your docs")

class QuestionRequest(BaseModel):
    question: str
    
@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    save_path = os.path.join("documents", file.filename)
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ingest_document(save_path)
    return {"message": f"Successfully ingested {file.filename}"}

@app.post("/ask")
async def ask(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    answer, sources = ask_question(request.question)
    return {"answer": answer, "sources": sources}