from search import search_prompt

def main():
    question = "Qual é o faturamento da Alfa Logística Holding?"
    chain = search_prompt(question)

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return

    print(f"Pergunta: {question}")
    print(f"Resposta: {chain.content}")

if __name__ == "__main__":
    main()