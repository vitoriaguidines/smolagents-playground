"""
Mesmo agente definido em agent.py, mas exposto numa interface de chat web
(Gradio) em vez de rodar uma única pergunta fixa no terminal.
"""

from smolagents import GradioUI
from agent import agent

if __name__ == "__main__":
    GradioUI(agent).launch()
