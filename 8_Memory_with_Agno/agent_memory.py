#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script agent_memory.py
======================
Aqui, vamos criar um agente que usa a memória para armazenar o histórico de conversa.

Run
---
uv run agent_memory.py
"""
from agno.agent import Agent
from agno.models.google.gemini import Gemini
from rich.pretty import pprint
import sys
import os

# Adicionar o diretório raiz ao path do Python:
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import GOOGLE_API_KEY

agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp", api_key=GOOGLE_API_KEY),
    add_history_to_messages=True, # Defina add_history_to_messages=true para adicionar o histórico de chat às mensagens enviadas ao Modelo.
    num_history_responses=3, # Número de respostas históricas a adicionar às mensagens.
    description="""Você é um assistente útil que sempre responde de forma educada, alegre e positiva.
                Ademais, você sempre responde em português do Brasil (pt-BR) e al final da resposta,
                você sempre adiciona um emoji.
                """,
)

agent.print_response("Olá, me chamo Eddy Giusepe e sou doutor em Física.", stream=True)
agent.print_response("Estudei na UFES e trabalho como cientista de dados.", stream=True)
# -*- Criar uma execução:
agent.print_response("Compartilhe uma história de terror de apenas uma sentença", stream=True)
# -*- Imprimir as mensagens na memória:
pprint([m.model_dump(include={"role", "content"}) for m in agent.get_messages_for_session()])
# -*- Perguntar uma pergunta de seguimento que continue a conversa:
agent.print_response("Qual foi a minha primeira mensagem?", stream=True)
# -*- Imprimir as mensagens na memória:
pprint([m.model_dump(include={"role", "content"}) for m in agent.get_messages_for_session()])
