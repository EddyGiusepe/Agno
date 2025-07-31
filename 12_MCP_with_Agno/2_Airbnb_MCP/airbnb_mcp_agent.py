#! /usr/bin/env python3
"""
Senior Data Scientist.:  Dr. Eddy Giusepe Chirinos Isidro

🏠 MCP Airbnb Agent - Busca por listagens do Airbnb!

Script airbnb_mcp_agent.py
==========================
Este script implementa um agente que usa MCP e gpt-4o
para buscar listagens do Airbnb.

Run:
---
uv run airbnb_mcp_agent.py
"""
import asyncio

from agno.agent import Agent
from agno.models.openai.chat import OpenAIChat
from agno.tools.mcp import MCPTools
import sys
import os

# Adiciona o diretório raiz do projeto ao PATH do Python:
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from config.settings import OPENAI_API_KEY


async def run_mcp_agent(message: str):
    try:
        # Usa MCPTools como context manager:
        async with MCPTools(
            "npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt", timeout_seconds=30
        ) as mcp_tools:
            # Usa as tools MCP com um Agente:
            agent = Agent(
                model=OpenAIChat(id="gpt-4o", api_key=OPENAI_API_KEY),
                tools=[mcp_tools],
                markdown=True,
            )
            await agent.aprint_response(message)
    except Exception as e:
        print(f"Erro ao executar o agente: {e}")


if __name__ == "__main__":
    asyncio.run(
        run_mcp_agent(
            "Mostre-me apenas 3 apartamentos em Vitória-ES Jardim da Penha (perto da UFES), para 2 pessoas."
        )
    )
