#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script interacting_with_agent_os.py
=====================================
Este script demonstra como interagir com o AgentOS de forma
interativa. Permite um bate-papo contínuo com o agente.

Run
---
uv run interacting_with_agent_os.py
"""
from typing import Optional
import requests
from pydantic import BaseModel, Field
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt


class AgentMetrics(BaseModel):
    """Métricas de execução do agente.
    
    Attributes:
        input_tokens: Número de tokens de entrada.
        output_tokens: Número de tokens de saída.
        total_tokens: Total de tokens utilizados.
        reasoning_tokens: Tokens usados para raciocínio (se aplicável).
        time_to_first_token: Tempo até o primeiro token (segundos).
        duration: Duração total da execução (segundos).
    """
    input_tokens: int = Field(default=0, description="Tokens de entrada")
    output_tokens: int = Field(default=0, description="Tokens de saída")
    total_tokens: int = Field(default=0, description="Total de tokens")
    reasoning_tokens: int = Field(default=0, description="Tokens de raciocínio")
    time_to_first_token: float = Field(default=0.0, description="Tempo até primeiro token")
    duration: float = Field(default=0.0, description="Duração em segundos")


class AgentResponse(BaseModel):
    """Representa a resposta completa do agente.
    
    Esta classe usa Pydantic para validação automática de tipos,
    conversão de dados e serialização JSON.
    
    Attributes:
        content: O conteúdo da resposta do agente.
        run_id: ID único da execução.
        agent_id: ID do agente que respondeu.
        agent_name: Nome do agente.
        session_id: ID da sessão para contexto.
        status: Status da resposta (COMPLETED, ERROR, etc.).
        model: Modelo de IA utilizado.
        model_provider: Provedor do modelo (OpenAI, etc.).
        metrics: Métricas de execução.
    
    Example:
        >>> response = AgentResponse(content="Olá!", status="COMPLETED")
        >>> print(response.content)
        Olá!
        >>> print(response.model_dump_json(indent=2))
    """
    content: str = Field(default="", description="Conteúdo da resposta")
    run_id: Optional[str] = Field(default=None, description="ID da execução")
    agent_id: Optional[str] = Field(default=None, description="ID do agente")
    agent_name: Optional[str] = Field(default=None, description="Nome do agente")
    session_id: Optional[str] = Field(default=None, description="ID da sessão")
    status: Optional[str] = Field(default=None, description="Status da resposta")
    model: Optional[str] = Field(default=None, description="Modelo utilizado")
    model_provider: Optional[str] = Field(default=None, description="Provedor do modelo")
    metrics: AgentMetrics = Field(default_factory=AgentMetrics, description="Métricas")
    
    @classmethod
    def from_api_response(cls, data: dict) -> "AgentResponse":
        """Cria uma instância a partir da resposta da API.
        
        Args:
            data: Dicionário com os dados da resposta da API.
        
        Returns:
            AgentResponse: Instância populada com os dados.
        
        Example:
            >>> data = {"content": "Olá!", "status": "COMPLETED"}
            >>> response = AgentResponse.from_api_response(data)
        """
        metrics_data = data.get("metrics", {})
        metrics = AgentMetrics(
            input_tokens=metrics_data.get("input_tokens", 0),
            output_tokens=metrics_data.get("output_tokens", 0),
            total_tokens=metrics_data.get("total_tokens", 0),
            reasoning_tokens=metrics_data.get("reasoning_tokens", 0),
            time_to_first_token=metrics_data.get("time_to_first_token", 0.0),
            duration=metrics_data.get("duration", 0.0)
        )
        
        return cls(
            content=data.get("content", ""),
            run_id=data.get("run_id"),
            agent_id=data.get("agent_id"),
            agent_name=data.get("agent_name"),
            session_id=data.get("session_id"),
            status=data.get("status"),
            model=data.get("model"),
            model_provider=data.get("model_provider"),
            metrics=metrics
        )


class AgentOSClient:
    """Cliente para interagir com o AgentOS via API REST.
    
    Esta classe fornece uma interface simples e profissional para 
    comunicação com agentes do AgentOS.
    
    Attributes:
        base_url: URL base do AgentOS (padrão: http://localhost:7777).
        agent_id: ID do agente para interação (padrão: assistant).
        session_id: ID da sessão para manter contexto entre mensagens.
        timeout: Timeout para requisições em segundos.
    
    Example:
        >>> client = AgentOSClient()
        >>> response = client.send_message("Qual é a capital do Brasil?")
        >>> print(response.content)
        A capital do Brasil é Brasília.
    """
    
    def __init__(
        self,
        base_url: str = "http://localhost:7777",
        agent_id: str = "agenteddy", # Assistant
        session_id: Optional[str] = None,
        timeout: int = 60
    ) -> None:
        """Inicializa o cliente do AgentOS.
        
        Args:
            base_url: URL base do AgentOS.
            agent_id: ID do agente para interação.
            session_id: ID da sessão (opcional, para manter contexto).
            timeout: Timeout para requisições em segundos.
        """
        self.base_url = base_url.rstrip("/")
        self.agent_id = agent_id
        self.session_id = session_id
        self.timeout = timeout
        self._console = Console()
    
    @property
    def _endpoint(self) -> str:
        """Retorna o endpoint completo para execução do agente."""
        return f"{self.base_url}/agents/{self.agent_id}/runs"
    
    def send_message(
        self,
        message: str,
        stream: bool = False,
        user_id: Optional[str] = None
    ) -> AgentResponse:
        """Envia uma mensagem ao agente e retorna a resposta.
        
        Args:
            message: A mensagem a ser enviada ao agente.
            stream: Se True, habilita streaming da resposta.
            user_id: ID do usuário (opcional).
        
        Returns:
            AgentResponse: Objeto contendo a resposta e metadados.
        
        Raises:
            ConnectionError: Se não conseguir conectar ao AgentOS.
            ValueError: Se a resposta for inválida.
        
        Example:
            >>> client = AgentOSClient()
            >>> response = client.send_message("Olá!")
            >>> print(response.content)
        """
        data: dict[str, str] = {
            "message": message,
            "stream": str(stream).lower()
        }
        
        if self.session_id:
            data["session_id"] = self.session_id
        
        if user_id:
            data["user_id"] = user_id
        
        try:
            response = requests.post(
                self._endpoint,
                data=data,
                timeout=self.timeout
            )
            response.raise_for_status()
            
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(
                f"Não foi possível conectar ao AgentOS em {self.base_url}. "
                "Verifique se o servidor está rodando."
            ) from e
        except requests.exceptions.Timeout as e:
            raise TimeoutError(
                f"Timeout ao aguardar resposta do agente ({self.timeout}s)."
            ) from e
        except requests.exceptions.HTTPError as e:
            raise ValueError(f"Erro na requisição: {e}") from e
        
        resultado = response.json()
        
        # Atualizar session_id se retornado
        if "session_id" in resultado:
            self.session_id = resultado["session_id"]
        
        # Criar resposta usando Pydantic (valida e converte tipos automaticamente)
        return AgentResponse.from_api_response(resultado)
    
    def health_check(self) -> bool:
        """Verifica se o AgentOS está disponível.
        
        Returns:
            bool: True se o servidor está disponível, False caso contrário.
        """
        try:
            response = requests.get(
                f"{self.base_url}/health",
                timeout=5
            )
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False


class InteractiveChat:
    """Interface interativa para bate-papo com o AgentOS.
    
    Fornece uma experiência de chat rica e interativa no terminal.
    
    Example:
        >>> chat = InteractiveChat()
        >>> chat.start()
    """
    
    def __init__(
        self,
        client: Optional[AgentOSClient] = None,
        show_metrics: bool = True
    ) -> None:
        """Inicializa o chat interativo.
        
        Args:
            client: Cliente do AgentOS (opcional, cria um novo se não fornecido).
            show_metrics: Se True, exibe métricas após cada resposta.
        """
        self.client = client or AgentOSClient()
        self.show_metrics = show_metrics
        self._console = Console()
        self._running = False
    
    def _print_welcome(self) -> None:
        """Exibe mensagem de boas-vindas."""
        self._console.print()
        self._console.print(Panel(
            "[bold cyan]🤗 Bem-vindo ao AgentOS Chat! 🤗[/bold cyan]\n\n"
            "[yellow]Digite suas mensagens para conversar com o agente.[/yellow]\n"
            "[dim]Comandos especiais:[/dim]\n"
            "[dim]  • 'sair' ou 'exit' - Encerra o chat[/dim]\n"
            "[dim]  • 'limpar' ou 'clear' - Limpa a tela[/dim]\n"
            "[dim]  • 'metrics on/off' - Ativa/desativa métricas[/dim]\n"
            "[dim]  • 'nova sessão' - Inicia nova sessão[/dim]",
            title="[bold white]AgentOS Interactive Chat[/bold white]",
            border_style="cyan",
            expand=False
        ))
        self._console.print()
    
    def _print_response(self, response: AgentResponse) -> None:
        """Exibe a resposta do agente formatada.
        
        Args:
            response: Resposta do agente a ser exibida.
        """
        # Renderizar como Markdown
        md = Markdown(response.content)
        self._console.print()
        self._console.print(Panel(
            md,
            title="[bold green]🤖 Assistente[/bold green]",
            border_style="green",
            expand=False
        ))
        
        # Exibir métricas se habilitado
        if self.show_metrics and response.metrics.duration > 0:
            self._console.print(
                f"[dim]⏱️ {response.metrics.duration:.2f}s | "
                f"📊 {response.metrics.input_tokens} in | {response.metrics.output_tokens} out | "
                f"{response.metrics.total_tokens} total tokens[/dim]"
            )
    
    def _print_user_message(self, message: str) -> None:
        """Exibe a mensagem do usuário formatada.
        
        Args:
            message: Mensagem do usuário.
        """
        self._console.print()
        self._console.print(Panel(
            message,
            title="[bold blue]👤 Você[/bold blue]",
            border_style="blue",
            expand=False
        ))
    
    def _handle_command(self, command: str) -> bool:
        """Processa comandos especiais.
        
        Args:
            command: Comando a ser processado.
        
        Returns:
            bool: True se deve continuar o chat, False para encerrar.
        """
        cmd = command.lower().strip()
        
        if cmd in ("sair", "exit", "quit", "q"):
            self._console.print("\n[yellow]👋 Até logo! Obrigado por usar o AgentOS![/yellow]\n")
            return False
        
        if cmd in ("limpar", "clear", "cls"):
            self._console.clear()
            self._print_welcome()
            return True
        
        if cmd == "metrics on":
            self.show_metrics = True
            self._console.print("[green]✅ Métricas ativadas[/green]")
            return True
        
        if cmd == "metrics off":
            self.show_metrics = False
            self._console.print("[yellow]⚠️ Métricas desativadas[/yellow]")
            return True
        
        if cmd in ("nova sessão", "nova sessao", "new session"):
            self.client.session_id = None
            self._console.print("[green]✅ Nova sessão iniciada[/green]")
            return True
        
        return True
    
    def start(self) -> None:
        """Inicia o chat interativo.
        
        Loop principal que processa mensagens do usuário e exibe respostas.
        """
        self._running = True
        self._print_welcome()
        
        # Verificar conexão
        if not self.client.health_check():
            self._console.print(
                "[bold red]❌ Erro: Não foi possível conectar ao AgentOS![/bold red]\n"
                f"[yellow]Verifique se o servidor está rodando em {self.client.base_url}[/yellow]\n"
            )
            return
        
        self._console.print("[green]✅ Conectado ao AgentOS![/green]\n")
        
        while self._running:
            try:
                # Obter entrada do usuário
                message = Prompt.ask("[bold cyan]Você[/bold cyan]")
                
                # Verificar se é vazio
                if not message.strip():
                    continue
                
                # Verificar se é um comando
                if message.lower().strip() in (
                    "sair", "exit", "quit", "q", "limpar", "clear", "cls",
                    "metrics on", "metrics off", "nova sessão", "nova sessao", "new session"
                ):
                    self._running = self._handle_command(message)
                    continue
                
                # Enviar mensagem ao agente
                self._console.print("[dim]⏳ Aguardando resposta...[/dim]")
                
                response = self.client.send_message(message)
                self._print_response(response)
                
            except KeyboardInterrupt:
                self._console.print("\n[yellow]👋 Chat interrompido. Até logo![/yellow]\n")
                break
            except ConnectionError as e:
                self._console.print(f"\n[bold red]❌ {e}[/bold red]\n")
                break
            except Exception as e:
                self._console.print(f"\n[bold red]❌ Erro: {e}[/bold red]\n")


def main() -> None:
    """Função principal para executar o chat interativo."""
    chat = InteractiveChat(show_metrics=True)
    chat.start()


if __name__ == "__main__":
    main()
