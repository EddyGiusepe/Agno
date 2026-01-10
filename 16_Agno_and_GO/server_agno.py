#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Server_agno.py
==============
This script implements a REST API using FastAPI that exposes an intelligent agent
called AnimeBot. The agent uses the Agno framework to create a conversational assistant
with advanced memory capabilities and integration with external APIs.

MAIN FEATURES
--------------
✓ Conversational intelligent agent with GPT-5.2-2025-12-11 model
✓ Integration with Jikan API for queries about anime and manga
✓ Persistence of history and memory using SQLite
✓ Support for real-time streaming responses
✓ User memory and session summaries automatically
✓ Responses in English (en-US)

USED TECHNOLOGIES
------------------
• Agno: Framework for creating intelligent agents
• FastAPI: Modern and high-performance web framework
• OpenAI GPT-5.2-2025-12-11: Modelo de linguagem para o agente
• SQLite: Database for memory persistence
• Jikan API: Public API for anime and manga data

RUN
---
uvicorn server_agno:app --reload --port 8000

INTEGRATION WITH GO
===================
This server was designed to be consumed by Go clients. See the file
client_golang.go for an example of client implementation.
"""
import sys
from pathlib import Path
from textwrap import dedent

# Add the parent directory to the path to import config:
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from agno.agent import Agent
from agno.tools.api import CustomApiTools
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb
from config.settings import OPENAI_API_KEY


app = FastAPI(
    title="An intelligent agent called AnimeBot API",
    description="Queries about anime (Jikan API) and other general topics.",
    version="1.0.0",
    contact={
        "name": "An intelligent agent called AnimeBot",
        "url": "https://github.com/EddyGiusepe",
        "email": "eddychirinos.unac@gmail.com",
    },
    license={"name": "MIT License", "url": "https://opensource.org/licenses/MIT"},
)

# Configuring the SQLite database:
db = SqliteDb(
    db_file="agent_memory.db",
)

# Creating the agent:
agent = Agent(
    model=OpenAIChat(
        id="gpt-5.2-2025-12-11",
        api_key=OPENAI_API_KEY,
        temperature=0.0,
        max_completion_tokens=700,  # Increased to more complete and CoT reasoning responses
    ),
    db=db,  # Adds the database to the agent
    tools=[CustomApiTools(base_url="https://api.jikan.moe/v4")],
    add_history_to_context=True,  # Now the history will be stored in the SQLite database
    num_history_runs=5,  # Number of history runs to include in the context
    enable_user_memories=True,
    add_memories_to_context=True,  # Now the memories will be stored in the SQLite database
    enable_session_summaries=True,
    add_session_summary_to_context=True,
    markdown=True,
    instructions=dedent(
        """
    You are an intelligent and versatile assistant called AnimeBot.
    You respond educatively, greet the user and always respond in English (en-US).
    
    ## Your Abilities:
    
    1. **General Knowledge**: Respond to any topic (science, history, technology, mathematics, etc.)
       using your knowledge.
    
    2. **Expert in Anime**: Use the Jikan API to search for updated information about anime, manga
       and characters.
    
    ## Available Jikan API endpoints:
    
    - GET /anime?q={name} - Search anime by name
    - GET /anime/{id} - Details of an anime
    - GET /random/anime - Return a random anime
    - GET /top/anime - Top anime of all time
    - GET /seasons/now - Anime of the current season
    - GET /anime/{id}/characters - Characters of an anime
    
    ## Guidelines:
    - Use the API when you need updated information about anime
    - Use your general knowledge for other topics
    - Always respond in English (en-US)
    - Be polite, friendly, factual and informative
    """
    ),
)


class QueryRequest(BaseModel):
    message: str = Field(
        ...,
        description="The message to be sent to the agent",
        min_length=1,
        max_length=1000,
    )


class QueryResponse(BaseModel):
    response: str = Field(
        ..., description="The response from the agent", min_length=1, max_length=1000
    )


@app.post("/chat", response_model=QueryResponse)
async def chat(request: QueryRequest):
    """Endpoint without streaming - complete response"""
    response = agent.run(request.message)
    return QueryResponse(response=str(response.content))


@app.post("/chat/stream")
async def chat_stream(request: QueryRequest):
    """Endpoint with streaming - gradual response"""

    def generate():
        for chunk in agent.run(
            request.message,
            stream=True,
        ):
            if hasattr(chunk, "content") and chunk.content:
                yield chunk.content

    return StreamingResponse(generate(), media_type="text/plain")


@app.get("/health")
async def health():
    """Health check"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
