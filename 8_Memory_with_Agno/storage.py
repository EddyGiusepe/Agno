#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script storage.py (Armazenamento de sessão)
===========================================
A memória interna só está disponível durante o ciclo de execução atual. Assim que 
o script termina ou a solicitação é concluída, a memória interna é perdida.

O armazenamento (storage) nos ajuda a salvar sessões e estados do Agente 
em um banco de dados ou arquivo.
Adicionar armazenamento a um Agente é tão simples quanto fornecer um 
storagedriver e o Agno cuida do resto. Você pode usar SQLite, Postgres, 
Mongo ou qualquer outro banco de dados que desejar.

Run
---
uv run storage.py
"""
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.sqlite import SqliteStorage
from rich.pretty import pprint
import sys
import os

# Adicionar o diretório raiz ao path do Python:
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import OPENAI_API_KEY

agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini", api_key=OPENAI_API_KEY),
    session_id="fixed_id_for_demo", # Fixa o id da sessão para continuar a mesma sessão em todos os ciclos de execução
    storage=SqliteStorage(table_name="agent_sessions", db_file="tmp/data.db"), # Armazena as sessões do Agente em um banco de dados SQLite
    add_history_to_messages=True,
    num_history_runs=3,
)
agent.print_response("Olá, me chamo Eddy Giusepe e sou doutor em Física.", stream=True)
agent.print_response("Estudei na UFES e trabalho como cientista de dados.", stream=True)
agent.print_response("Qual foi a minha última pergunta?", stream=True)
agent.print_response("Qual é a capital da França?", stream=True)
agent.print_response("Qual foi a minha última pergunta?", stream=True)
pprint(agent.get_messages_for_session())