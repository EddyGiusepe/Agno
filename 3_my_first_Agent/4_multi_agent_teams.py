#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Multi Agent Teams
=================
Os agentes funcionam melhor quando têm um propósito singular, 
um escopo estreito e um pequeno número de ferramentas. Quando 
o número de ferramentas cresce além do que o modelo de linguagem 
pode manipular ou as ferramentas pertencem a categorias diferentes, 
use uma equipe de agentes para distribuir a carga.

Run
---
uv run 4_multi_agent_teams.py ou python 4_multi_agent_teams.py
"""
import sys
import os

# Adicionar o diretório raiz ao path do Python:
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from config.settings import OPENAI_API_KEY

web_agent = Agent(
    name="Agente de Pesquisa na Web",
    role="Pesquisa na web para informações",
    model=OpenAIChat(id="o3-mini", api_key=OPENAI_API_KEY),
    tools=[DuckDuckGoTools()],
    instructions="Sempre incluir fontes",
    show_tool_calls=True,
    markdown=True,
)

finance_agent = Agent(
    name="Agente de Análise Financeira",
    role="Obter dados financeiros",
    model=OpenAIChat(id="o3-mini", api_key=OPENAI_API_KEY),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True)],
    instructions="Usar tabelas para exibir dados",
    show_tool_calls=True,
    markdown=True,
)

agent_team = Agent(
    team=[web_agent, finance_agent],
    model=OpenAIChat(id="o3-mini", api_key=OPENAI_API_KEY),
    instructions=["Sempre incluir fontes", "Usar tabelas para exibir dados"],
    show_tool_calls=True,
    markdown=True,
)

agent_team.print_response("Qual é a visão do mercado e o desempenho financeiro das empresas de semicondutores de IA?", stream=True)
