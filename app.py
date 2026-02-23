from flask import Flask, render_template, jsonify, request
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_community.llms import CTransformers
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from dotenv import load_dotenv
import os
from src.prompt import *
from src.helper import load_embedding_model

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

embeddings = load_embedding_model()
pc = Pinecone(api_key= PINECONE_API_KEY)
index_name="medical-chatbot"

vectorstore = PineconeVectorStore.from_existing_index(
    index_name= index_name,
    embedding=embeddings
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)

PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

llm = CTransformers(
    model="model/llama-2-7b-chat.Q4_K_M.gguf",
    model_type="llama",
    config={
        "max_new_tokens": 512,
        "temperature": 0.3
    }
)

document_chain = create_stuff_documents_chain(
    llm=llm,
    prompt=PROMPT
)

qa = create_retrieval_chain(
    retriever,
    document_chain
)

@app.route("/")
def index():
    return render_template('chat.html')


if __name__ == '__main__':
    app.run(debug= True)