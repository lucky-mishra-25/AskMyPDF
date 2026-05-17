from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_mistralai import ChatMistralAI

load_dotenv()

# =========================
# DOCUMENTS
# =========================
docs = [
    Document(page_content="Gradient descent is an optimization algorithm used in machine learning."),
    Document(page_content="Gradient descent minimizes the loss function."),
    Document(page_content="Neural networks use gradient descent for training."),
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

retriever = vectorstore.as_retriever()

# =========================
# LLM
# =========================
llm = ChatMistralAI(
    model="mistral-small-latest"
)

# =========================
# MULTI QUERY RETRIEVER
# =========================
multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=retriever,
    llm=llm
)

query = "What is gradient descent?"

results = multi_query_retriever.invoke(query)

print("\nRetrieved Documents:\n")

for doc in results:
    print(doc.page_content)