#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Saída Estruturada com Agno
==========================
Vamos criar um agente de filmes para escrever MovieScript para nós.
"""
import sys
import os
# Adicionar o diretório raiz ao path do Python:
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from typing import List
from rich.pretty import pprint
from pydantic import BaseModel, Field
from agno.agent import Agent, RunResponse
from agno.models.openai import OpenAIChat
from config.settings import OPENAI_API_KEY


class MovieScript(BaseModel):
    setting: str = Field(..., description="Fornece um bom cenário para um filme de sucesso.")
    ending: str = Field(..., description="Final do filme. Se não estiver disponível, forneça um final feliz.")
    genre: str = Field(..., description="Gênero do filme. Se não estiver disponível, selecione ação, thriller ou comédia romântica.")
    name: str = Field(..., description="Dê um nome a este filme")
    characters: List[str] = Field(..., description="Nome dos personagens para este filme.")
    storyline: str = Field(..., description="3 sentenças de história para o filme. Faça-o emocionante!")

# Agente que usa JSON mode:
json_mode_agent = Agent(
    model=OpenAIChat(id="o3-mini", api_key=OPENAI_API_KEY),
    description="Você escreve roteiros de filmes.",
    response_model=MovieScript,
    use_json_mode=True,
)
json_mode_agent.print_response("Perú!")
print("\n")
response_json = json_mode_agent.run("Perú!")
#assistant_content = response_json.messages[2].content
#print(assistant_content)
movie_script = response_json.content
print(movie_script.name)
print(movie_script.storyline)
pprint(movie_script)

print("\n\n")
import json
#assistant_dict = json.loads(assistant_content)
#pprint(assistant_dict["storyline"])


# Agente que usa saída estruturada:
structured_output_agent = Agent(
    model=OpenAIChat(id="o3-mini", api_key=OPENAI_API_KEY),
    description="Você escreve roteiros de filmes.",
    response_model=MovieScript,
)
structured_output_agent.print_response("Perú!")

