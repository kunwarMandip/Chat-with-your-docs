import chromadb
from openai import OpenAI
from app.config import EMBEDDING_MODEL, CHROMA_DB_PATH, GROQ_API_KEY, GROQ_MODEL

chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = chroma_client.get_or_create_collection(name="documents")

llm = OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")

def retrieve_chunks(question, n_results=3):
    results = collection.query(query_texts=[question], n_results=n_results)
    return results['documents'][0], results['metadatas'][0]


def ask_question(question):
    chunks, metadatas = retrieve_chunks(question)

    context = "\n\n---\n\n".join(chunks)
    prompt = f"""Answer the question using ONLY the context below. If the answer isn't in the context, say so — don't make anything up.

Context:
{context}

Question: {question}

Answer:"""

    response = llm.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    sources = sorted(set(m['source'] for m in metadatas))
    return response.choices[0].message.content, sources

if __name__ == "__main__":
    question = input("Ask a question about your documents: ")
    answer, sources = ask_question(question)
    print(f"\nAnswer: {answer}")
    print(f"Sources: {', '.join(sources)}")