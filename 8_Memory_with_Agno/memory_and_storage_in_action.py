#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script memory_and_storage_in_action.py
======================================
Este script demonstra como usar a memória e o armazenamento no Agno.

Run
---
uv run memory_and_storage_in_action.py
"""
from agno.agent import Agent
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.models.openai import OpenAIChat
from agno.storage.sqlite import SqliteStorage
from rich.pretty import pprint
import sys
import os

# Adicionar o diretório raiz ao path do Python:
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import OPENAI_API_KEY

# UserId para as memórias:
user_id = "EddyGiusepe"
# Arquivo de banco de dados para memórias e armazenamento:
db_file = "tmp/agent.db"

# Inicializa a memória.v2:
memory = Memory(
    # Use qualquer modelo para criar memórias:
    model=OpenAIChat(id="gpt-4.1", api_key=OPENAI_API_KEY),
    db=SqliteMemoryDb(table_name="user_memories", db_file=db_file),
)
# Inicializa o armazenamento:
storage = SqliteStorage(table_name="agent_sessions", db_file=db_file)

# Inicializa o Agente:
memory_agent = Agent(
    model=OpenAIChat(id="gpt-4.1"),
    memory=memory, # Armazena as memórias em um banco de dados
    enable_agentic_memory=True, # Dá ao Agente a capacidade de atualizar as memórias
    enable_user_memories=True, # OU - Executa o MemoryManager após cada resposta
    storage=storage, # Armazena o histórico de chat no banco de dados
    add_history_to_messages=True, # Adiciona o histórico de chat às mensagens
    num_history_runs=3, # Determina o número de execuções do histórico a adicionar
    read_chat_history=True, # Lê o histórico de chat do banco de dados
    markdown=True, # Formatação Markdown
)

memory.clear()
memory_agent.print_response(
    "Meu nome é Eddy Giusepe e eu gosto de programar em Python e jogar futebol.",
    user_id=user_id,
    stream=True,
    stream_intermediate_steps=True,
)
print("Memórias sobre Eddy Giusepe:")
pprint(memory.get_user_memories(user_id=user_id))

memory_agent.print_response(
    "Eu moro em Lima-Perú, aonde devo me deslocar para um evento de IA?",
    user_id=user_id,
    stream=True,
    stream_intermediate_steps=True,
)
print("Memórias sobre Eddy Giusepe:")
pprint(memory.get_user_memories(user_id=user_id))
