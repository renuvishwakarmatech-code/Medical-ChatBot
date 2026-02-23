from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

def load_pdf(data):
    loader = DirectoryLoader(data ,
                             glob="*.pdf",
                             loader_cls=PyPDFLoader
                            )
    documents = loader.load()
    for doc in documents:
     doc.page_content = doc.page_content.replace("-\n", "")
     doc.page_content = doc.page_content.replace("\n", " ")
    return documents

def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(
              chunk_size = 2500 , chunk_overlap = 500
    )
    texts_chunk = text_splitter.split_documents(extracted_data)
    return texts_chunk


def load_embedding_model():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings

