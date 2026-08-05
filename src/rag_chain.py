from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from src.config import GOOGLE_API_KEY

CHROMA_PATH = "chroma_db"

PROMPT_TEMPLATE = """
Você é um assistente especializado em recomendar locais para date em Recife.
Responda a pergunta do usuário usando APENAS as informações do contexto abaixo.
Se o contexto não tiver informação suficiente, diga que não encontrou um local
que combine com o pedido, não invente informações.

Contexto:
{context}

Pergunta: {question}

Resposta (seja direto, cite o nome do local e o motivo da recomendação):
"""


def format_docs(docs):
    return "\n\n---\n\n".join(doc.page_content for doc in docs)


def build_rag_chain():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY
    )

    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 4})

    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.3
    )

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain


def ask(question: str) -> str:
    chain = build_rag_chain()
    return chain.invoke(question)