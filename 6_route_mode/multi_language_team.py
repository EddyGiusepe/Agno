#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro



Script multi_language_team.py
=============================
Neste script, criamos uma equipe de agentes que podem responder em diferentes idiomas.
Cada agente é responsável por responder em um idioma específico e o roteador (team) direciona
as perguntas para o agente correto com base no idioma da pergunta.
"""
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.models.deepseek import DeepSeek
from agno.models.mistral.mistral import MistralChat
from agno.models.openai import OpenAIChat
from agno.team.team import Team
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())  # read local .env file


english_agent = Agent(
    name="Agente Inglês",
    role="Você só pode responder em Inglês",
    model=OpenAIChat(id="gpt-4.5-preview"),
    instructions=[
        "Você deve responder apenas em Inglês",
    ],
)

japanese_agent = Agent(
    name="Agente Japonês",
    role="Você só pode responder em Japonês",
    model=DeepSeek(id="deepseek-chat"),
    instructions=[
        "Você deve responder apenas em Japonês",
    ],
)
chinese_agent = Agent(
    name="Agente Chinês",
    role="Você só pode responder em Chinês",
    model=DeepSeek(id="deepseek-chat"),
    instructions=[
        "Você deve responder somente em Chinês",
    ],
)
spanish_agent = Agent(
    name="Agente Espanhol",
    role="Você só pode responder em Espanhol",
    model=OpenAIChat(id="gpt-4.5-preview"),
    instructions=[
        "Você deve responder somente em Espanhol",
    ],
)

french_agent = Agent(
    name="Agente Francês",
    role="Você só pode responder em Francês",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRALAI_API_KEY")),
    instructions=[
        "Você deve responder somente em Francês",
    ],
)

german_agent = Agent(
    name="Agente Alemão",
    role="Você só pode responder em Alemão",
    model=Claude("claude-3-5-sonnet-20241022"),
    instructions=[
        "Você deve responder somente em Alemão",
    ],
)
multi_language_team = Team(
    name="Equipe de Idiomas Múltiplos",
    mode="route",
    model=OpenAIChat("gpt-4.5-preview"),
    members=[
        english_agent,
        spanish_agent,
        japanese_agent,
        french_agent,
        german_agent,
        chinese_agent,
    ],
    show_tool_calls=True,
    markdown=True,
    instructions=[
        "Você é um roteador de idiomas que direciona perguntas para o agente de idioma apropriado.",
        "Se o usuário perguntar em um idioma cujo agente não é um membro da equipe, responda em Inglês com:",
        "'Posso responder apenas em Inglês, Espanhol, Japonês, Francês e Alemão. Por favor, pergunte sua pergunta em um desses idiomas.'",
        "Sempre verifique o idioma da entrada do usuário antes de rotear para um agente.",
        "Para idiomas não suportados, como Italiano, responda em Inglês com a mensagem acima.",
    ],
    show_members_responses=True,
)


#Ask "How are you?" in all supported languages
multi_language_team.print_response(
    "Como você está?", stream=True  # Portuguese
)

#multi_language_team.print_response(
#    "¿Cómo usted está?", stream=True  # Spanish
#)

#multi_language_team.print_response(
#    "你好吗？", stream=True  # Chinese
#)

#multi_language_team.print_response(
#    "お元気ですか?", stream=True  # Japanese
#)

#multi_language_team.print_response(
#    "Comment allez-vous?",
#    stream=True,  # French
#)

#multi_language_team.print_response(
#    "Wie geht es dir?",
#    stream=True,  # German
#)
