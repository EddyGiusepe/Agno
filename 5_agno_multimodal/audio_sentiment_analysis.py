#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script audio_sentiment_analysis.py
==================================
Este script usa o modelo GPT-4o-audio-preview para analisar
o sentimento de um áudio.

Run
---
uv run audio_sentiment_analysis.py
"""
import requests
from agno.agent import Agent
from agno.media import Audio
from agno.models.google import Gemini
import psycopg

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())  # read local .env file

db_url = "postgresql://ai:ai@localhost:5432/ai"

agent = Agent(
    model=Gemini(
        id="gemini-2.0-flash-exp"
    ),  # api_key=os.getenv("GEMINI_API_KEY")  ou api_key=os.getenv("GOOGLE_API_KEY")
    add_history_to_messages=True,
    #reasoning=True, # Quando uso isto, o resulatdo é vazio
    markdown=True,
    save_response_to_file="sentiment_analysis_audio.md",
)

url = "https://agno-public.s3.amazonaws.com/demo_data/sample_conversation.wav"

response = requests.get(url)
audio_content = response.content

# Faça uma análise de sentimentos desta conversa em áudio. Use speaker A, speaker B para
# identificar os falantes (interlocutores).

agent.print_response(
    """Faça uma análise de sentimentos desta conversa em áudio. Use speaker A, speaker B para 
       identificar os falantes (interlocutores).
    """,
    audio=[Audio(content=audio_content)],
    stream=True,
)

agent.print_response(
    "O que mais você pode me contar sobre esta conversa em áudio?",
    stream=True,
)

# Lê o conteúdo do arquivo markdown gerado
with open("sentiment_analysis_audio.md", "r") as file:
    texto_completo = file.read()

# Simplifica o modelo de dados (apenas texto, sem classificação de sentimento)
conn = psycopg.connect(db_url)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS audio_analyses (id SERIAL PRIMARY KEY, análise TEXT, data_criação TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
cursor.execute("INSERT INTO audio_analyses (análise) VALUES (%s)", (texto_completo,))
conn.commit()
conn.close()


