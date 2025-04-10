from agno.agent import Agent
from agno.embedder.openai import OpenAIEmbedder
from agno.embedder.ollama import OllamaEmbedder
from agno.knowledge.url import UrlKnowledge
from agno.models.openai import OpenAIChat
from agno.models.groq import Groq
from agno.models.ollama import Ollama
# from agno.vectordb.lancedb import LanceDb, SearchType
from agno.vectordb.pgvector import PgVector, SearchType
import streamlit as st
from agno.run.response import RunEvent, RunResponse
from agno.tools.thinking import ThinkingTools
from agno.tools.python import PythonTools
from agno.tools.knowledge import KnowledgeTools
from dotenv import load_dotenv
import os

load_dotenv()

# Criar uma base de conhecimento contendo informações de uma URL:
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

agno_docs = UrlKnowledge(
    urls=["https://docs.agno.com/llms-full.txt"],

    vector_db=PgVector(
        # uri="tmp/lancedb",
        table_name="agno_docs2",
        db_url=db_url,
        search_type=SearchType.hybrid,
        embedder=OllamaEmbedder(id="nomic-embed-text", dimensions=768),
    ),
)

crewai_docs = UrlKnowledge(
    urls=["https://docs.crewai.com/llms-full.txt"],

    vector_db=PgVector(
        # uri="tmp/lancedb",
        table_name="crewai_docs2",
        db_url=db_url,
        search_type=SearchType.hybrid,
        embedder=OllamaEmbedder(id="nomic-embed-text", dimensions=768),
    ),
)

# Você pode descomentar o método upsert abaixo para carregar os dados:
# crewai_docs.load(upsert=True)
# agno_docs.load(upsert=True)

groq_model = Groq(

    id="meta-llama/llama-4-scout-17b-16e-instruct",
    api_key=os.getenv("GROQ_API_KEY")

)



knowledge_tools = KnowledgeTools(
    knowledge=crewai_docs,
    think=True,
    search=True,
    analyze=True,
    add_few_shot=True,
)

Thinking_tools = ThinkingTools(

    think=True,
    instructions="""
## Instruções Gerais
- Comece usando a ferramenta think...
""",

)

knowledge_agent = Agent(
    model=Groq(id ="meta-llama/llama-4-scout-17b-16e-instruct"),
    # tools=[knowledge_tools],
    tools=[Thinking_tools, knowledge_tools],
    instructions="""Primeiro, utilize as Ferramentas de Pensamento para conduzir um pensamento extenso.
    Em seguida, recupere informações relevantes da base de conhecimento usando a Ferramenta de Conhecimento.
    """,
    show_tool_calls=True,
    markdown=True,
)

# if __name__ == "__main__":
#     # Load the knowledge base, comment after first run
#     # agent.knowledge.load()
#     knowledge_agent.print_response("How do I build multi-agent teams with Agno?", stream=True)

def as_stream(response):
    for chunk in response:
        if isinstance(chunk, RunResponse) and isinstance(chunk.content, str):
            if chunk.event == RunEvent.run_response:
                yield chunk.content

def apply_styles():
    st.markdown("""
    <style>
    hr.divider {
    background-color: white;
    margin: 0;
    }
    </style>
    <hr class='divider' />""", unsafe_allow_html=True)

# Aplicativo Streamlit:
st.title("Aplicação de RAG Agência")

apply_styles()

if st.button("💬 Nova Conversa"):
    st.session_state.messages = []
    st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("O que está acontecendo?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        chunks = knowledge_agent.run(prompt, stream=True)
        response = st.write_stream(as_stream(chunks))
    st.session_state.messages.append({"role": "assistant", "content": response})

# Botão de Salvar:
if st.button("Salvar Conversa"):
    # Implementar a funcionalidade de salvar aqui
    # Por exemplo, você pode salvar o histórico de conversas em um arquivo
    with open("chat_history.txt", "w") as file:
        for message in st.session_state.messages:
            file.write(f"{message['role']}: {message['content']}\n")
    st.success("Histórico de conversas salvo com sucesso!")
