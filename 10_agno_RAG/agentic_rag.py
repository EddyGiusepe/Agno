#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script agentic_rag.py
=====================
"""
"""
Opções de Chunking
==================
1. Document Chunking (Baseado na estrutura do documento)

* from agno.document.chunking.document import DocumentChunking ---> chunking_strategy=DocumentChunking()

2. Fixed Size Chunking (Tamanho fixo)

* from agno.document.chunking.fixed import FixedSizeChunking ---> chunking_strategy=FixedSizeChunking()

3. Semantic Chunking (Baseado em similaridade semântica)

* from agno.document.chunking.semantic import SemanticChunking ---> chunking_strategy=SemanticChunking()

4. Recursive Chunking (Divisão recursiva)

* from agno.document.chunking.recursive import RecursiveChunking ---> chunking_strategy=RecursiveChunking()

Qual estratégia escolher?
* Document Chunking: Melhor para documentos estruturados (com parágrafos e seções bem definidas)
* Fixed Size Chunking: Útil quando você quer controle preciso sobre o tamanho dos chunks
* Semantic Chunking: Ideal para preservar o contexto semântico, mantendo conteúdo relacionado junto
* Recursive Chunking: Boa opção geral que aplica estratégias de divisão de forma recursiva

Para o nosso caso com documentos do DETRAN DF Habilitação, vamos começar com Document Chunking 
ou Semantic Chunking, pois eles preservam melhor o contexto e a estrutura do documento.
"""

from agno.agent import Agent
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.document.chunking.document import DocumentChunking
from agno.embedder.openai import OpenAIEmbedder
#from agno.embedder.cohere import CohereEmbedder
from agno.knowledge.url import UrlKnowledge
from agno.models.anthropic import Claude
#from agno.reranker.cohere import CohereReranker
from agno.vectordb.lancedb import LanceDb, SearchType
import sys
import os

# Adicionar o diretório raiz ao path do Python:
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import OPENAI_API_KEY, ANTHROPIC_API_KEY

# Criar uma base de conhecimento:
knowledge_base = PDFKnowledgeBase(
        path="/home/karinag/1_GitHub/Agno/7_RAG_with_Agents_and_route/data/DETRAN-DF/detran_habilitacao.pdf",
        vector_db=LanceDb(
            uri="tmp/lancedb_detran_df",
            table_name="detran_df_docs",
            search_type=SearchType.hybrid,
            embedder=OpenAIEmbedder(id="text-embedding-3-large", api_key=OPENAI_API_KEY),
        ),
        chunking_strategy=DocumentChunking(),
    )

agent = Agent(
    model=Claude(id="claude-3-7-sonnet-latest", api_key=ANTHROPIC_API_KEY),
    # O RAG Agentic é habilitado por padrão quando `knowledge` é fornecido ao Agente.
    knowledge=knowledge_base,
    # search_knowledge=True dá ao Agente a capacidade de pesquisar sob demanda
    # search_knowledge é True por padrão
    search_knowledge=True,
    instructions=[
        "Inclua fontes em sua resposta.",
        "Sempre pesquise seu conhecimento (Detran DF Habilitação) antes de responder a pergunta.",
        "Se a pergunta não for relacionada ao Detran DF Habilitação, responda educadamente: 'Desculpe, não encontrei informações sobre a sua pergunta nos documentos do Detran DF Habilitação.'",
        "Sempre responda em português brasileiro (pt-br).",
    ],
    markdown=True,
)

if __name__ == "__main__":
    # Carregar a base de conhecimento, comente após a primeira execução:
    #knowledge_base.load(recreate=True)
    agent.print_response("O que é o serviço de Autorização para conduzir ciclomotor - ACC?", stream=True)
