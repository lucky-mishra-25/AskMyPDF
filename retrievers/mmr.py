from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# =========================
# DOCUMENTS
# =========================
docs = [
    Document(page_content="Gradient descent is an optimization algorithm used in machine learning."),
    Document(page_content="Gradient descent minimizes the loss function."),
    Document(page_content="Neural networks use gradient descent for training."),
    Document(page_content="Support Vector Machines are supervised learning algorithms.")
]

# =========================
# EMBEDDINGS
# =========================
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# =========================
# VECTORSTORE
# =========================
vectorstore = Chroma.from_documents(
    docs,
    embeddings
)

# =========================
# MMR RETRIEVER
# =========================
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 3}
)

results = retriever.invoke(
    "What is gradient descent?"
)

print("\n===== MMR RESULTS =====\n")

for doc in results:
    print(doc.page_content)