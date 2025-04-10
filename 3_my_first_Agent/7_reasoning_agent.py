#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Reasoning Agent
===============


Run
---
uv run 7_reasoning_agent.py
"""
import sys
import os
# Adicionar o diretório raiz ao path do Python:
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio
from agno.agent import Agent
from agno.cli.console import console
from agno.models.openai import OpenAIChat
from config.settings import OPENAI_API_KEY
task = "Entre 9.11 e 9.9, qual é o maior?"

regular_agent = Agent(
    model=OpenAIChat(id="gpt-4o", temperature=0.0, api_key=OPENAI_API_KEY),
    markdown=True
)

reasoning_agent = Agent(
    model=OpenAIChat(id="gpt-4o", temperature=0.0, api_key=OPENAI_API_KEY),

    reasoning=True,
    markdown=True,
)

console.rule("[bold green]Regular Agent[/bold green]")
asyncio.run(regular_agent.aprint_response(task, stream=True))

print("-" * 100)

console.rule("[bold yellow]Reasoning Agent[/bold yellow]")
asyncio.run(
    reasoning_agent.aprint_response(task, stream=True, show_full_reasoning=True)
)
