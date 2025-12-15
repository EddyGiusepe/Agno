#!/usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script test_client.py
=====================
This script uses MCPTools to test the AgentOS as an MCP server.

Run:
uv run test_client.py
"""
# Standard library imports:
import asyncio
import sys
import uuid
from pathlib import Path
from textwrap import dedent

# Third-party imports:
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.tools.mcp import MCPTools

# Add the project root directory to the sys.path:
sys.path.append(str(Path(__file__).parent.parent))
# Local imports:
from config.settings import OPENAI_API_KEY
from config.ansi_colors import RED, BLUE, CYAN, GREEN, RESET, YELLOW
from config.logging_config import get_logger, setup_logging
from prompts_agent_os_and_mcp.prompts import MCP_COORDINATOR_PROMPT

setup_logging()
logger = get_logger(__name__)


class MCPTestClient:
    """Client MCP for interactive tests with AgentOS.

    Attributes:
        server_url: URL of the MCP server.
        user_id: ID of the user for persistent memory.
        session_id: ID of the session for context between messages.
        db: SQLite database for history and memory.
    """

    def __init__(
        self,
        server_url: str = "http://localhost:7777/mcp",
        user_id: str = "eddy-giusepe",
    ) -> None:
        """Initialize the MCP client.

        Args:
            server_url: URL of the MCP server.
            user_id: ID of the user for persistent memory.
        """
        # This is the URL of the MCP server we want to use:
        self.server_url: str = server_url
        # User ID fixed for persistent memory (same as the AgentOS):
        self.user_id: str = user_id
        # Session ID fixed for persistent context between messages:
        self.session_id: str = str(uuid.uuid4())
        # Setup the database to persist history and memory:
        self.db: SqliteDb = SqliteDb(db_file="tmp/client_memory.db")

    def _create_agent(self, mcp_tools: MCPTools) -> Agent:
        """Create and configure the agent with MCP tools.

        Args:
            mcp_tools: MCP tools connected to the server.

        Returns:
            Agent configured with model, tools and memory.
        """
        return Agent(
            user_id=self.user_id,  # User ID fixed for persistent memory
            session_id=self.session_id,  # Session ID fixed for persistent context
            db=self.db,  # Database to store history and memory
            model=OpenAIChat(
                api_key=OPENAI_API_KEY,
                id="gpt-5.2-2025-12-11",  # Using gpt-4o for better reasoning and delegation
                temperature=0.0,
                max_completion_tokens=1000,  # Increased to more complete and CoT reasoning responses
                instructions=dedent(MCP_COORDINATOR_PROMPT),
            ),
            tools=[mcp_tools],
            add_history_to_context=True,
            num_history_runs=5,  # Number of history runs to include in the context
            enable_user_memories=True,  # Enable user memories
            add_memories_to_context=True,
            enable_session_summaries=True,  # Enable session summaries
            add_session_summary_to_context=True,
            markdown=True,
        )

    def _log_welcome_message(self) -> None:
        """Display the welcome message in interactive mode."""
        logger.info(f"{RED}🤖 Interactive mode - Agent with MCP Server{RESET}")
        logger.info(f"{BLUE}User ID: {self.user_id}{RESET}")
        logger.info(
            f"{BLUE}Session ID: {self.session_id[:8]}... (active memory){RESET}"
        )
        logger.info(f"{YELLOW}Available agents:{RESET}")
        logger.info(
            f"{GREEN}  1. 🌐 web-research-agent: Web search with DuckDuckGo{RESET}"
        )
        logger.info(
            f"{GREEN}  2. 📚 knowledge-base-agent: Knowledge base search{RESET}"
        )
        logger.info(f"{CYAN}Enter your questions and press Enter.{RESET}")
        logger.info(f"{CYAN}To exit, enter 'exit', 'quit' or 'q'.{RESET}")

    async def _process_user_input(self, agent: Agent) -> bool:
        """Process the user input and return if it should continue.

        Args:
            agent: Agent configured to process the input.

        Returns:
            True to continue, False to exit.
        """
        user_input = input("\n👤 User: ").strip()

        # Check if the user wants to exit:
        if user_input.lower() in ["exit", "quit", "q"]:
            logger.info(f"{RED}👋 Ending interactive mode. Goodbye!{RESET}")
            return False

        # Ignore empty inputs:
        if not user_input:
            logger.warning(f"{RED}Please enter a question.{RESET}")
            return True

        # Process the question:
        logger.info(f"{GREEN}🤖 Agent response:{RESET}")
        await agent.aprint_response(input=user_input, stream=True, markdown=True)
        return True

    async def interactive_mode(self) -> None:
        """Interactive mode to chat with the agent."""
        self._log_welcome_message()

        try:
            async with MCPTools(
                transport="streamable-http",
                url=self.server_url,
                timeout_seconds=60,  # Increased to 60 seconds
            ) as mcp_tools:
                agent = self._create_agent(mcp_tools)

                while True:
                    try:
                        if not await self._process_user_input(agent):
                            break
                    except KeyboardInterrupt:
                        logger.info(
                            f"{RED}👋 Interrupted by user. Ending interactive mode...{RESET}"
                        )
                        break
                    except Exception as e:
                        logger.error(f"{RED}Error during processing: {e}{RESET}")
                        logger.info(f"{YELLOW}Try again or enter 'exit' to end.{RESET}")

        except ConnectionError as e:
            logger.error(f"{RED}Error connecting to MCP server: {e}{RESET}")
            logger.info(
                f"{YELLOW}Please ensure the MCP server is running at: {self.server_url}{RESET}"
            )
        except Exception as e:
            logger.error(f"{RED}Error initializing MCP agent: {e}{RESET}")
            logger.info(
                f"{YELLOW}Please ensure the MCP server is active and accessible. Try again or enter 'exit' to end.{RESET}"
            )

    def run(self) -> None:
        """Run the client in interactive mode."""
        asyncio.run(self.interactive_mode())


# Example usage:
if __name__ == "__main__":
    client = MCPTestClient()
    client.run()
