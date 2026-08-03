import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import MarkdownTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from src.config import GOOGLE_API_KEY

DATA_PATH = "data"
CHROMA_PATH = "chroma_db"


def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.md", loader_cls=TextLoader)
    documents = loader.load()
    print(f"{len(documents)} documentos carregados.")
    return documents


def split_documents(documents):
    splitter = MarkdownTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)
    print(f"{len(chunks)} chunks gerados.")
    return chunks


def save_to_chroma(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY
    )

    # limpa o banco antigo, se existir, pra sempre reconstruir do zero
    if os.path.exists(CHROMA_PATH):
        import shutil
        shutil.rmtree(CHROMA_PATH)

    db = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=CHROMA_PATH
    )
    print(f"Banco vetorial salvo em '{CHROMA_PATH}'.")


def main():
    documents = load_documents()
    chunks = split_documents(documents)
    save_to_chroma(chunks)


if __name__ == "__main__":
    main()