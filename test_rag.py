from src.rag_chain import ask

perguntas = [
    "Onde posso ir num date barato e ao ar livre em Recife?",
    "Qual restaurante é bom para um jantar romântico especial?",
    "Tem algum lugar com vista bonita para date ao entardecer?",
]

for p in perguntas:
    print(f"\nPergunta: {p}")
    print(f"Resposta: {ask(p)}")
    print("-" * 60)