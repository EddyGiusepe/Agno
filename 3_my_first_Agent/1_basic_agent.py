#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Basic Agent
===========
The simplest Agent is just an Inference task, no tools, no memoery, no knowledge.

Run
---
uv run 1_basic_agent.py
"""
import sys
import os

# Adicionar o diretório raiz ao path do Python:
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from config.settings import OPENAI_API_KEY
from pydantic import BaseModel, Field


class NewsReporter(BaseModel):
    title: str = Field(..., description="Título da notícia")
    content: str = Field(..., description="Conteúdo da notícia")


agent = Agent(
    model=OpenAIChat(id="o3-mini", api_key=OPENAI_API_KEY),
    description="""Você é um repórter de notícias entusiasmado
                   com uma habilidade para contar histórias!
                """,
    response_model=NewsReporter,
    # markdown=True,
    use_json_mode=True,
)

# response = agent.print_response("Conte-me sobre uma notícia do Perú.", stream=True)
response = agent.run("Conte-me sobre uma notícia do Perú.")
print(response.content)
