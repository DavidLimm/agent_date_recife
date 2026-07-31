from langchain_google_genai import ChatGoogleGenerativeAI
from src.config import GOOGLE_API_KEY

llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", google_api_key=GOOGLE_API_KEY)
resposta = llm.invoke("Diga apenas 'conexão funcionando' se você recebeu esta mensagem.")
print(resposta.content)