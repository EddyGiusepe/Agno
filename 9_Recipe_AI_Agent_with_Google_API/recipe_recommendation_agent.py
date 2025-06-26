#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Baseado no Tutorial de "Jie Jenn"

Script recipe_recommendation_agent.py
=====================================
Neste script, criamos um agente de assistência de receitas que utiliza
a API do Google para buscar receitas na web.
O agente é capaz de:
- Buscar receitas na web
- Apresentar as opções de receitas encontradas
- Obter a receita da URL
- Apresentar a receita ao usuário
- Responder perguntas sobre receitas

Run
---
uv run recipe_recommendation_agent.py
"""
import json
from textwrap import dedent
import httpx
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from agno.agent import Agent
from agno.storage.agent.sqlite import SqliteAgentStorage
from agno.models.openai import OpenAIChat
import sys
import os

# Adicionar o diretório raiz ao path do Python:
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import GOOGLE_SEARCH_API_KEY, SEARCH_ENGINE_ID, OPENAI_API_KEY


class SearchResult(BaseModel):
    """
    Representa um único resultado da pesquisa web.
    Contém informações básicas como título, snippet (fragmento) e link do resultado.
    """

    title: str = Field(..., title="Título do resultado da pesquisa")
    snippet: str = Field(..., title="Snippet (fragmento) do resultado da pesquisa")
    link: str = Field(..., title="Link para o resultado da pesquisa")


class SearchResults(BaseModel):
    """
    Coleção de resultados de pesquisa web.
    Encapsula múltiplos resultados individuais em uma única estrutura.
    """

    results: list[SearchResult] = Field(..., title="Lista de resultados da pesquisa")


def get_recipe(url: str) -> str:
    """
    Busca o conteúdo de uma página web e retorna seu texto.
    Args:
        url (str): A URL da página web a ser buscada.
    Returns:
        str: O texto da página web, com quebras de linha, retornos de carro,
        tabulações e múltiplos espaços substituídos por um único espaço.
    Raises:
        Exception: Se houver um erro durante a solicitação HTTP ou análise.
    """
    # print('Acessando URL:', url)
    try:
        response = httpx.get(url, headers={"user-agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.content, "html.parser")
        return (
            soup.get_text()
            .replace("\n", " ")
            .replace("\r", " ")
            .replace("\t", " ")
            .replace("  ", "")
        )
    except Exception as e:
        # print('Exceção:', e)
        return str(e)


def search_google(
    query: str,
    date_restrict: str = None,
    exact_terms: str = None,
    exclude_terms: str = None,
    link_site: str = None,
    site_search: str = None,
    num: int = 10,
    start: int = 1,
) -> list[dict]:
    """
    Google Custom Search API

    Args:
        query (str): Pesquisa da query
        date_restrict (str, optional): Restringe os resultados para URLs com base na data. Os valores suportados incluem:
            d[number]: solicita resultados dos últimos n dias.
            w[number]: solicita resultados dos últimos n semanas.
            m[number]: solicita resultados dos últimos n meses.
            y[number]: solicita resultados dos últimos n anos.
        exact_terms (str, optional): Identifica uma frase que todos os documentos nos resultados da pesquisa devem conter.
        exclude_terms (str, optional): Identifica uma palavra ou frase que não deve aparecer em nenhum dos documentos nos resultados da pesquisa.
        link_site (str, optional): Especifica que todos os resultados da pesquisa devem conter um link para uma URL específica.
        site_search (str, optional): Especifica que todos os resultados da pesquisa devem ser páginas de um site específico.
        num (int, optional): Número de resultados da pesquisa a serem retornados. O padrão é 10. O máximo é 10.
        start (int, optional): O índice do primeiro resultado a ser retornado. O padrão é 1.

    Returns:
        list[dict]: lista de resultados da pesquisa
    """
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_SEARCH_API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
        "num": num,
        "start": start,
        "dateRestrict": date_restrict,
        "exactTerms": exact_terms,
        "excludeTerms": exclude_terms,
        "linkSite": link_site,
        "siteSearch": site_search,
    }
    response = httpx.get(url, params=params)
    if response.status_code == 200:
        # return response.json()
        json_results = response.json()

        lst = []
        for item in json_results.get("items", []):
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            link = item.get("link", "")
            lst.append(SearchResult(title=title, snippet=snippet, link=link))
        return json.dumps(SearchResults(results=lst).model_dump())
    return response.text


def setup_storage(table_name: str, target_dir: str = None) -> SqliteAgentStorage:
    """
    Configura o armazenamento do Agno SQLite agente
    """
    if target_dir is None:
        target_dir = "./agent_sessions.db"

    storage = SqliteAgentStorage(db_file=target_dir, table_name=table_name)
    return storage


def recipe_agent() -> Agent:
    agent_storage = setup_storage(table_name="recipe_agent_sessions")

    agent = Agent(
        name="Agente de Assistência de Receitas",
        model=OpenAIChat(id="gpt-4o-mini", api_key=OPENAI_API_KEY),
        storage=agent_storage,
        description=dedent(
            """
            Você é um agente que foi criado para ajudar o usuário com receitas da web.
            
            Se o usuário perguntar sobre algo não relacionado a receitas, simplesmente responda "Não posso ajudar com isso".
            Sempre responda em português (pt-br).
            
            1. Use a função search_google para encontrar páginas de receitas na web e apresentar ao usuário as opções (nome e URL)
            2. Pergunte ao usuário para escolher uma das opções ou pedir mais opções.
            3. Use a função get_recipe para obter a receita da URL e apresentá-la ao usuário.  
            """
        ),
        instructions=dedent(
            """
            Acompanhe cada recomendação de receita com os seguintes passos:
            
            1. Fase de Análise 📋
            - Entender os ingredientes disponíveis
            - Considerar restrições dietéticas
            - Notar restrições de tempo
            - Considerar o nível de habilidade de cozinha
            - Verificar necessidades de equipamento de cozinha
            
            2. Seleção de Receita 🔍
            - Use Exa para buscar receitas relevantes
            - Garantir que os ingredientes correspondam à disponibilidade
            - Verificar se os tempos de cozimento são apropriados
            - Considerar ingredientes sazonais
            - Verificar avaliações e comentários da receita
            
            3. Informações Detalhadas 📝
            - Título e tipo de culinária da receita
            - Tempo de preparo e cozimento
            - Lista completa de ingredientes com medidas
            - Instruções de cozimento passo a passo
            - Informações nutricionais por porção
            - Nível de dificuldade
            - Tamanho da porção
            - Instruções de armazenamento
            
            4. Extra Features ✨
            - Opções de substituição de ingredientes
            - Erros comuns a evitar
            - Sugestões de pratos
            - Sugestões de vinhos
            - Sugestões de uso de sobras
            - Possibilidades de pré-preparo
            
            Estilo de apresentação:
            - Use formatação markdown clara
            - Apresente ingredientes em uma lista estruturada
            - Numere os passos de cozimento claramente
            - Adicione indicadores de emoji para:
                🌱 Vegetariano
                🌿 Vegano
                ⚡ Sem glúten
                🥜 Contém castanhas
                🕒 Receitas rápidas
            - Inclua dicas para escalonamento de porções
            - Note warnings de alergênios
            - Destacar passos de pré-preparo
            - Sugestões de acompanhamentos"""
        ),
        tools=[search_google, get_recipe],
        add_history_to_messages=True,
        num_history_responses=3,
        debug_mode=False,
        show_tool_calls=True,
    )
    return agent
