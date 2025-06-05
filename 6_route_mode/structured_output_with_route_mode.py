#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script structured_output_with_route_mode.py
============================================
Aqui temos um exemplo de como usar o modo de rotação com saída estruturada.

Este script demonstra:
- Como definir modelos Pydantic para saída estruturada
- Como configurar agentes especializados com ferramentas YFinance
- Como usar o modo "route" para direcionar consultas ao agente mais adequado
- Como lidar com resultados estruturados

Run
---
uv run 6_route_mode/structured_output_with_route_mode.py
"""
import sys
import os

# Adicionar o diretório raiz ao path do Python:
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydantic import BaseModel
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team import Team
from agno.tools.yfinance import YFinanceTools
from config.settings import OPENAI_API_KEY


class StockAnalysis(BaseModel):
    """
    Modelo Pydantic para armazenar análise de ações.
    
    Attributes:
        symbol: Símbolo da ação (ticker) na bolsa.
        company_name: Nome da empresa.
        analysis: Texto contendo a análise do preço da ação.
    """
    symbol: str
    company_name: str
    analysis: str


class CompanyAnalysis(BaseModel):
    """
    Modelo Pydantic para armazenar informações gerais sobre uma empresa.
    
    Attributes:
        company_name: Nome da empresa.
        analysis: Texto contendo análise da empresa baseada em informações e notícias.
    """
    company_name: str
    analysis: str


stock_searcher = Agent(
    name="Pesquisador de Ações",
    model=OpenAIChat("gpt-4o", api_key=OPENAI_API_KEY),
    response_model=StockAnalysis,
    role="Pesquisa informações sobre ações e fornece análise de preço.",
    tools=[
        YFinanceTools(
            stock_price=True, # Habilita a busca de preços de ações
            analyst_recommendations=True, # Habilita a busca de recomendações de analistas
        )
    ],
)

company_info_agent = Agent(
    name="Pesquisador de Informações da Empresa",
    model=OpenAIChat("gpt-4o", api_key=OPENAI_API_KEY),
    role="Pesquisa informações sobre empresas e notícias recentes.",
    response_model=CompanyAnalysis,
    tools=[
        YFinanceTools(
            stock_price=False, # Desabilita a busca de preços (não é o foco deste agente)
            company_info=True, # Habilita a busca de informações da empresa
            company_news=True, # Habilita a busca de notícias da empresa
        )
    ],
)

# No modo "route", o modelo principal (definido em "model") analisa a consulta
# e decide qual agente é mais adequado para responder, roteando a consulta para ele.
team = Team(
    name="Equipe de Pesquisa de Ações",
    mode="route", # Modo de roteamento - envia a consulta para o agente mais adequado
    model=OpenAIChat("gpt-4o", api_key=OPENAI_API_KEY),
    members=[stock_searcher, company_info_agent], # Agentes disponíveis para roteamento
    markdown=True,
)

# Isto deve rotear para o stock_searcher:
response = team.run("Qual é o preço atual da ação da NIVIDA?")
assert isinstance(response.content, StockAnalysis)

print(response.content)
