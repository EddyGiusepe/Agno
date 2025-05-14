#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script audio_input_output.py
============================
Este script usa o modelo GPT-4o-audio-preview para processar
um arquivo de áudio.
"""
import os
import requests
from agno.agent import Agent
from agno.media import Audio
from agno.models.openai import OpenAIChat
from agno.utils.audio import write_audio_to_file

# Obtenha o arquivo de áudio e converta-o em uma string codificada em base64:
url = "https://openaiassets.blob.core.windows.net/$web/API/docs/audio/alloy.wav"
response = requests.get(url)
response.raise_for_status()
wav_data = response.content

agent = Agent(
    model=OpenAIChat(
        api_key=os.getenv("OPENAI_API_KEY"),
        id="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "sage", "format": "wav"},
        # max_tokens=800, # Limite seus tokens, já que é caro usar modelos de audio.
    ),
    markdown=True,
)

agent.run(
    """Escute esta gravação em inglês (en-us) e descreva o conteúdo 
       em português brasileiro (pt-br). Seja claro e conciso.
    """,
    audio=[Audio(content=wav_data, format="wav")],
)

if agent.run_response.response_audio is not None:
    # Criar o diretório tmp se não existir:
    os.makedirs("tmp", exist_ok=True)
    write_audio_to_file(
        audio=agent.run_response.response_audio.content, filename="tmp/result.wav"
    )
