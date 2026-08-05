import streamlit as st
from src.rag_chain import ask

st.set_page_config(page_title="Date Finder Recife", page_icon="💕")

st.title("💕 Date Finder Recife")
st.caption("Pergunte sobre lugares para date em Recife — restaurantes, passeios, mirantes e mais.")

# inicializa o histórico de chat na sessão
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Oi! Me conta que tipo de date você procura (barato, romântico, ao ar livre...) que eu te ajudo a escolher um lugar em Recife 😊"}
    ]

# renderiza o histórico
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# input do usuário
pergunta = st.chat_input("Ex: onde ir num date barato à noite?")

if pergunta:
    st.session_state.messages.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)

    with st.chat_message("assistant"):
        with st.spinner("Procurando o lugar certo..."):
            resposta = ask(pergunta)
            st.markdown(resposta)

    st.session_state.messages.append({"role": "assistant", "content": resposta})