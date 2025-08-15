#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro
"""
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools import tool
from agno.workflow.v2 import Workflow, Step, Condition, Parallel
from agno.storage.sqlite import SqliteStorage
from datetime import datetime
import json

import sys
import os
# Adiciona o diretório raiz do projeto ao PATH do Python:
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import OPENAI_API_KEY

# 1. FERRAMENTAS PERSONALIZADAS PARA INDÚSTRIA

@tool
def verificar_temperatura_forno(forno_id: str) -> dict:
    """Verifica temperatura atual do forno industrial"""
    # Simulação - conectaria com sistema real
    import random
    temp = random.randint(800, 1200)
    return {
        "forno_id": forno_id,
        "temperatura": temp,
        "status": "normal" if 850 <= temp <= 1150 else "alerta",
        "timestamp": datetime.now().isoformat()
    }

@tool
def verificar_qualidade_produto(lote_id: str) -> dict:
    """Executa controle de qualidade do lote"""
    import random
    qualidade = random.choice(["aprovado", "reprovado", "retrabalho"])
    return {
        "lote_id": lote_id,
        "resultado": qualidade,
        "defeitos": random.randint(0, 5) if qualidade != "aprovado" else 0,
        "timestamp": datetime.now().isoformat()
    }

@tool
def ajustar_parametros_maquina(maquina_id: str, parametros: dict) -> dict:
    """Ajusta parâmetros da máquina"""
    return {
        "maquina_id": maquina_id,
        "parametros_ajustados": parametros,
        "status": "ajustado",
        "timestamp": datetime.now().isoformat()
    }

# 2. AGENTES ESPECIALIZADOS

# Agent para monitoramento
monitor_agent = Agent(
    name="Monitor Industrial",
    model=OpenAIChat(id="gpt-4o-mini", api_key=OPENAI_API_KEY),
    tools=[verificar_temperatura_forno, verificar_qualidade_produto],
    #markdown=True,
    instructions="""
    Você é um especialista em monitoramento industrial. SEMPRE responda EXCLUSIVAMENTE em português brasileiro.
    - Monitore equipamentos continuamente
    - Identifique anomalias e alertas
    - Forneça relatórios claros sobre status
    - OBRIGATÓRIO: Use apenas português brasileiro em todas as respostas
    - PROIBIDO: Nunca use palavras em inglês ou outras línguas
    - Todas as suas respostas devem ser 100% em português do Brasil
    """
)

# Agent para controle de qualidade
qualidade_agent = Agent(
    name="Controle de Qualidade",
    model=OpenAIChat(id="gpt-4o-mini", api_key=OPENAI_API_KEY),
    tools=[verificar_qualidade_produto],
    #markdown=True,
    instructions="""
    Você é responsável pelo controle de qualidade. SEMPRE responda EXCLUSIVAMENTE em português brasileiro.
    - Analise resultados de testes
    - Classifique produtos (aprovado/reprovado/retrabalho)
    - Identifique padrões de defeitos
    - OBRIGATÓRIO: Use apenas português brasileiro em todas as respostas
    - PROIBIDO: Nunca use palavras em inglês ou outras línguas
    - Todas as suas respostas devem ser 100% em português do Brasil
    """
)

# Agent para manutenção
manutencao_agent = Agent(
    name="Sistema de Manutenção",
    model=OpenAIChat(id="gpt-4o-mini", api_key=OPENAI_API_KEY),
    tools=[ajustar_parametros_maquina],
    #markdown=True,
    instructions="""
    Você gerencia manutenção e ajustes. SEMPRE responda EXCLUSIVAMENTE em português brasileiro.
    - Execute ajustes preventivos
    - Responda a alertas de equipamentos
    - Otimize parâmetros de produção
    - OBRIGATÓRIO: Use apenas português brasileiro em todas as respostas
    - PROIBIDO: Nunca use palavras em inglês ou outras línguas
    - Todas as suas respostas devem ser 100% em português do Brasil
    """
)

# 3. FUNÇÕES DE AVALIAÇÃO PARA WORKFLOW

def precisa_manutencao(step_input) -> bool:
    """Avalia se equipamento precisa manutenção"""
    try:
        # Analisa resultado do monitoramento
        content = step_input.previous_step_content
        return "alerta" in content.lower() or "problema" in content.lower()
    except:
        return False

def qualidade_aprovada(step_input) -> bool:
    """Verifica se qualidade foi aprovada"""
    try:
        content = step_input.previous_step_content
        return "aprovado" in content.lower()
    except:
        return False

# 4. WORKFLOW INDUSTRIAL COMPLETO

workflow_industrial = Workflow(
    name="Sistema de Produção Industrial",
    description="Workflow completo de monitoramento, qualidade e manutenção",
    storage=SqliteStorage(
        table_name="producao_industrial",
        db_file="tmp/industrial.db",
        mode="workflow_v2"
    ),
    steps=[
        # Etapa 1: Monitoramento paralelo
        Parallel(
            Step(
                name="monitorar_forno",
                agent=monitor_agent,
                description="Monitorar temperatura dos fornos"
            ),
            Step(
                name="controle_qualidade",
                agent=qualidade_agent,
                description="Verificar qualidade dos produtos"
            ),
            name="monitoramento_paralelo",
            description="Monitoramento simultâneo de equipamentos e qualidade"
        ),
        
        # Etapa 2: Manutenção condicional
        Condition(
            name="verificar_manutencao",
            description="Executar manutenção se necessário",
            evaluator=precisa_manutencao,
            steps=[
                Step(
                    name="executar_manutencao",
                    agent=manutencao_agent,
                    description="Executar ajustes e manutenção"
                )
            ]
        ),
        
        # Etapa 3: Reprocessamento condicional
        Condition(
            name="verificar_reprocessamento",
            description="Reprocessar se qualidade não aprovada",
            evaluator=lambda x: not qualidade_aprovada(x),
            steps=[
                Step(
                    name="reprocessar",
                    agent=qualidade_agent,
                    description="Reprocessar lote com problemas"
                )
            ]
        )
    ]
)

# 5. EXECUÇÃO DO SISTEMA

if __name__ == "__main__":
    print("🏭 Iniciando Sistema Industrial Agno")
    print("=" * 50)
    
    # Simular ciclo de produção
    resultado = workflow_industrial.run(
        message="Iniciar ciclo de produção - Lote L001, Forno F001. IMPORTANTE: Responder APENAS em português brasileiro, nunca usar palavras em inglês.",
        stream=True
    )
    
    print("\n📊 Relatório do Ciclo:")
    
    # Coleta todo o conteúdo do stream
    conteudo_completo = ""
    for response in resultado:
        if hasattr(response, 'content') and response.content:
            conteudo_completo += response.content
    
    # Imprime o conteúdo completo de uma vez
    print(conteudo_completo)
            