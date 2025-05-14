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
"""
from typing import Optional
import os
from agno.agent import Agent
from agno.media import Image
from agno.models.openai import OpenAIChat
from pydantic import BaseModel, Field
from rich.pretty import pprint


class TabelaDesenhoTecnico(BaseModel):
    nome_universidade: str = Field(..., description="O nome da universidade que aparece na tabela")
    nome_professor: str = Field(..., description="Nome do professor que está na tabela, representado como 'Prof.'")
    escala_desenho: str = Field(..., description="Escala do desenho que está na tabela, representada como 'Esc.'")
    data: str = Field(..., description="Data que aparece na tabela, representada como 'Data'")
    nome_aluno: str = Field(..., description="Nome do aluno encontrado na tabela")
    codigo_materia: str = Field(..., description="Código da matéria, representado como 'Mat.'")


agent = Agent(
    model=OpenAIChat(api_key=os.getenv("OPENAI_API_KEY"), id="gpt-4.1-2025-04-14"), # "gpt-4o" "gpt-4.1-2025-04-14"  
    response_model=TabelaDesenhoTecnico,
)

response = agent.run(
    """Extraia as informações/Campos solicitados da tabela que se encontra na imagem fornecida. 
       Identifique corretamente o nome da universidade, nome do professor (Prof.),
       escala do desenho (Esc.), data, nome do aluno e código da matéria (Mat.).
       Ademais, sempre forneça a resposta em português brasileiro (pt-br).
       Faça essa extração com muito cuidado, sempre pensando e verificando, de tal maneira que sejam informações factuais.
    """,
    images=[
        Image(
            filepath="/home/karinag/1_GitHub/Agno/5_agno_multimodal/img/image_Desenho_tecnico.jpeg"
        )
    ],
    stream=True,
)

pprint(response.content) 