#!/usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script agent_os_enable_mcp_server.py
====================================
This script configures the AgentOS as an MCP server.
It uses the AgentOS to delegate tasks to specialized agents.
Specialized agents:
- web-research-agent: Web search via DuckDuckGo
- knowledge-base-agent: Knowledge base search (Eddy Giusepe Chirinos Isidro's Curriculum Vitae - CV of Eddy)

Run:
uv run agent_os_enable_mcp_server.py
"""
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.knowledge.chunking.document import DocumentChunking
from agno.models.anthropic import Claude
from agno.os import AgentOS
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.knowledge.embedder.openai import OpenAIEmbedder
import sys
from pathlib import Path
from textwrap import dedent
from typing import Optional
from prompts_agent_os_and_mcp.prompts import (
    WEB_RESEARCH_AGENT_PROMPT,
    KNOWLEDGE_BASE_AGENT_PROMPT,
)

# Add the project root directory to the sys.path:
sys.path.append(str(Path(__file__).parent.parent))
from config.settings import ANTHROPIC_API_KEY, OPENAI_API_KEY


class AgentOSMCPServer:
    """
    Main class to configure and run the AgentOS as MCP Server.

    This class encapsulates the entire configuration and execution of the AgentOS as MCP Server,
    including:
    - Configuration of the SQLite database
    - Configuration of the knowledge base with LanceDB
    - Creation of specialized agents (Web Research and Knowledge Base)
    - Exposure of the MCP server via FastAPI

    Attributes:
        user_id (str): ID of the user to persist memories.
        anthropic_api_key (str): API key for Anthropic.
        openai_api_key (str): API key for OpenAI.
        db_path (str): Path to the SQLite database.
        lancedb_uri (str): URI to the LanceDB database.
        documents_path (Path): Path to the PDF documents.

    Example:
        >>> server = AgentOSMCPServer(
        ...     anthropic_api_key=ANTHROPIC_API_KEY,
        ...     openai_api_key=OPENAI_API_KEY,
        ... )
        >>> server.serve()
    """

    def __init__(
        self,
        anthropic_api_key: str = ANTHROPIC_API_KEY,
        openai_api_key: str = OPENAI_API_KEY,
        db_path: str = "tmp/agentos.db",
        lancedb_uri: str = "tmp/lancedb_kb",
        documents_path: Optional[Path] = (Path(__file__).parent / "data" / "documents"),
        user_id: str = "eddy-giusepe",
    ) -> None:
        """
        Initialize the AgentOSMCPServer with the necessary configurations.

        Args:
            anthropic_api_key: API key for Anthropic.
            openai_api_key: API key for OpenAI.
            db_path: Path to the SQLite database. Defaults to "tmp/agentos.db".
            lancedb_uri: URI to the LanceDB database. Defaults to "tmp/lancedb_kb".
            documents_path: Path to the PDF documents. Defaults to (Path(__file__).parent / "data" / "documents").
            user_id: ID of the user to persist memories. Defaults to "eddy-giusepe".
        """
        # Fixed user ID to persist memories consistently:
        self.user_id: str = user_id
        self.anthropic_api_key: str = anthropic_api_key
        self.openai_api_key: str = openai_api_key
        self.db_path: str = db_path
        self.lancedb_uri: str = lancedb_uri
        self.documents_path: Path = documents_path or (
            Path(__file__).parent / "data" / "documents"
        )

        # Setup the database:
        self.db: SqliteDb = self._setup_database()

        # Setup knowledge base with PDFs:
        self.knowledge_base: Knowledge = self._setup_knowledge_base()

        # Setup basic research agent:
        self.web_research_agent: Agent = self._create_web_research_agent()

        # Setup knowledge base agent:
        self.knowledge_base_agent: Agent = self._create_knowledge_base_agent()

        # Setup our AgentOS with MCP enabled:
        self.agent_os: AgentOS = self._setup_agent_os()

    def _setup_database(self) -> SqliteDb:
        """
        Setup and return the SQLite database.

        Returns:
            SqliteDb: Configured instance of the SQLite database.
        """
        # Setup the database:
        return SqliteDb(db_file=self.db_path)

    def _setup_knowledge_base(self) -> Knowledge:
        """
        Setup and return the knowledge base with LanceDB.

        Setup the PDF reader with chunking strategy,
        setup the LanceDB vector database with OpenAI embeddings,
        and add the content of the documents.

        Returns:
            Knowledge: Configured instance of the knowledge base.
        """
        reader = PDFReader(
            chunking_strategy=DocumentChunking(chunk_size=600, overlap=150)
        )

        # Setup knowledge base with PDFs:
        knowledge_base = Knowledge(
            vector_db=LanceDb(
                uri=self.lancedb_uri,
                table_name="pdf_knowledge_cv_eddy",
                search_type=SearchType.hybrid,
                embedder=OpenAIEmbedder(
                    id="text-embedding-3-small", api_key=self.openai_api_key
                ),
            ),
            contents_db=self.db,  # Database to track added contents
            max_results=8,
        )

        # Add content using add_content or add_content_async:
        knowledge_base.add_content(
            path=self.documents_path,
            reader=reader,
            skip_if_exists=True,  # Indicates that if the content already exists, do not add it again.
        )
        # or asynchronously:
        # await knowledge_base.add_content_async(path="data/documents", reader=reader)

        return knowledge_base

    def _create_web_research_agent(self) -> Agent:
        """
        Create and return the web research agent.

        The agent uses DuckDuckGo for internet searches,
        with support for user memories and session history.

        Returns:
            Agent: Configured instance of the web research agent.
        """
        # Setup basic research agent:
        return Agent(
            id="web-research-agent",
            name="Web Research Agent",
            description=dedent(
                """Web search agent for general internet information. Use for current events,
                                  news, public data and information that are NOT about Eddy Giusepe Chirinos Isidro.
                               """
            ),
            user_id=self.user_id,  # Fixed user ID to persist memories consistently
            model=Claude(
                api_key=self.anthropic_api_key,
                id="claude-sonnet-4-5",
                temperature=0.0,
                max_tokens=2000,
                instructions=dedent(WEB_RESEARCH_AGENT_PROMPT),
            ),
            db=self.db,
            tools=[DuckDuckGoTools()],
            add_history_to_context=True,
            num_history_runs=5,  # Increased from 3 to 5 for more context
            add_datetime_to_context=True,
            enable_user_memories=True,  # Needs the user_id to associate memories to the user.
            # enable_agentic_memory=True,  # This has priority over enable_user_memories. Do not use both together.
            enable_session_summaries=True,  # Enables the generation of session summaries for improved delegation.
            add_memories_to_context=True,  # Needs the user_id to retrieve the user's memories.
            add_session_summary_to_context=True,  # Adds the session summary to the context. Needs partially the user_id.
            markdown=True,
        )

    def _create_knowledge_base_agent(self) -> Agent:
        """
        Create and return the knowledge base agent.

        The agent is specialized in information about Eddy Giusepe Chirinos Isidro,
        using the configured knowledge base to search for information.

        Returns:
            Agent: Configured instance of the knowledge base agent.
        """
        # Setup knowledge base agent:
        return Agent(
            id="knowledge-base-agent",
            name="Knowledge Base Agent",
            description=dedent(
                """Specialist in information about Eddy Giusepe Chirinos Isidro.
                                  Use for questions about Eddy, his curriculum, skills, experience and formation.
                               """
            ),
            user_id=self.user_id,  # Fixed user ID to persist memories consistently
            model=Claude(
                api_key=self.anthropic_api_key,
                id="claude-sonnet-4-5",
                temperature=0.0,
                max_tokens=2000,
                instructions=dedent(KNOWLEDGE_BASE_AGENT_PROMPT),
            ),
            db=self.db,
            knowledge=self.knowledge_base,
            search_knowledge=True,  # Enables automatic search in the knowledge base
            add_history_to_context=True,
            num_history_runs=5,  # Increased from 3 to 5 for more context
            add_datetime_to_context=True,
            enable_user_memories=True,  # Enables the use of user memories, that is, the user can update the agent's memories.
            # enable_agentic_memory=True,  # Enables the use of agentic memories, that is, the agent can update the user's memories.
            enable_session_summaries=True,  # Enables the generation of session summaries for improved delegation.
            add_memories_to_context=True,  # Adds the memories to the context for improved delegation.
            add_session_summary_to_context=True,  # Adds the session summary to the context for improved delegation.
            markdown=True,
        )

    def _setup_agent_os(self) -> AgentOS:
        """
        Setup and return the AgentOS with MCP enabled.

        The AgentOS manages the specialized agents and exposes
        the MCP server (Model Context Protocol) for integration.

        Returns:
            AgentOS: Configured instance of the AgentOS.
        """
        # Setup our AgentOS with MCP enabled:
        return AgentOS(
            description="AgentOS with MCP enabled - Web Research and Knowledge Base",
            agents=[
                self.knowledge_base_agent,
                self.web_research_agent,
            ],  # KB first for priority on questions about Eddy Giusepe Chirinos Isidro
            enable_mcp_server=True,  # This enables a LLM-friendly MCP server at /mcp (Model Context Protocol)
            version="1.0",
            name="🤗 My second AgentOS 🤗",
            telemetry=True,
            tracing=True,
        )

    def get_app(self):
        """
        Return the FastAPI application of the AgentOS.

        Returns:
            FastAPI: Configured FastAPI application with the AgentOS endpoints.
        """
        return self.agent_os.get_app()

    def serve(
        self,
        app: str = "agent_os_enable_mcp_server:app",
        host: str = "0.0.0.0",
        port: int = 7777,
        ws: str = "websockets-sansio",
    ) -> None:
        """
        Start the AgentOS server.

        Args:
            app: Path to the application in the format "module:app".
                 Defaults to "agent_os_enable_mcp_server:app".
            host: Host address. Defaults to "0.0.0.0".
            port: Server port. Defaults to 7777.
            ws: WebSocket implementation. Defaults to "websockets-sansio".

        Note:
            The MCP server will be available at http://localhost:{port}/mcp
        """
        # Use websockets-sansio to avoid warnings of websockets.legacy deprecation
        # uvicorn 0.35.0+ supports the new websockets-sansio implementation
        self.agent_os.serve(app=app, host=host, port=port, ws=ws)


# Global instance for use with uvicorn:
agent_os_server = AgentOSMCPServer(
    anthropic_api_key=ANTHROPIC_API_KEY,
    openai_api_key=OPENAI_API_KEY,
)
app = agent_os_server.get_app()


if __name__ == "__main__":
    """Run your AgentOS.

    You can see your LLM-friendly MCP server at:
    http://localhost:7777/mcp
    """
    agent_os_server.serve()
