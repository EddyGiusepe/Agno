#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script audio_streaming.py
=========================
Aqui pedidmos ao modelo da OpenAI para contar uma história de 10 segundos, e cuja
resposta será fornecida em streming (no terminal) e também será fornecida um arquivo
de áudio.

O streaming é uma técnica que permite que o modelo gere o áudio enquanto o texto é
exibido no terminal.

Run
---
uv run audio_streaming.py
"""
import os
import base64
import wave
from pathlib import Path
from typing import Iterator
from agno.agent import Agent, RunResponse  # noqa
from agno.models.openai import OpenAIChat

# Configuração do Audio:
SAMPLE_RATE = 24000  # Hz (24kHz)
CHANNELS = 1  # Mono (Mude para 2 se for estéreo)
SAMPLE_WIDTH = 2  # Bytes (16 bits)

# Forneça o agente com o arquivo de áudio e a configuração de áudio e obtenha o resultado como texto + áudio:
agent = Agent(
    model=OpenAIChat(
        api_key=os.getenv("OPENAI_API_KEY"),
        id="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={
            "voice": "alloy",
            "format": "pcm16",
        },  # Apenas pcm16 é suportado com streaming.  PCM16 é um formato de áudio não comprimido que usa 16 bits por amostra. É o formato padrão para áudio digital de alta qualidade
    ),
)

output_stream: Iterator[RunResponse] = agent.run("Diga-me uma história de 10 segundos",
                                                 stream=True
                                                )

filename = "tmp/response_stream.wav"

# Abre o arquivo uma vez no modo binário de adição:
with wave.open(str(filename), "wb") as wav_file:
    wav_file.setnchannels(CHANNELS)
    wav_file.setsampwidth(SAMPLE_WIDTH)
    wav_file.setframerate(SAMPLE_RATE)

    # Itera sobre o áudio gerado:
    for response in output_stream:
        if response.response_audio:
            if response.response_audio.transcript:
                print(response.response_audio.transcript, end="", flush=True)
            if response.response_audio.content:
                try:
                    pcm_bytes = base64.b64decode(response.response_audio.content)
                    wav_file.writeframes(pcm_bytes)
                except Exception as e:
                    print(f"Error decoding audio: {e}")
print()