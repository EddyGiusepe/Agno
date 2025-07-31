#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script filesystem_agent.py
==========================
Este script implementa um agente de sistema de arquivos que
utiliza o MCP (Model Context Protocol) para acessar o sistema de arquivos.

Run:
----
uv run filesystem_agent.py
"""
import asyncio
from pathlib import Path
from textwrap import dedent
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.mcp import MCPTools  # Classe que conecta o agente aos servidores MCP
from mcp import StdioServerParameters
import sys
import os

# Adiciona o diretório raiz do projeto ao PATH do Python:
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from config.settings import OPENAI_API_KEY


async def run_agent(message: str) -> None:
    """Execute o agente do sistema de arquivos com a mensagem fornecida."""

    file_path = str(
        Path(__file__).parent.parent.parent
    )  #  Diretório raiz Agno (onde está o LICENSE)

    # Servidor MCP para acessar o sistema de arquivos (via `npx`):
    async with MCPTools(  # MCPTools automaticamente inicia um servidor MCP filesystem
        f"npx -y @modelcontextprotocol/server-filesystem {file_path}"  # Usa npx para executar o servidor oficial @modelcontextprotocol/server-filesystem
    ) as mcp_tools:  # O servidor é limitado ao diretório file_path # Não precisa configurar client/server separadamente!
        agent = Agent(
            model=OpenAIChat(id="gpt-4o", api_key=OPENAI_API_KEY),
            tools=[mcp_tools],
            instructions=dedent(
                """\
                Você é um assistente de sistema de arquivos. Ajude os usuários a explorar arquivos e diretórios.

                - Navegue pelo sistema de arquivos para responder perguntas
                - Use a ferramenta list_allowed_directories para encontrar diretórios que você pode acessar
                - Forneça um contexto claro sobre os arquivos que você examina
                - Use títulos para organizar suas respostas
                - Seja conciso e foco em informações relevantes\
            """
            ),
            markdown=True,
            show_tool_calls=True,
        )

        # Executa o agente:
        await agent.aprint_response(message, stream=True)


# Exemplo de uso:
if __name__ == "__main__":
    # Exemplo básico - explorando o licenciamento deste projeto ATUAL --> Agno:
    asyncio.run(run_agent("Qual é o licenciamento deste projeto?"))
