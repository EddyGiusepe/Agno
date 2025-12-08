#!/usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script my_agent_os.py
=====================
This script implements a runtime AgentOS using the Agno framework.
It provides a runtime AgentOS with persistence, telemetry and tracing capabilities.
The runtime AgentOS is a FastAPI server that orchestrates AI agents.
"""
import os
import sys
from pydantic import BaseModel, Field, PrivateAttr

# Add the root directory to the Python path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.db.sqlite import AsyncSqliteDb
from agno.os import AgentOS
from config.settings import OPENAI_API_KEY


class AgentOSManager(BaseModel):
    """
    Manager of the runtime AgentOS. The AgentOS is like a FastAPI server
    that orchestrates AI agents.

    This class encapsulates the entire configuration and creation of the runtime AgentOS,
    including the AI model, database, agent instructions, etc.

    Attributes:
        model_id: OpenAI model identifier (e.g. "gpt-4o", "gpt-4o-mini").
        temperature: Controls the randomness of the responses (0.0 to 2.0).
        max_tokens: Maximum number of tokens in the generated response.
        agent_name: Agent identifier name.
        db_file: Path to the SQLite database file for persistence.
        instructions: List of agent behavior instructions.
        markdown: If True, enables markdown formatting in responses.
        os_id: Unique identifier of the runtime AgentOS.
        os_name: Display name of the runtime AgentOS.
        os_description: Detailed description of the runtime AgentOS.
        version: Version of the runtime AgentOS.
        telemetry: If True, enables telemetry collection. (default: True)
        tracing: If True, enables execution tracing. (default: True)

    Example:
        >>> manager = AgentOSManager(
        ...     model_id="gpt-4o-mini",
        ...     temperature=0.1,
        ...     max_tokens=500
        ... )
        >>> app = manager.get_app()
        >>> manager.serve()
    """

    # Model configuration:
    model_id: str = Field(default="gpt-4o-mini", description="OpenAI model identifier")
    temperature: float = Field(
        default=0.0,
        ge=0.0,
        le=2.0,
        description="Temperature for text generation (0.0 to 2.0)",
    )
    max_tokens: int = Field(
        default=300,
        gt=200,
        le=600,
        description="Maximum number of tokens in the response",
    )

    # Agent configuration:
    agent_name: str = Field(
        default="AgentEddy", min_length=1, description="Name of the agent"
    )
    db_file: str = Field(default="my_agent_os.db", description="SQLite database file")
    instructions: list[str] = Field(
        default=[
            "Você é um assistente de IA que responde educadamente, gentil e factualmente ao usuário.",
            "Sempre responda in the language of the user and at the end always add an emoji.",
        ],
        description="Agent behavior instructions",
    )
    markdown: bool = Field(
        default=True, description="Enables markdown formatting in responses"
    )

    # Runtime AgentOS configuration:
    os_id: str = Field(
        default="my-first-os",
        min_length=1,
        description="Unique identifier of the AgentOS",
    )
    os_name: str = Field(
        default="🤗 My first AgentOS 🤗", description="Display name of the AgentOS"
    )
    os_description: str = Field(
        default=("Runtime AgentOS developed by Eddy Giusepe. "),
        description="Description of the AgentOS",
    )
    version: str = Field(default="1.0", description="Version of the AgentOS")
    telemetry: bool = Field(default=True, description="Enables telemetry")
    tracing: bool = Field(default=True, description="Enables tracing")

    # Lazy initialization pattern: cache the instances for performance optimization
    # Use PrivateAttr from Pydantic v2 for attributes that should not be serialized
    _agent: Agent | None = PrivateAttr(default=None)
    _agent_os: AgentOS | None = PrivateAttr(default=None)

    def _create_agent(self) -> Agent:
        """
        Create and configure the AI agent with lazy initialization.

        Returns:
            Agent: Configured instance of the Agent with model, database and instructions.
        """
        if self._agent is None:
            model = OpenAIChat(
                api_key=OPENAI_API_KEY,
                id=self.model_id,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            database = AsyncSqliteDb(db_file=self.db_file)

            self._agent = Agent(
                name=self.agent_name,
                model=model,
                db=database,
                instructions=self.instructions,
                markdown=self.markdown,
            )
        return self._agent

    def _create_agent_os(self) -> AgentOS:
        """
        Create and configure the runtime AgentOS with lazy initialization.

        Returns:
            AgentOS: Configured instance of the runtime AgentOS.
        """
        if self._agent_os is None:
            agent = self._create_agent()
            self._agent_os = AgentOS(
                id=self.os_id,
                name=self.os_name,
                description=self.os_description,
                version=self.version,
                telemetry=self.telemetry,
                tracing=self.tracing,
                agents=[agent],
            )
        return self._agent_os

    def get_app(self):
        """
        Returns the FastAPI application of the AgentOS.

        Returns:
            FastAPI: Configured application ready to serve.
        """
        agent_os = self._create_agent_os()
        return agent_os.get_app()

    def serve(self, app_path: str = "my_agent_os:app", reload: bool = True) -> None:
        """
        Start the AgentOS server.

        Args:
            app_path: Path to the application in the format "module:variable".
            reload: If True, enables automatic reload in development (default: True).
        """
        agent_os = self._create_agent_os()
        agent_os.serve(app=app_path, reload=reload)


manager = AgentOSManager(
    model_id="gpt-4o-mini",  # "gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"
    temperature=0.1,  # 0.0 = deterministic, 1.0 = creative
    max_tokens=500,  # Maximum number of tokens in the response
    agent_name="AgentEddy",  # Assistant
    db_file="my_agent_os.db",
    instructions=[
        "You are an AI assistant, called AgentEddy, that responds educatively and usefully.",
        "Always respond in the language of the user and at the end always add an emoji.",
    ],
    markdown=True,
    os_id="my-first-os",
    os_name="🤗 My first AgentOS 🤗",
    os_description=("Runtime AgentOS developed by Dr. Eddy Giusepe."),
    version="1.0",
    telemetry=True,
    tracing=True,
)


app = manager.get_app()


if __name__ == "__main__":
    manager.serve(app_path="my_agent_os:app", reload=True)
