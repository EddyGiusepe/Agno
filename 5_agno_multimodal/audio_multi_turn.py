#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script audio_multi_turn.py
=========================
Este script usa o modelo GPT-4o-audio-preview para gerar aúdios 
de respostas às perguntas do usuário.
Dizemos que o modelo é um modelo de multi-turn, pois ele pode
gerar respostas de várias formas, dependendo das perguntas do
usuário.

Run
---
uv run audio_multi_turn.py
"""
import os
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.utils.audio import write_audio_to_file

agent = Agent(
    model=OpenAIChat(
        api_key=os.getenv("OPENAI_API_KEY"),
        id="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "sage", "format": "wav"},
    ),
    debug_mode=True,
    add_history_to_messages=True,
)

agent.run("Um cachorro de raça golden retriever é um bom cão de família?")
if agent.run_response.response_audio is not None:
    os.makedirs("tmp", exist_ok=True)
    write_audio_to_file(
        audio=agent.run_response.response_audio.content, filename="tmp/answer_1.wav"
    )

agent.run("Por que você disse que eles são leais?")
if agent.run_response.response_audio is not None:
    os.makedirs("tmp", exist_ok=True)
    write_audio_to_file(
        audio=agent.run_response.response_audio.content, filename="tmp/answer_2.wav"
    )
