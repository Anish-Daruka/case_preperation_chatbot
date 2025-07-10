import fitz  # PyMuPDF

from langchain.text_splitter import RecursiveCharacterTextSplitter
def extract_text_from_pdf(path):
    doc = fitz.open(path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text


splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
    separators=["\n\n", "\n", ".", " ", ""]
)

def classify_doc_type(filename):
    fname = filename.lower()
    if "framework" in fname or "victor" in fname:
        return "framework"
    elif "guesstimate" in fname:
        return "guesstimate"
    elif "case" in fname:
        return "casebook"
    else:
        return "other"


documents = []

pdf_paths = [
    "FMS_Casebook_20-21.pdf",
    "CIC New Cases.pdf",
    "IIM Ahmedabad Casebook.pdf",
    "Case Compendium.pdf",
    "IIT Madras Casebook.pdf",
    "Capacity change framework.pdf",
    "Case Interviews Cracked.pdf",
    "Victor Cheng - Case Interview Secrets.pdf",
    "caseinterviewframeworks.pdf",
    "Guesstimate Compendium.pdf",
    "Guesstimates.pdf",
    "handoutslides.pdf",
]

for path in pdf_paths:
    path="case_prep_resources/" + path
    text = extract_text_from_pdf(path)
    chunks = splitter.split_text(text)
    print(chunks)
    for i, chunk in enumerate(chunks):
        documents.append({
            "chunk_id": i,
            "text": chunk,
            "doc_type": classify_doc_type(path),
            
        })


from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd
from tqdm.notebook import tqdm

model = SentenceTransformer(
    "all-MiniLM-L6-v2", device="cpu"
)  
texts=[doc['text'] for doc in documents]
vectors = model.encode(
    texts,
    show_progress_bar=True,
)

np.save("caseprep_vectors.npy", vectors, allow_pickle=False)

# Import client library
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

client = QdrantClient("http://localhost:6333")

if not client.collection_exists("case_preperation"):
    client.create_collection(
        collection_name="case_preperation",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )


payload=documents
client.upload_collection(
    collection_name="case_preperation",
    vectors=vectors,
    payload=payload,
    ids=None,  # Vector ids will be assigned automatically
    batch_size=256,  # How many vectors will be uploaded in a single request?
)