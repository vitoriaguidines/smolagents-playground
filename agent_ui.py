"""
Mesmo agente definido em agent.py, mas exposto numa interface de chat web
(Gradio) em vez de rodar uma única pergunta fixa no terminal.

Reaproveitamos a instância `agent` já configurada em agent.py (mesmo model,
mesmas tools) para não duplicar a definição das tools em dois arquivos.
"""

from smolagents import GradioUI

# Importar `agent` de agent.py NÃO executa a pergunta de teste daquele
# arquivo, porque ela está dentro do bloco `if __name__ == "__main__":`
# de agent.py — esse bloco só roda quando agent.py é executado diretamente.
from agent import agent

if __name__ == "__main__":
    # Abre uma interface de chat local no navegador (por padrão em
    # http://127.0.0.1:7860). Cada mensagem que você enviar dispara o mesmo
    # loop Thought-Action-Observation, mas mostrado numa UI de chat em vez
    # do terminal.
    GradioUI(agent).launch()
