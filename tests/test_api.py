from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ask_rejects_empty_question():
    response = client.post("/ask", json={"question": "   "})
    assert response.status_code == 400

def test_ingest_rejects_non_pdf():
    response = client.post(
        "/ingest",
        files={"file": ("test.txt", b"some text", "text/plain")}
    )
    assert response.status_code == 400