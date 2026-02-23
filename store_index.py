from src.helper import load_pdf, text_split, load_embedding_model
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from dotenv import load_dotenv

import os

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key= PINECONE_API_KEY)

extracted_data = load_pdf("data/")
text_chunks = text_split(extracted_data)

filtered_chunks = []

for chunk in text_chunks:
    content = chunk.page_content.lower()

    if "key terms" in content:
        continue
    if "organizations" in content:
        continue
    if content.strip().startswith("allergen —"):
        continue

    filtered_chunks.append(chunk)


embeddings = load_embedding_model()
vectorstore = PineconeVectorStore.from_documents(documents=filtered_chunks, embedding=embeddings, index_name="medical-chatbot")
