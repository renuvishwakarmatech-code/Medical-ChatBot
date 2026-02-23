from flask import Flask, render_template, jsonify, request
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_community.llms import LlamaCpp
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

vectorstore = PineconeVectorStore.from_existing_index(
    index_name="medical-chatbot",
    embedding=embeddings
)

retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 3}
)

PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "input"])

llm = LlamaCpp(
    model_path="model/llama-2-7b-chat.Q4_K_M.gguf",
    temperature=0.2,
    max_tokens=350,
    top_p=0.9,
    top_k=40,
    repeat_penalty=1.25,
    n_ctx=2200,
    verbose=False,
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

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    print("User:", msg)
    response = qa.invoke({
        "input": msg
    })
    answer = response["answer"]
    print(response)
    print("Response:", answer)
    return answer

if __name__ == '__main__':
    app.run(debug= True)