# 💕 Date Finder Recife

Agente de IA que recomenda lugares para date em Recife (restaurantes, passeios, mirantes etc.) com base em um acervo próprio de locais, usando a técnica de **RAG (Retrieval-Augmented Generation)**. O usuário conversa em linguagem natural (ex: "quero um date barato ao ar livre") e o agente responde citando o local ideal e o motivo da recomendação, sempre com base no contexto recuperado — sem inventar informações.

**🔗 Acesse online:** [agentdaterecife.streamlit.app](https://agentdaterecife-blxbnkyymph8gp8zt3s4xu.streamlit.app/)

## Arquitetura da solução

O projeto segue um pipeline clássico de RAG, dividido em duas etapas: **ingestão** (offline) e **consulta** (online).

```
data/*.md  --(1) load + split-->  chunks
                                     |
                                (2) embeddings (Gemini)
                                     v
                              chroma_db/ (vector store)
                                     ^
                                     | (3) retrieval (top-k)
Pergunta do usuário --------------> retriever
                                     |
                              (4) contexto + pergunta
                                     v
                            Prompt Template (few-shot instruction)
                                     |
                                     v
                     LLM (Gemini Flash) --> Resposta
                                     ^
                                     |
                          Interface de chat (Streamlit)
```

1. **Ingestão** (`src/ingest.py`): os locais cadastrados em `data/*.md` são carregados, divididos em chunks (`MarkdownTextSplitter`) e transformados em embeddings com o modelo `gemini-embedding-001`. Os vetores são persistidos em um banco vetorial **Chroma** (`chroma_db/`).
2. **Recuperação + geração** (`src/rag_chain.py`): a pergunta do usuário é usada para buscar os `k` chunks mais relevantes no Chroma. Esse contexto é injetado em um prompt que instrui o modelo `gemini-flash-latest` a responder **apenas** com base nas informações recuperadas, citando o nome do local e o motivo da recomendação.
3. **Interface** (`app.py`): uma interface de chat construída com **Streamlit**, que mantém o histórico da conversa na sessão e envia cada pergunta para a cadeia RAG.

O banco vetorial (`chroma_db/`) já vem pré-gerado no repositório, então não é necessário rodar a ingestão para usar o agente — apenas para atualizar a base de locais.

## Tecnologias e ferramentas utilizadas

- **Python 3.13**
- **[LangChain](https://python.langchain.com/)** — orquestração da cadeia de RAG (loaders, text splitters, prompts, runnables)
- **[langchain-google-genai](https://python.langchain.com/docs/integrations/providers/google/)** — integração com os modelos Gemini (embeddings e LLM)
- **Google Gemini** — `gemini-embedding-001` (embeddings) e `gemini-flash-latest` (geração de respostas)
- **[Chroma](https://www.trychroma.com/)** (`langchain-chroma` / `chromadb`) — banco de dados vetorial
- **[Streamlit](https://streamlit.io/)** — interface de chat
- **python-dotenv** — carregamento de variáveis de ambiente (`.env`)

## Instruções para executar o projeto

> Quer só testar o agente sem instalar nada? Acesse a versão publicada: https://agentdaterecife-blxbnkyymph8gp8zt3s4xu.streamlit.app/

Para rodar localmente:

### Pré-requisitos
- Python 3.10+
- Uma chave de API do Google Gemini ([Google AI Studio](https://aistudio.google.com/))

### 1. Clone o repositório e crie o ambiente virtual
```bash
git clone <url-do-repositorio>
cd agent_date_recife
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # Linux/Mac
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto com sua chave da API do Gemini:
```
GOOGLE_API_KEY=sua_chave_aqui
```

### 4. (Opcional) Gere o banco vetorial
Necessário apenas se você adicionar ou alterar arquivos em `data/`. O repositório já inclui um `chroma_db/` pronto para uso.
```bash
python -m src.ingest
```

### 5. Rode a interface de chat
```bash
streamlit run app.py
```

### Testar via terminal (sem interface)
```bash
python test_rag.py
```

## Exemplos de perguntas que o agente consegue responder

- "Onde posso ir num date barato e ao ar livre em Recife?"
- "Qual restaurante é bom para um jantar romântico especial?"
- "Tem algum lugar com vista bonita para date ao entardecer?"
- "Quero um lugar tranquilo pra um primeiro encontro descontraído."
- "Onde comemorar um aniversário de namoro sem gastar muito?"

## Exemplos de respostas geradas pelo agente

Conversa real registrada no app publicado ([agentdaterecife.streamlit.app](https://agentdaterecife-blxbnkyymph8gp8zt3s4xu.streamlit.app/)):

> 🤖 Oi! Me conta que tipo de date você procura (barato, romântico, ao ar livre...) que eu te ajudo a escolher um lugar em Recife 😊
>
> 🧑 Gostaria de um local aberto, e bonito, vista romântica
>
> 🤖 Recomendo o **Parque Dona Lindu**, pois é um local ao ar livre (aberto), localizado na orla, ideal para ver o pôr do sol com um ambiente tranquilo e romântico.
>
> Outra opção é o **Mirante do Alto da Sé** (no Recife Antigo), que é um local histórico e aberto, oferecendo um ambiente romântico com vista panorâmica.

Outros exemplos:

> **Pergunta:** Onde posso ir num date barato e ao ar livre em Recife?
>
> **Resposta:** Uma boa opção é o **Parque Dona Lindu**, na orla de Boa Viagem. É gratuito, ao ar livre e tem um clima tranquilo e romântico, ideal para caminhar, ver o pôr do sol e até fazer um piquenique — perfeito para um date econômico.

> **Pergunta:** Qual restaurante é bom para um jantar romântico especial?
>
> **Resposta:** Recomendo a **Mercearia Pará**, em Boa Vista. É um restaurante conhecido por menus especiais para casais em datas comemorativas, com pratos autorais e um ambiente intimista e aconchegante — ótimo para um jantar romântico ou aniversário de namoro.

> **Pergunta:** Tem algum lugar com vista bonita para date ao entardecer?
>
> **Resposta:** O **Mirante do Alto da Sé**, no Marco Zero (Recife Antigo), é uma ótima pedida. É um local histórico e gratuito, com vista panorâmica, ideal para um date ao entardecer ou um passeio cultural.

*As respostas reais podem variar de acordo com o modelo e o contexto recuperado no momento da consulta.*
