#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Agno
====
Aqui começamos com um exemplo simples de como usar
a biblioteca Agno para realizar buscas na web.
"""
import sys
import os

# Adicionar o diretório raiz ao path do Python:
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from config.settings import OPENAI_API_KEY
from openai import OpenAI


class WebSearchAgent:
    """
    Agente para realizar buscas na web utilizando a biblioteca Agno.

    Esta classe encapsula a funcionalidade de busca na web através da API OpenAI
    e das ferramentas do DuckDuckGo, permitindo consultas em linguagem natural.
    """

    def __init__(self):
        """
        Inicializa o agente de busca na web.
        """
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.agent = Agent(
            model=OpenAIChat(id="o3-mini"),  # gpt-4o
            tools=[DuckDuckGoTools()],
            markdown=True,
        )

    def search_web(self, query):
        """
        Realiza uma busca na web baseada na consulta fornecida.

        Args:
            query: Consulta em linguagem natural para buscar na web.

        Returns:
            A resposta gerada pelo agente com base na consulta.
        """
        return self.agent.print_response(query, stream=True)


if __name__ == "__main__":
    print("=== Agente de Busca Web Interativo ===")
    print("Digite suas perguntas e receba respostas da web.")
    print("Para sair, digite 'sair', 'exit' ou pressione Ctrl+C")
    print("-" * 50)

    agent = WebSearchAgent()

    try:
        while True:
            query = input("\nDigite sua pergunta: ")

            # Verifica se o usuário quer sair:
            if query.lower() in ["sair", "exit", "quit", "q"]:
                print("Encerrando o programa. Até logo!")
                break

            if not query.strip():
                print("Por favor, digite uma pergunta válida.")
                continue

            print("\nBuscando resposta, por favor aguarde...\n")
            agent.search_web(query)
            print("\n" + "-" * 50)

    except KeyboardInterrupt:
        print("\n\nPrograma interrompido pelo usuário. Até logo!")
