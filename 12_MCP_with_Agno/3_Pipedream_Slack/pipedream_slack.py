#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

💬 Pipedream Slack MCP
======================
Este exemplo mostra como usar servidores MCP Pipedream (neste caso do Slack) com Agno Agents.

1. Conecte suas contas Pipedream e Slack: https://mcp.pipedream.com/app/slack
2. Obtenha a URL do servidor MCP Pipedream: https://mcp.pipedream.com/app/slack
3. Defina a variável de ambiente MCP_SERVER_URL para a URL do servidor MCP que você obteve acima
4. Instale as dependências: pip install agno mcp-sdk

Run
---
uv run pipedream_slack.py
"""
import asyncio
import os
import sys
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.mcp import MCPTools
from agno.utils.log import log_exception

# Adiciona o diretório raiz do projeto ao PATH do Python:
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from config.settings import OPENAI_API_KEY, MCP_SERVER_URL

# mcp_server_url = os.getenv("MCP_SERVER_URL")
mcp_server_url = MCP_SERVER_URL


async def run_agent(task: str) -> None:
    try:
        async with MCPTools(
            url=mcp_server_url, transport="sse", timeout_seconds=20
        ) as mcp:
            agent = Agent(
                model=OpenAIChat(id="gpt-4o-mini", api_key=OPENAI_API_KEY),
                tools=[mcp],
                markdown=True,
            )
            await agent.aprint_response(
                message=task,
                stream=True,
            )
    except Exception as e:
        log_exception(f"Erro inesperado: {e}")


async def run_interactive_agent() -> None:
    try:
        async with MCPTools(
            url=mcp_server_url, transport="sse", timeout_seconds=20
        ) as mcp:
            agent = Agent(
                model=OpenAIChat(id="gpt-4o-mini", api_key=OPENAI_API_KEY),
                tools=[mcp],
                markdown=True,
            )
            print("Modo interativo com Slack iniciado. Digite 'sair' para encerrar.")

            while True:
                user_input = input("\nDigite sua instrução para o Slack: ")
                if user_input.lower() == "sair":
                    break

                await agent.aprint_response(
                    message=user_input,
                    stream=True,
                )
    except Exception as e:
        log_exception(f"Erro inesperado: {e}")


if __name__ == "__main__":
    # O agente pode ler canais, usuários, mensagens, etc.
    asyncio.run(run_agent("Mostre-me a última mensagem no canal #comunidade"))

    # Use seu nome real do Slack para isso funcionar!
    # asyncio.run(
    #    run_agent("Envie uma mensagem para <EddyGiusepe> dizendo 'Olá, eu sou seu Agno Agent!'")
    # )

    # Use o modo interativo:
    # asyncio.run(run_interactive_agent())
