#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script structured_output_with_route_mode.py
============================================
Aqui temos um exemplo de como usar o modo de rotação com saída estruturada.

Run
---
uv run 6_route_mode/structured_output_with_route_mode.py
"""
from pydantic import BaseModel
from typing import List, Optional
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team import Team
from agno.tools.yfinance import YFinanceTools


class StockAnalysis(BaseModel):
    symbol: str
    company_name: str
    analysis: str

class CompanyAnalysis(BaseModel):
    company_name: str
    analysis: str

stock_searcher = Agent(
    name="Pesquisador de Ações",
    model=OpenAIChat("gpt-4o"),
    response_model=StockAnalysis,
    role="Pesquisa informações sobre ações e fornece análise de preço.",
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
        )
    ],
)

company_info_agent = Agent(
    name="Pesquisador de Informações da Empresa",
    model=OpenAIChat("gpt-4o"),
    role="Pesquisa informações sobre empresas e notícias recentes.",
    response_model=CompanyAnalysis,
    tools=[
        YFinanceTools(
            stock_price=False,
            company_info=True,
            company_news=True,
        )
    ],
)

team = Team(
    name="Equipe de Pesquisa de Ações",
    mode="route",
    model=OpenAIChat("gpt-4o"),
    members=[stock_searcher, company_info_agent],
    markdown=True,
)

# Isto deve rotear para o stock_searcher:
response = team.run("Qual é o preço atual da ação da NIVIDA?")
assert isinstance(response.content, StockAnalysis)

print(response.content)
