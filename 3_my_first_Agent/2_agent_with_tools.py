#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Agent with Tools
================
Esse agente básico obviamente inventará uma história.
Vamos dar a ele uma ferramenta para pesquisar na web.

Run
---
uv run 2_agent_with_tools.py
"""
import sys
import os

# Adicionar o diretório raiz ao path do Python:
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from config.settings import OPENAI_API_KEY


class ReporterAgent:
    def __init__(self, api_key: str, model_id: str = "o3-mini", max_retries: int = 2):
        """
        Inicializa um agente repórter que pode buscar e reportar notícias.

        Args:
            api_key (str): Chave de API do OpenAI
            model_id (str): ID do modelo a ser usado
            max_retries (int): Número máximo de tentativas para chamadas API
        """
        self.agent = Agent(
            model=OpenAIChat(id=model_id, api_key=api_key, max_retries=max_retries),
            description="""Você é um repórter com muita experiência.
                           Você fornece notícias factuais e atualizadas
                           sobre algum país.
                        """,
            tools=[DuckDuckGoTools()],
            show_tool_calls=True,
            markdown=True,
        )

    def search_news(self, query: str, stream: bool = True):
        """
        Busca informações sobre o tópico solicitado.

        Args:
            query (str): Pergunta ou tópico sobre o qual buscar informações.
            stream (bool): Se deve mostrar a resposta em streaming.

        Returns:
            A resposta do agente.
        """
        return self.agent.print_response(query, stream=stream)

    def country_to_be_searched(self, country: str, stream: bool = True):
        """
        Busca notícias específicas sobre um país.

        Args:
            country (str): Nome do país a ser pesquisado.
            stream (bool): Se deve mostrar a resposta em streaming.

        Returns:
            A resposta do agente com notícias sobre o país
        """
        query = f"Conte-me sobre o que está acontecendo no(a) {country}."
        return self.search_news(query, stream=stream)


if __name__ == "__main__":
    reporter = ReporterAgent(api_key=OPENAI_API_KEY)
    reporter.country_to_be_searched("Peru", stream=True)
