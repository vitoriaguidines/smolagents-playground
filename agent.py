"""
Agente de IA simples usando smolagents (Hugging Face Agents Course - Unidade 1).

Fluxo Thought -> Action -> Observation (o "loop" de um agente):
  1. Thought: o LLM recebe a pergunta + a lista de tools disponíveis e
     "pensa" em texto sobre o que fazer a seguir.
  2. Action: no CodeAgent, a Action é sempre um trecho de código Python que
     o próprio modelo escreve (podendo chamar as tools abaixo como funções
     normais de Python).
  3. Observation: o smolagents executa esse código de verdade num
     interpretador Python, e o que for impresso/retornado volta para o
     modelo como "observação".
  Esse ciclo se repete (é um agente "multi-step") até o modelo chamar
  final_answer(...) dentro do código, ou até atingir max_steps.
"""

from datetime import datetime

import pytz
from dotenv import load_dotenv
from smolagents import CodeAgent, InferenceClientModel, tool

# Lê o arquivo .env e injeta suas variáveis (HF_TOKEN=...) no ambiente do
# processo. Precisa rodar ANTES de criar o InferenceClientModel, pois ele lê
# o token de os.environ["HF_TOKEN"] automaticamente.
load_dotenv()


@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """Retorna a hora atual em um fuso horário específico.

    Args:
        timezone: Nome do fuso horário no formato pytz, por exemplo
            "America/Sao_Paulo", "Europe/Lisbon" ou "Asia/Tokyo".
    """
    # Importante: essa docstring não é só para humanos. O smolagents lê o
    # nome da função, os type hints e a docstring para montar a descrição
    # da tool que é enviada ao LLM. É assim que o modelo "sabe" que essa
    # tool existe, o que ela faz e quais argumentos passar.
    try:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"A hora atual em {timezone} é {now}."
    except Exception as e:
        return f"Erro ao buscar o fuso horário '{timezone}': {e}"


@tool
def convert_temperature(value: float, from_unit: str, to_unit: str) -> str:
    """Converte uma temperatura entre Celsius, Fahrenheit e Kelvin.

    Args:
        value: Valor numérico da temperatura a converter.
        from_unit: Unidade de origem: "celsius", "fahrenheit" ou "kelvin".
        to_unit: Unidade de destino: "celsius", "fahrenheit" ou "kelvin".
    """
    units = {"celsius", "fahrenheit", "kelvin"}
    from_unit = from_unit.strip().lower()
    to_unit = to_unit.strip().lower()

    if from_unit not in units or to_unit not in units:
        return f"Unidades suportadas: {', '.join(sorted(units))}."

    # Normaliza sempre para Celsius primeiro, depois converte para o alvo.
    if from_unit == "fahrenheit":
        celsius = (value - 32) * 5 / 9
    elif from_unit == "kelvin":
        celsius = value - 273.15
    else:
        celsius = value

    if to_unit == "fahrenheit":
        result = celsius * 9 / 5 + 32
    elif to_unit == "kelvin":
        result = celsius + 273.15
    else:
        result = celsius

    return f"{value}° {from_unit} = {round(result, 2)}° {to_unit}."


# InferenceClientModel fala com a Inference API da Hugging Face. Ele lê
# HF_TOKEN do ambiente (carregado pelo load_dotenv() acima) para autenticar
# as chamadas ao modelo indicado em model_id.
model = InferenceClientModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct")

# CodeAgent junta o modelo + a lista de tools disponíveis. A cada passo do
# loop Thought-Action-Observation, ele monta um prompt com: a pergunta
# original, o histórico de passos anteriores e a descrição de cada tool
# (gerada automaticamente a partir dos decorators @tool acima).
agent = CodeAgent(
    tools=[get_current_time_in_timezone, convert_temperature],
    model=model,
    # Limita quantos ciclos Thought-Action-Observation o agente pode fazer
    # antes de ser forçado a responder — evita loops infinitos.
    max_steps=6,
    # verbosity_level=2 imprime no terminal cada Thought/Action/Observation,
    # ótimo para estudar o fluxo enquanto você aprende.
    verbosity_level=2,
)


if __name__ == "__main__":
    # Pergunta de teste propositalmente pensada para exigir as DUAS tools,
    # assim dá pra observar o agente decidindo (Thought) quais chamar e em
    # que ordem (Action), uma por passo.
    pergunta = (
        "Que horas são agora em Tóquio (Asia/Tokyo)? "
        "E quanto é 30 graus Celsius em Fahrenheit?"
    )
    resposta = agent.run(pergunta)
    print("\n=== Resposta final do agente ===")
    print(resposta)
