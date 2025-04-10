#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Agent Data Analyst
==================
This script uses an Agent to analyze a dataset and provide insights.

Run
---
uv run 6_agent_data_analyst.py
"""
import sys
import os
import pandas as pd

# Adicionar o diretório raiz ao path do Python:
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio
from textwrap import dedent
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckdb import DuckDbTools
from config.settings import OPENAI_API_KEY

# Vamos visualizar o arquivo CSV de forma interativa:
df_movies = pd.read_csv(
    "https://agno-public.s3.amazonaws.com/demo_data/IMDB-Movie-Data.csv"
)
df_movies.head()

df_movies.shape
df_movies["Votes"].max()


duckdb_tools = DuckDbTools(
    create_tables=False, export_tables=False, summarize_tables=False
)
duckdb_tools.create_table_from_path(
    path="https://agno-public.s3.amazonaws.com/demo_data/IMDB-Movie-Data.csv",
    table="movies",
)

agent = Agent(
    model=OpenAIChat(id="gpt-4o", temperature=0.0, api_key=OPENAI_API_KEY),
    tools=[duckdb_tools],
    markdown=True,
    show_tool_calls=True,
    additional_context=dedent(
        """\
    Você tem acesso às seguintes tabelas:
    - movies: contém informações sobre filmes do IMDB.
    """
    ),
)

# response = asyncio.run(agent.aprint_response("Qual é a média de avaliação dos filmes?"))
response = asyncio.run(
    agent.aprint_response(
        "Quais são os gêneros de filmes?"
    )  # Quais são os 3 filmes com maior avaliação?
)
