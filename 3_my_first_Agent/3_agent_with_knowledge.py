#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Agent with Knowledge
====================
Os agentes podem armazenar conhecimento em um banco
de dados vetorial e usá-lo para RAG ou aprendizado
dinâmico de few-shot.

Os agentes da Agno usam o Agentic RAG por padrão,
o que significa que eles pesquisarão em sua base
de conhecimento as informações específicas necessárias
para realizar sua tarefa.

Run
---
uv run 3_agent_with_knowledge.py  (não funcionou!!!)

usei --> python 3_agent_with_knowledge.py (tive que criar o ambiente virtual com o comando: python3 -m venv .venv)
"""
import sys
import os

# Adicionar o diretório raiz ao path do Python:
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.embedder.openai import OpenAIEmbedder
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.vectordb.lancedb import LanceDb, SearchType
from config.settings import OPENAI_API_KEY

agent = Agent(
    model=OpenAIChat(id="o3-mini", api_key=OPENAI_API_KEY),  # o3-mini  gpt-4o
    description="""Você é um chef de cozinha experiente, com vasta experiência em culinária e gastronomia.
                   Se tiver uma pergunta diferente de culinária (ou gastronomia), você deverá pesquisar na web para
                   assim responder à pergunta do usuário.
                   Ademais, você deverá, SEMPRE, responder ao usuário em português brasileiro (pt-br).
                """,
    instructions=[
        "Você pesquisa, APENAS, no seu banco de dados de conhecimento sobre culinária (ou gastronomia) para responder ao usuário.",
        "Se a pergunta não estiver relacionada a culinária (ou gastronomia) ou não for respondida pelo seu banco de dados de conhecimento, você deverá pesquisar na web para responder ao usuário.",
        "Sempre priorize as informações do seu banco de dados de conhecimento sobre culinária (ou gastronomia) para responder ao usuário.",
        "Ademais, você deverá, SEMPRE, responder ao usuário em português brasileiro (pt-br).",
    ],
    knowledge=PDFUrlKnowledgeBase(
        urls=[
            "https://www.colegiosantoantonio.com.br/revista/receita9C.pdf"
        ],  # ["https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
        vector_db=LanceDb(
            uri="tmp/lancedb",
            table_name="receitas",
            search_type=SearchType.hybrid,
            embedder=OpenAIEmbedder(
                id="text-embedding-3-small", api_key=OPENAI_API_KEY
            ),  # text-embedding-3-small     text-embedding-3-large
        ),
    ),
    # tools=[DuckDuckGoTools()], # OBS: Se uso internet não traz o resultado esperado ou melhor dito não traz o conteúdo exato do meu PDF.
    # show_tool_calls=True,
    markdown=True,
)

# Commente depois que o banco de dados de conhecimento for carregado:
if agent.knowledge is not None:
    agent.knowledge.load()

# agent.print_response("Quais são os ingredientes para a preparação do ceviche peruano?", stream=True)
# agent.print_response("Qual é a história do ceviche?", stream=True)
agent.print_response(
    "Quais são os ingredientes para a preparação do Alfajor Peruano 'King Kong'?",
    stream=True,
)
