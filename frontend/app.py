import streamlit as st
import requests

API_URL = "https://chat-with-your-docs-mnsg.onrender.com"

st.title("Chat with your docs")

st.header("Upload a document")
uploaded_file = st.file_uploader("Choose a PDF", type="pdf")

if uploaded_file is not None and st.button("Ingest document"):
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
    with st.spinner("Ingesting... (can take up to a minute if the backend was asleep)"):
        try:
            response = requests.post(f"{API_URL}/ingest", files=files, timeout=120)
            if response.status_code == 200:
                st.success(response.json()["message"])
            else:
                try:
                    st.error(f"Failed: {response.json()['detail']}")
                except requests.exceptions.JSONDecodeError:
                    st.error(f"Backend returned an unexpected response (status {response.status_code}). It may still be waking up — try again in a moment.")
        except requests.exceptions.RequestException as e:
            st.error(f"Could not reach the backend: {e}")

st.header("Ask a question")
question = st.text_input("Your question")

if st.button("Ask") and question:
    with st.spinner("Thinking..."):
        try:
            response = requests.post(f"{API_URL}/ask", json={"question": question}, timeout=120)
            if response.status_code == 200:
                data = response.json()
                st.write(data["answer"])
                st.caption(f"Sources: {', '.join(data['sources'])}")
            else:
                try:
                    st.error(f"Failed: {response.json()['detail']}")
                except requests.exceptions.JSONDecodeError:
                    st.error(f"Backend returned an unexpected response (status {response.status_code}). It may still be waking up — try again in a moment.")
        except requests.exceptions.RequestException as e:
            st.error(f"Could not reach the backend: {e}")