#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro
"""
import sys
import os
# Adicionar o diretório raiz ao path do Python:
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools
from config.settings import ANTHROPIC_API_KEY

agent = Agent(
    model=Claude(id="claude-3-7-sonnet-latest", api_key=ANTHROPIC_API_KEY),
    tools=[
        ReasoningTools(add_instructions=True),
        YFinanceTools(stock_price=True,
                      analyst_recommendations=True,
                      company_info=True,
                      company_news=True
                      ),
    ],
    instructions=[
        "Use tabelas para exibir dados",
        "Apenas saída do relatório, sem outro texto",
    ],
    markdown=True,
    save_response_to_file="relatorio_nvidia_finance.md"
)

response = agent.print_response("Escreva um relatório da Tesla neste 2025.",
                     stream=True,
                     show_full_reasoning=True,
                     stream_intermediate_steps=True
                    )
response
