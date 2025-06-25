#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script demo.py
=====================
Este script demonstra o uso do agente de assistência de receitas criado 
no script setup_agent.py.

Run
---
uv run demo.py
"""
from setup_agent import recipe_agent
from agno.playground import Playground, serve_playground_app

agent = recipe_agent()

#app = Playground(agents=[agent]).get_app()
#if __name__ == '__main__':
#    serve_playground_app('demo:app', reload=True)

while True:
    query = input("Digite sua consulta: ")
    if query.lower() in ["sair", "exit", "quit"]:
        break
    agent.print_response(query, stream=True)