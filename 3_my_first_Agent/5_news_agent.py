"""
Agente de notícias baseado no tutorial de "Touseef Shaik"
"""
import asyncio
import nest_asyncio
nest_asyncio.apply()

from duckduckgo_search import DDGS
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
from datetime import datetime
import os
import streamlit as st

# Definir a data atual (formato ano-mês):
current_date = datetime.now().strftime("%Y-%m")

# Inicializar o modelo com sua chave API:
model = OpenAIChatCompletionsModel(
    model="llama-3.3-70b-versatile",
    openai_client=AsyncOpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=os.environ.get("GROQ_API_KEY")
    )
)

# Definir a ferramenta de busca para buscar notícias usando DuckDuckGo:
@function_tool
def get_news_articles(topic):
    st.info(f"Executando a busca de notícias do DuckDuckGo para **{topic}**...")

    # Realizar a busca do DuckDuckGo::
    ddg_api = DDGS()
    results = ddg_api.text(f"{topic} {current_date}", max_results=5)

    if results:
        news_results = "\n\n".join(
            [
                f"**Title:** {result['title']}\n**URL:** {result['href']}\n**Description:** {result['body']}"
                for result in results
            ]
        )
        st.write(news_results)
        return news_results
    else:
        return f"Não foi possível encontrar resultados de notícias para **{topic}**."

# Criar um Agente de Notícias que busca as notícias:
news_agent = Agent(
    name="Assistente de Notícias",
    instructions="Você fornece as últimas notícias sobre um determinado assunto usando a busca do DuckDuckGo.",
    tools=[get_news_articles],
    model=model
)

# Criar um Agente Editor que reescreve as notícias em artigos publicáveis:
editor_agent = Agent(
    name="Assistente de Edição",
    instructions="Reescreva e me dê um artigo de notícias pronto para publicação. Cada história de notícias deve ser em uma seção separada.",
    model=model
)

# Definir o fluxo de trabalho que executa ambos os agentes:
def run_news_workflow(topic):
    st.markdown("### Buscando Artigos de Notícias...")

    # Passo 1: Buscar notícias usando o agente de notícias:
    news_response = Runner.run_sync(
        news_agent,
        f"Get me the news about {topic} on {current_date}"
    )
    raw_news = news_response.final_output

    # Passo 2: Passar as notícias brutas para o agente editor para finalizar o formato:
    st.markdown("### Editando os Artigos de Notícias...")
    edited_news_response = Runner.run_sync(
        editor_agent,
        raw_news
    )
    edited_news = edited_news_response.final_output

    st.success("Artigo de notícias pronto!")
    return edited_news

# Interface principal do Aplicativo Streamlit com uma IU aprimorada:
def main():
    # Barra lateral para instruções e branding:
    st.sidebar.title("Assistente de Notícias")
    st.sidebar.markdown(
        """
        **Bem-vindo ao Assistente de Notícias!**

        1. **Digite um assunto** no campo de entrada.
        2. **Clique em 'Get News'** para buscar e editar as últimas notícias.
        3. Divirta-se com seu artigo de notícias pronto para publicação!
        """
    )
    st.sidebar.image("https://images.unsplash.com/photo-1557683316-973673baf926?auto=format&fit=crop&w=400&q=80", caption="Stay Informed", use_container_width =True)

    # Estilo da página principal:
    st.markdown(
        """
        <style>
        .main-title {
            font-size: 3em;
            font-weight: bold;
            color: #4B8BBE;
            text-align: center;
            margin-bottom: 20px;
        }
        .sub-title {
            font-size: 1.5em;
            text-align: center;
            margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="main-title">News Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Fetch and transform news for your favorite topics!</div>', unsafe_allow_html=True)

    # Campo de entrada e botão:
    topic = st.text_input("Digite um assunto para buscar notícias:", placeholder="e.g., AI, Climate Change, Space Exploration")

    if st.button("Buscar Notícias"):
        if topic:
            st.info(f"Buscando notícias sobre **{topic}**...")
            try:
                with st.spinner("Buscando e editando artigos de notícias..."):
                    news_content = run_news_workflow(topic)
                    st.markdown("### Artigo de Notícias Final:")
                    st.markdown(news_content)
            except Exception as e:
                st.error(f"Erro ao buscar notícias: {str(e)}")
        else:
            st.warning("Por favor, digite um assunto para buscar.")




if __name__ == "__main__":
    main()