from dotenv import load_dotenv
load_dotenv()

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

# =========================
# DOCUMENTS
# =========================
docs = [
    Document(
        page_content="Python is widely used in Artificial Intelligence.",
        metadata={"source": "AI_book"}
    ),

    Document(
        page_content="Pandas is used for data analysis in Python.",
        metadata={"source": "DataScience_book"}
    ),

    Document(
        page_content="Neural networks are used in deep learning.",
        metadata={"source": "DL_book"}
    ),
]

# =========================
# FREE EMBEDDING MODEL
# =========================
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# =========================
# CREATE VECTOR STORE
# =========================
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embedding_model,
    persist_directory="chroma-db"
)

print("✅ Vector Store Created")

# =========================
# SIMILARITY SEARCH
# =========================
result = vectorstore.similarity_search(
    "what is used for data analysis?",
    k=2
)

print("\n=== Similarity Search Results ===\n")

for r in result:
    print(r.page_content)
    print(r.metadata)
    print()

# =========================
# RETRIEVER
# =========================
retriever = vectorstore.as_retriever()

retrieved_docs = retriever.invoke(
    "Explain deep learning"
)

print("\n=== Retriever Results ===\n")

for d in retrieved_docs:
    print(d.page_content)