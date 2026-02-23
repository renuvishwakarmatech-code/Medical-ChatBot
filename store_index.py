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
embeddings = load_embedding_model()
vectorstore = PineconeVectorStore.from_documents(documents=text_chunks, embedding=embeddings, index_name="medical-chatbot")
