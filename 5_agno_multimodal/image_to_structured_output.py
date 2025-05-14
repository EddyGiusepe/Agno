#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script image_to_structured_output.py
====================================
Este script usa o modelo GPT-4o para criar um filme baseado em uma imagem.
A saída ou resposta é um filme com o nome, cenário, personagens e história.
Ademais, a saída é estruturada, devido ao uso do Pydantic.

Run
---
uv run image_to_structured_output.py
"""
from typing import List
import os
from agno.agent import Agent
from agno.media import Image
from agno.models.openai import OpenAIChat
from pydantic import BaseModel, Field
from rich.pretty import pprint


class MovieScript(BaseModel):
    name: str = Field(..., description="Dê um nome para este filme")
    setting: str = Field(
        ..., description="Forneça um bom cenário para um filme de sucesso."
    )
    characters: List[str] = Field(
        ..., description="Nome dos personagens para este filme."
    )
    storyline: str = Field(
        ..., description="3 sentenças de história para o filme. Faça-o emocionante!"
    )


agent = Agent(
    model=OpenAIChat(api_key=os.getenv("OPENAI_API_KEY"), id="gpt-4o"),
    response_model=MovieScript,
)

response = agent.run(
    "Escreva um filme sobre esta imagem",
    images=[
        Image(
            url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Midday_at_Machu_Picchu.jpg/640px-Midday_at_Machu_Picchu.jpg"
            #url="https://upload.wikimedia.org/wikipedia/commons/0/0c/GoldenGateBridge-001.jpg"
        )
    ],
    stream=True,
)

pprint(response.content)
