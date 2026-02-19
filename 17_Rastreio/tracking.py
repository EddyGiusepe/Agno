#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Link: https://support.aftership.com/en/tracking/article/learn-more-about-aftership-api-1eab61j

Rastreamento de Pacotes - AfterShip API
========================================
Este script implementa um agente inteligente para rastreamento de pacotes
usando a API do AfterShip (aftership.com).

Características da API AfterShip:
----------------------------------
- Suporte a 1.207+ transportadoras globais
- Rastreamento no Brasil: Correios, BrasPress, Diálogo, Bulkylog, etc.
- Dados normalizados (7 status principais, 33 substatus)
- 99.99% uptime, ISO 27001, SOC2, GDPR
- Rate limit: 10 requisições por segundo
- Modo de teste gratuito disponível

Modo de Teste (Gratuito):
--------------------------
- Slug: "testing-courier"
- Número de teste: "ITOD-3-xxxxxxxxxx" (cada número usado apenas uma vez)
- Não requer conta paga para testar

Modo Produção:
--------------
- Correios Brasil: slug "brazil-correios", formato AA123456789BR
- BrasPress: slug "braspress"
- Bulkylog: slug suportado
- Outras: detecta automaticamente ou especifica slug

Run
---
uv run tracking.py
"""
import sys
import requests
from pathlib import Path
from typing import Dict, Any, Optional
from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools import tool
    
# Add the parent directory to the path to import config:
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.settings import OPENAI_API_KEY, AFTERSHIP_API_KEY


# ============================================================================
# FERRAMENTAS CUSTOMIZADAS PARA AFTERSHIP API v4
# ============================================================================

AFTERSHIP_BASE_URL = "https://api.aftership.com/v4"
AFTERSHIP_HEADERS = {
    "aftership-api-key": AFTERSHIP_API_KEY,
    "Content-Type": "application/json"
}


@tool
def create_tracking(tracking_number: str, slug: Optional[str] = None) -> Dict[str, Any]:
    """
    Cria um novo rastreamento no AfterShip.
    
    Args:
        tracking_number: Código de rastreamento (ex: "AC579104723BR" para Correios ou "ITOD-3-teste123" para teste)
        slug: Identificador da transportadora (ex: "brazil-correios", "braspress", "testing-courier").
              Se None, o AfterShip tentará detectar automaticamente.
    
    Returns:
        Dicionário com informações do rastreamento criado
    """
    endpoint = f"{AFTERSHIP_BASE_URL}/trackings"
    
    payload = {
        "tracking": {
            "tracking_number": tracking_number
        }
    }
    
    # Adicionar slug se fornecido
    if slug:
        payload["tracking"]["slug"] = slug
    
    try:
        response = requests.post(endpoint, json=payload, headers=AFTERSHIP_HEADERS, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        return {
            "success": True,
            "message": "Rastreamento criado com sucesso!",
            "data": data.get("data", {})
        }
    except requests.exceptions.HTTPError as e:
        error_data = e.response.json() if e.response else {}
        return {
            "success": False,
            "error": f"Erro HTTP {e.response.status_code}",
            "message": error_data.get("meta", {}).get("message", str(e)),
            "details": error_data
        }
    except Exception as e:
        return {
            "success": False,
            "error": "Erro ao criar rastreamento",
            "message": str(e)
        }


@tool
def get_tracking(tracking_number: str, slug: Optional[str] = None) -> Dict[str, Any]:
    """
    Obtém informações atualizadas de um rastreamento existente no AfterShip.
    
    Args:
        tracking_number: Código de rastreamento
        slug: Identificador da transportadora (opcional, mas recomendado para melhor performance)
    
    Returns:
        Dicionário com status completo do rastreamento incluindo checkpoints
    """
    # Se slug fornecido, usar endpoint mais específico
    if slug:
        endpoint = f"{AFTERSHIP_BASE_URL}/trackings/{slug}/{tracking_number}"
    else:
        # Buscar por tracking_number (pode ser mais lento)
        endpoint = f"{AFTERSHIP_BASE_URL}/trackings"
        params = {"tracking_number": tracking_number}
        
        try:
            response = requests.get(endpoint, params=params, headers=AFTERSHIP_HEADERS, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            trackings = data.get("data", {}).get("trackings", [])
            if not trackings:
                return {
                    "success": False,
                    "error": "Rastreamento não encontrado",
                    "message": f"Nenhum rastreamento encontrado para o código {tracking_number}. Você pode precisar criar o rastreamento primeiro usando create_tracking."
                }
            
            return {
                "success": True,
                "data": trackings[0]
            }
        except Exception as e:
            return {
                "success": False,
                "error": "Erro ao buscar rastreamento",
                "message": str(e)
            }
    
    # Busca com slug específico
    try:
        response = requests.get(endpoint, headers=AFTERSHIP_HEADERS, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        return {
            "success": True,
            "data": data.get("data", {}).get("tracking", {})
        }
    except requests.exceptions.HTTPError as e:
        error_data = e.response.json() if e.response else {}
        return {
            "success": False,
            "error": f"Erro HTTP {e.response.status_code}",
            "message": error_data.get("meta", {}).get("message", str(e)),
            "details": error_data
        }
    except Exception as e:
        return {
            "success": False,
            "error": "Erro ao obter rastreamento",
            "message": str(e)
        }


@tool
def detect_courier(tracking_number: str) -> Dict[str, Any]:
    """
    Detecta qual transportadora corresponde ao código de rastreamento fornecido.
    
    Args:
        tracking_number: Código de rastreamento
    
    Returns:
        Lista de transportadoras possíveis para o código fornecido
    """
    endpoint = f"{AFTERSHIP_BASE_URL}/couriers/detect"
    
    payload = {
        "tracking": {
            "tracking_number": tracking_number
        }
    }
    
    try:
        response = requests.post(endpoint, json=payload, headers=AFTERSHIP_HEADERS, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        couriers = data.get("data", {}).get("couriers", [])
        
        if not couriers:
            return {
                "success": False,
                "message": "Nenhuma transportadora detectada para este código"
            }
        
        return {
            "success": True,
            "couriers": couriers,
            "message": f"Detectadas {len(couriers)} transportadora(s) possível(is)"
        }
    except Exception as e:
        return {
            "success": False,
            "error": "Erro ao detectar transportadora",
            "message": str(e)
        }


# ============================================================================
# AGENTE DE RASTREAMENTO
# ============================================================================

tracking_agent = Agent(
    name="Analista de Rastreamento Multi-Transportadoras",
    model=OpenAIResponses(id="gpt-4o-mini", api_key=OPENAI_API_KEY),
    tools=[create_tracking, get_tracking, detect_courier],
    instructions=[
        "Você é um analista especializado em rastreamento de pacotes usando a API do AfterShip.",
        "O AfterShip suporta mais de 1.200 transportadoras, incluindo todas as principais do Brasil.",
        "",
        "TRANSPORTADORAS BRASILEIRAS SUPORTADAS:",
        "- Correios do Brasil (slug: 'brazil-correios', formato: AA123456789BR - 13 caracteres)",
        "- BrasPress (slug: 'braspress')",
        "- Diálogo Logística (slug: 'dialogo-logistica')",
        "- Bulkylog (suportada)",
        "- Loggi (slug: 'loggi')",
        "- E muitas outras transportadoras nacionais e internacionais",
        "",
        "MODO DE TESTE GRATUITO:",
        "- Para testar sem custo, use: slug='testing-courier' com números no formato 'ITOD-3-xxxxxxxxxx'",
        "- Exemplo: tracking_number='ITOD-3-teste123456', slug='testing-courier'",
        "- ATENÇÃO: Cada número de teste só pode ser usado UMA vez",
        "- Ideal para: testar a integração antes de usar códigos reais",
        "",
        "MODO PRODUÇÃO:",
        "- Para Correios: tracking_number='AA123456789BR', slug='brazil-correios'",
        "- Para outras: forneça o código e o slug específico, ou deixe o AfterShip detectar automaticamente",
        "",
        "WORKFLOW DE RASTREAMENTO:",
        "1. Se o usuário fornecer um código de teste (ITOD-3-xxx), use create_tracking com slug='testing-courier'",
        "2. Se for código dos Correios (formato AA123456789BR), use create_tracking com slug='brazil-correios'",
        "3. Se não souber a transportadora, use detect_courier primeiro para identificar",
        "4. Após criar o rastreamento, use get_tracking para obter detalhes completos",
        "5. Se o rastreamento já existir (erro 4003), use get_tracking diretamente",
        "",
        "INFORMAÇÕES A FORNECER AO USUÁRIO:",
        "- Status atual da entrega (tag: Pending, InfoReceived, InTransit, OutForDelivery, Delivered, etc.)",
        "- Checkpoints com data, hora, local e descrição de cada evento",
        "- Transportadora utilizada",
        "- Previsão de entrega (se disponível)",
        "- Orientações claras caso haja erros ou problemas",
        "",
        "TRATAMENTO DE ERROS:",
        "- Se erro 4003 (tracking já existe): use get_tracking para consultar",
        "- Se erro 4004 (tracking não encontrado): oriente sobre formato correto do código",
        "- Se erro 4005 (slug inválido): sugira usar detect_courier",
        "- Se código não for reconhecido: explique formato esperado para cada transportadora",
        "",
        "SEMPRE responda em português brasileiro (pt-BR) de forma clara e amigável.",
        "Forneça informações completas sobre o status do pacote e próximos passos esperados.",
    ],
    markdown=True,
    add_datetime_to_context=True,
)


# ============================================================================
# EXECUÇÃO DE EXEMPLO
# ============================================================================

if __name__ == "__main__":
    print("🚀 Sistema de Rastreamento Multi-Transportadoras - AfterShip")
    print("=" * 70)
    print()
    print("💡 DICA: Para testar gratuitamente, use:")
    print("   Código: ITOD-3-teste123456")
    print("   (cada código de teste só funciona uma vez)")
    print()
    print("=" * 70)
    print()
    
    # Teste com modo gratuito
    response = tracking_agent.print_response(
        "Rastreie o pacote ITOD-3-teste123456 usando o modo de teste gratuito"
    )
