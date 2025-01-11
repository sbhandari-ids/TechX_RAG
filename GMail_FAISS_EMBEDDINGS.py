import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

def load_data(file_content: str) -> str:
    """Loads text data from a file."""
    loader = TextLoader(file_content)
    return loader.load()

def split_text(data: str, chunk_size: int = 1000, chunk_overlap: int = 50) -> list[str]:
    """Splits text data into chunks."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_documents(data)

def create_vector_store(embeddings, texts: list[str]) -> FAISS:
    """Creates a FAISS vector store from a list of texts."""
    return FAISS.from_texts(texts=texts, embedding=embeddings)

def main():
    # load_dotenv()
    openai_api_key = os.getenv("OpenAI_SECRET_KEY")
    if not openai_api_key:
        raise ValueError("OpenAI API key not found")

    file_path = "email_text.txt"

    with open('email_text.txt', 'r') as file:
        email_text = file.read()

    file_content = email_text

    data = load_data(file_content)
    splits = split_text(data)

    print("Total Number of Chunks", len(splits))

    embeddings = OpenAIEmbeddings()

    vector_store = FAISS.from_texts(texts=splits[:5], embedding=embeddings)

    for i in range(10, len(splits), 9):
        # print(f"Processing chunks {i} to {i+10}")
        vector_store.add_texts(texts=splits[i:i+10], embedding=embeddings)

    vector_store.save_local("email_vector_store")
   
# Attempting to save the vector_store files within the project directory
    # vector_store_path = "/Users/SB/TechX_RAG/email_vector_store"
    # vector_store.save_local(vector_store_path)

if __name__ == "__main__":
    main()