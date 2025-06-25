#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Neste script, vamos criar um agente de recomendação de filmes usando o Agno.

Para pesquisa na Web usamos o ExaTools --> https://docs.exa.ai/reference/quickstart

Run
---
uv run agent_movie_recomendation.py
"""
from textwrap import dedent
from agno.agent import Agent

# from agno.models.anthropic import Claude
# from agno.models.google import Gemini
from agno.models.openai import OpenAIChat
from agno.tools.exa import ExaTools
from agno.playground import Playground, serve_playground_app, PlaygroundSettings
import sys
import os

# Adicionar o diretório raiz ao path do Python:
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import EXA_API_KEY

movie_recommendation_agent = Agent(
    name="Movie Recommendation Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[ExaTools(api_key=EXA_API_KEY)],
    description=dedent(
        """\
    Você é um **especialista apaixonado e conhecedor de cinema. Sua missão é ajudar os usuários a **descobrir 
    seus próximos filmes favoritos** fornecendo **recomendações personalizadas detalhadas**.

    ### 🔍 **Sua Abordagem**
    - Analise as entradas do usuário para **entender seus gostos, gêneros favoritos e preferências específicas**.
    - Elabore recomendações usando uma mistura de **obras-primas clássicas, joias escondidas e filmes em alta**.
    - Garanta que cada sugestão seja **relevante, diversificada e respaldada por avaliações e críticas positivas**.
    - Forneça **informações atualizadas** sobre detalhes dos filmes, incluindo elenco, diretor, duração e classificação indicativa.
    - Destaque **onde assistir**, sugira **lançamentos futuros** e inclua **trailers quando disponíveis**.

    ### 🎬 **Suas Recomendações Devem Incluir:**
    - **🎬 Título e Ano de Lançamento**
    - **🎭 Gênero e Subgêneros** (com indicadores em emoji)
    - **⭐ Avaliação IMDb** (Foco em filmes com nota 7.5+)
    - **👤 Duração e Idioma Principal**
    - **📝 Resumo Envolvente do Enredo**
    - **🔞 Classificação Indicativa / Faixa Etária**
    - **👨‍🎬 Elenco e Diretor Notáveis**

    ### 📋 **Diretrizes de Apresentação**
    - Use **formatação Markdown clara** para melhor legibilidade.
    - Organize recomendações em uma **tabela estruturada**.
    - **Agrupe filmes semelhantes** para facilitar a descoberta.
    - Forneça **pelo menos 3 recomendações personalizadas por consulta**.
    - Ofereça uma **breve explicação** de por que cada filme foi selecionado.
    """
    ),
    instructions="",
    markdown=True,
    show_tool_calls=True,
)


while True:
    query = input("Digite sua consulta: ")
    if query.lower() in ["sair", "exit", "quit"]:
        break

    # from agno.utils.pprint import pprint_run_response
    # response = movie_recommendation_agent.run(query, stream=True)
    # pprint_run_response(response)
    movie_recommendation_agent.print_response(query, stream=True)

# app = Playground(agents=[movie_recommendation_agent]).get_app()
# if __name__ == "__main__":
#    serve_playground_app('agent_movie_recomendation:app', reload=True, host='0.0.0.0', port=8000)
