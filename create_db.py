from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

documents = []

# 🔹 Load all PDFs from data folder
for file in os.listdir("data"):
    if file.endswith(".pdf"):
        loader = PyPDFLoader(f"data/{file}")
        documents.extend(loader.load())

# 🔹 Split into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
)

docs = splitter.split_documents(documents)

# 🔹 Metadata tagging
for doc in docs:
    text = doc.page_content.lower()
    
    if "dpdp" in text or "data protection" in text:
        doc.metadata["Law_Type"] = "DPDP"
    elif "bank" in text or "nomination" in text:
        doc.metadata["Law_Type"] = "Banking"
    else:
        doc.metadata["Law_Type"] = "Other"

# 🔹 FREE embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 🔹 Create FAISS DB
db = FAISS.from_documents(docs, embeddings)
db.save_local("db")

print("✅ Vector DB created successfully (FREE version)!")