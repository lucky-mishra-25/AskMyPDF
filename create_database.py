from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

# =========================
# LOAD PDF
# =========================
loader = PyPDFLoader(
    "document_loaders/deeplearning.pdf"
)

pages = loader.load()

print(f"Total Pages Loaded: {len(pages)}")

# =========================
# SPLIT DOCUMENTS
# =========================
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(pages)

print(f"Total Chunks Created: {len(chunks)}")

# =========================
# EMBEDDING MODEL
# =========================
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# =========================
# CREATE CHROMA VECTOR DB
# =========================
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory="chroma_db"
)

vectorstore.persist()

print("✅ Chroma Vector Database Created Successfully")