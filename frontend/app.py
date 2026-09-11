import streamlit as st
import requests

API_URL = "https://chat-with-your-docs-mnsg.onrender.com"

st.title("Chat with your docs")

# --- Upload section ---
st.header("Upload a document")
uploaded_file = st.file_uploader("Choose a PDF", type="pdf")

if uploaded_file is not None and st.button("Ingest document"):
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
    with st.spinner("Ingesting..."):
        response = requests.post(f"{API_URL}/ingest", files=files)
    if response.status_code == 200:
        st.success(response.json()["message"])
    else:
        st.error(f"Failed: {response.json()['detail']}")

# --- Question section ---
st.header("Ask a question")
question = st.text_input("Your question")

if st.button("Ask") and question:
    with st.spinner("Thinking..."):
        response = requests.post(f"{API_URL}/ask", json={"question": question})
    if response.status_code == 200:
        data = response.json()
        st.write(data["answer"])
        st.caption(f"Sources: {', '.join(data['sources'])}")
    else:
        st.error(f"Failed: {response.json()['detail']}")