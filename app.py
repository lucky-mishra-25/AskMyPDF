import os
import tempfile

import streamlit as st
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

st.set_page_config(page_title="RAG Book Assistant")

st.title("📚 RAG Book Assistant")
st.write("Upload a PDF and ask questions from the document")

uploaded_file = st.file_uploader(
    "Upload PDF",
    type="pdf"
)

# =========================
# CREATE DATABASE
# =========================
if uploaded_file:

    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        file_path = tmp_file.name

    st.success("PDF Uploaded Successfully")

    if st.button("Create Vector Database"):

        with st.spinner("Processing PDF..."):

            loader = PyPDFLoader(file_path)
            pages = loader.load()

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )

            chunks = splitter.split_documents(pages)

            embedding_model = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )

            vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=embedding_model,
                persist_directory="chroma_db"
            )

            vectorstore.persist()

        st.success("✅ Vector Database Created")

# =========================
# LOAD DATABASE
# =========================
if os.path.exists("chroma_db"):

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma(
        persist_directory="chroma_db",
        embedding_function=embedding_model
    )

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 4,
            "fetch_k": 10,
            "lambda_mult": 0.5
        }
    )

    llm = ChatMistralAI(
        model="mistral-small-latest"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a helpful AI assistant.

Use ONLY the provided context to answer the question.

If answer is not found in context,
say: 'I could not find the answer in the document.'
"""
            ),
            (
                "human",
                """Context:
{context}

Question:
{question}
"""
            )
        ]
    )

    st.divider()
    st.subheader("Ask Questions")

    query = st.text_input("Ask your question")

    if query:

        docs = retriever.invoke(query)

        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )

        final_prompt = prompt.invoke({
            "context": context,
            "question": query
        })

        response = llm.invoke(final_prompt)

        st.write("### Answer")
        st.write(response.content)

else:
    st.warning("Please create the vector database first")