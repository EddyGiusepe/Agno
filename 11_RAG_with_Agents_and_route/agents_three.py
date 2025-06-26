#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro
"""
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team.team import Team
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.knowledge.json import JSONKnowledgeBase
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.embedder.openai import OpenAIEmbedder
from config.settings import OPENAI_API_KEY

agent_detran_df = Agent(
    name="Especialista do Detran do Distrito Federal (DF)",
    role="Especialista em fornecer informações precisas e atualizadas sobre documentação, processos e serviços do Detran DF",
    model=OpenAIChat(id="gpt-4o", temperature=0.0, api_key=OPENAI_API_KEY),
    instructions=[
        "Você é especialista em informações oficiais do Detran do Distrito Federal (DF)",
        "Responda apenas com base nas informações contidas nos documentos oficiais do Detran DF fornecidos.",
        "Se a pergunta não for relacionada ao Detran DF, responda educadamente: 'Desculpe, não encontrei informações sobre a sua pergunta nos documentos do Detran DF.'",
        "Sempre cite a fonte do documento oficial do Detran DF ao fornecer a resposta, incluindo página ou seção, se possível.",
        "Se a informação não estiver clara nos documentos, informe que não há dados suficientes para responder.",
        "Mantenha as respostas claras, objetivas e em linguagem acessível para o público geral.",
        "Sempre responda em português brasileiro (pt-br).",
    ],
    knowledge=PDFKnowledgeBase(
        path="/home/karinag/1_GitHub/Agno/7_RAG_with_Agents_and_route/data/DETRAN-DF/detran_habilitacao.pdf",
        vector_db=LanceDb(
            uri="tmp/lancedb_detran_df",
            table_name="detran_df_docs",
            search_type=SearchType.hybrid,
            embedder=OpenAIEmbedder(id="text-embedding-3-large"),
        ),
    ),
    show_tool_calls=True,
    markdown=True,
)


cleaning_service_agent_df = Agent(
    name="Especialista em fornecer informações sobre o Serviço de Limpeza Urbana (SLU) do Distrito Federal (DF)",
    role="""Especialista em fornecer informações precisas, atualizadas e oficiais sobre o Serviço de Limpeza Urbana
            do Distrito Federal (DF), incluindo serviços, atendimento, legislação e canais de comunicação.""",
    model=OpenAIChat(id="gpt-4o", temperature=0.0, api_key=OPENAI_API_KEY),
    instructions=[
        "Você é especialista em informações oficiais do Serviço de Limpeza Urbana do Distrito Federal (DF)",
        "Responda apenas com base nas informações contidas nos documentos oficiais do Serviço de Limpeza Urbana do Distrito Federal (DF) fornecidos.",
        "Se a pergunta não for sobre o Serviço de Limpeza Urbana do Distrito Federal (DF), responda educadamente: 'Desculpe, não encontrei informações sobre a sua pergunta nos documentos do Serviço de Limpeza Urbana do Distrito Federal (DF).'",
        "Sempre cite a fonte do documento oficial ao fornecer a resposta, mencionando a página, seção ou tópico, se possível.",
        "Se a informação não estiver clara nos documentos, informe que não há dados suficientes para responder.",
        "Mantenha as respostas claras, objetivas e em linguagem acessível para o público geral.",
        "Se a pergunta envolver contatos, canais de atendimento ou horários, forneça essas informações conforme o documento.",
        "Sempre responda em português brasileiro (pt-br).",
    ],
    knowledge=PDFKnowledgeBase(  
        path="/home/karinag/1_GitHub/Agno/7_RAG_with_Agents_and_route/data/SERVICO-LIMPEZA-URBANA-DF/slu_2024_DF.pdf",
        vector_db=LanceDb(
            uri="tmp/lancedb_slu_df",
            table_name="slu_df_docs",
            search_type=SearchType.hybrid,
            embedder=OpenAIEmbedder(id="text-embedding-3-large"),
        ),
    ),
    show_tool_calls=True,
    markdown=True,
)


agent_health_secretary_df = Agent(
    name="Especialista em fornecer informações sobre a Secretaria de Saúde do Distrito Federal (DF)",
    role="""Especialista em fornecer informações precisas, atualizadas e oficiais sobre a Secretaria de Saúde do Distrito Federal (DF),
            incluindo serviços, atendimento, legislação, documentos, campanhas de saúde pública e canais de comunicação.""",
    model=OpenAIChat(id="gpt-4o", temperature=0.0, api_key=OPENAI_API_KEY),
    instructions=[
        "Você é especialista em informações oficiais da Secretaria de Saúde do Distrito Federal (DF)",
        "Responda apenas com base nas informações contidas nos documentos oficiais da Secretaria de Saúde do Distrito Federal (DF) fornecidos.",
        "Se a pergunta não for sobre a Secretaria de Saúde do Distrito Federal (DF), responda educadamente: 'Desculpe, não encontrei informações sobre a sua pergunta nos documentos da Secretaria de Saúde do Distrito Federal (DF).'",
        "Sempre cite a fonte do documento oficial ao fornecer a resposta, mencionando a página, seção, tópico ou nome do documento, se possível.",
        "Se a informação não estiver clara nos documentos, informe que não há dados suficientes para responder.",
        "Mantenha as respostas claras, objetivas e em linguagem acessível para o público geral.",
        "Se a pergunta envolver contatos, canais de atendimento ou horários, forneça essas informações conforme o documento.",
        "Sempre responda em português brasileiro (pt-br).",
    ],
    knowledge=PDFKnowledgeBase(
        path="/home/karinag/1_GitHub/Agno/7_RAG_with_Agents_and_route/data/SES-DF/secretaria_saude_df.pdf",
        vector_db=LanceDb(
            uri="tmp/lancedb_secretaria_saude_df",
            table_name="secretaria_saude_df_docs",
            search_type=SearchType.hybrid,
            embedder=OpenAIEmbedder(id="text-embedding-3-large"),
        ),
    ),
    show_tool_calls=True,
    markdown=True,
)

# ✅ CARREGAR OS DADOS (MUITO IMPORTANTE!)
def setup_knowledge_bases():
    print("🔄 Carregando base de conhecimento do Detran DF...")
    if agent_detran_df.knowledge is not None:
        agent_detran_df.knowledge.load(upsert=True)
    
    print("🔄 Carregando base de conhecimento do Serviço de Limpeza Urbana DF...")
    if cleaning_service_agent_df.knowledge is not None:
        cleaning_service_agent_df.knowledge.load(upsert=True)
    
    print("🔄 Carregando base de conhecimento da Secretaria de Saúde DF...")
    if agent_health_secretary_df.knowledge is not None:
        agent_health_secretary_df.knowledge.load(upsert=True)
    
    print("✅ Todas as bases de conhecimento foram carregadas!")

multi_data_team = Team(
    name="Equipe de Fontes Múltiplas",
    mode="route",
    model=OpenAIChat("gpt-4o", temperature=0.0, api_key=OPENAI_API_KEY),
    members=[
        agent_detran_df,
        cleaning_service_agent_df,
        agent_health_secretary_df,
    ],
    show_tool_calls=True,
    markdown=True,
    instructions=[
        "Você é um roteador inteligente que direciona perguntas para o agente especializado mais adequado.",
        "Analise cuidadosamente a pergunta do usuário para identificar se ela se refere a:",
        "- Detran DF: perguntas sobre habilitação, documentação, trânsito e serviços do Detran do Distrito Federal.",
        "- Serviço de Limpeza Urbana DF: perguntas sobre coleta de resíduos, varrição, limpeza pública e serviços do SLU DF.",
        "- Secretaria de Saúde DF: perguntas sobre serviços de saúde, campanhas, atendimento e informações da Secretaria de Saúde do DF.",
        "Se a pergunta mencionar explicitamente uma dessas três áreas, direcione para o agente correspondente.",
        "Se a pergunta não for clara ou abranger mais de uma área, peça ao usuário para especificar, respondendo: "
        "'Posso responder apenas sobre Detran DF, Serviço de Limpeza Urbana DF ou Secretaria de Saúde DF. "
        "Por favor, poderia especificar sobre qual dessas áreas você deseja informações?'",
        "Evite enviar a pergunta para mais de um agente ao mesmo tempo para otimizar respostas e evitar confusão.",
        "Se a pergunta for genérica ou fora do escopo, responda com a mesma mensagem de solicitação de especificação.",
        ],
    show_members_responses=True,
)

if __name__ == "__main__":
    setup_knowledge_bases()
    
    # Teste:
    multi_data_team.print_response(
        "O que é a Secretaria de Saúde do Distrito Federal?", stream=True
    )
