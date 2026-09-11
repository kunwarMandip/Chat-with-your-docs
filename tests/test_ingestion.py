from app.ingestion import chunk_text

def test_chunk_text_splits_correctly():
    text = "a" * 2500
    chunks = chunk_text(text, chunk_size=1000, overlap=200)
    assert len(chunks) == 4
    assert chunks[0] == text[0:1000]

def test_chunk_text_overlap_is_correct():
    text = "0123456789" * 300
    chunks = chunk_text(text, chunk_size=1000, overlap=200)
    # the last 200 chars of chunk 1 should equal the first 200 chars of chunk 2
    assert chunks[0][-200:] == chunks[1][:200]