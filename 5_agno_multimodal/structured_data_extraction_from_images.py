#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script structured_data_extraction_from_images.py
================================================
Este script usa o modelo GPT-4o para extrair informações específicas de uma tabela
contida em uma imagem de desenho técnico.
A saída é estruturada em formato JSON, utilizando Pydantic.

Run
---
uv run structured_data_extraction_from_images.py

Exemplo de saída:

TabelaDesenhoTecnico(
│   nome_universidade='UFPB - Universidade Federal da Paraíba',
│   nome_professor='Prof. Frederico',
│   escala_desenho='2:1',
│   data='20/11/2000',
│   nome_aluno='Fábio',
│   codigo_materia='9920133'
)
"""
import sys
import os

# Adicionar o diretório raiz ao path do Python:
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agno.agent import Agent
from agno.media import Image
from agno.models.openai import OpenAIChat
from pydantic import BaseModel, Field
from rich.pretty import pprint
from config.settings import OPENAI_API_KEY


class TabelaDesenhoTecnico(BaseModel):
    nome_universidade: str = Field(
        ..., description="O nome da universidade dentro da tabela"
    )
    nome_professor: str = Field(
        ...,
        description="Nome do professor dentro da tabela, representado com o campo 'Prof.'",
    )
    escala_desenho: str = Field(
        ...,
        description="Escala do desenho dentro da tabela, representada com o campo 'Esc.'",
    )
    data: str = Field(
        ..., description="Campo Data dentro da tabela, representado com o campo 'Data'"
    )
    nome_aluno: str = Field(
        ..., description="Nome do aluno dentro da tabela, representado com o campo 'Aluno'"
    )
    codigo_materia: str = Field(
        ...,
        description="Código da matéria dentro da tabela, representado com o campo 'Mat.'",
    )


agent = Agent(
    model=OpenAIChat(
        api_key=OPENAI_API_KEY, temperature=0.0, id="gpt-4.1-nano"
    ),  # "gpt-4o" "gpt-4.1-2025-04-14"    gpt-4.1-mini
    response_model=TabelaDesenhoTecnico,
)

response = agent.run(
    """Extraia as informações/Campos solicitados da tabela a qual se encontra na imagem fornecida. 
       Identifique corretamente o nome da universidade, nome do professor (campo Prof.),
       escala do desenho (campo Esc.), data (campo Data), nome do aluno (campo Aluno) e código da matéria (campo Mat.).
       Ademais, sempre forneça a resposta em português brasileiro (pt-br).
       Faça essa extração com muito cuidado, sempre pensando e verificando, de tal maneira que sejam informações factuais.
    """,
    images=[
        Image(
            filepath="/home/eddygiusepe/1_github/Agno/5_agno_multimodal/img/image_Desenho_tecnico.jpeg"
        )
    ],
    stream=True,
)

pprint(response.content)
