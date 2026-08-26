# Unit 1 — smolagents (Hugging Face Agents Course)

Projeto simples para aprender o funcionamento de um Agente de IA usando a
biblioteca [smolagents](https://github.com/huggingface/smolagents), rodando
100% local (sem Docker, sem Hugging Face Spaces).

## Arquivos

- `agent.py` — define o `CodeAgent`, duas tools customizadas e roda uma
  pergunta de teste no terminal.
- `agent_ui.py` — mesmo agente, exposto numa interface de chat web (Gradio).
- `requirements.txt` — dependências do projeto.

## 1. Criar e ativar o ambiente virtual

O `venv` já foi criado na pasta `venv/`. Para ativá-lo:

**PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

**cmd.exe:**

```cmd
venv\Scripts\activate.bat
```

Se ainda não existir (ou quiser recriar), gere-o com:

```powershell
python -m venv venv
```

## 2. Instalar as dependências

Com o ambiente virtual ativado:

```powershell
pip install -r requirements.txt
```

## 3. Configurar o `.env` com o seu token

Crie um arquivo `.env` na raiz do projeto com o seu token da Hugging Face
(`https://huggingface.co/settings/tokens`):

```
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

O arquivo `.env` já está listado no `.gitignore` — ele nunca deve ser
commitado no Git.

## 4. Rodar o agente no terminal

```powershell
python agent.py
```

Isso executa uma pergunta de teste e imprime no terminal cada passo do
ciclo **Thought → Action → Observation** (graças a `verbosity_level=2`),
até a resposta final.

## 5. Rodar o agente com interface de chat (Gradio)

```powershell
python agent_ui.py
```

Isso abre um servidor local (por padrão em `http://127.0.0.1:7860`) — abra
esse endereço no navegador para conversar com o agente numa interface de
chat.

## As duas tools disponíveis

- `get_current_time_in_timezone(timezone)` — retorna a hora atual num fuso
  horário (ex: `"Asia/Tokyo"`, `"America/Sao_Paulo"`).
- `convert_temperature(value, from_unit, to_unit)` — converte temperaturas
  entre Celsius, Fahrenheit e Kelvin.

Experimente perguntar coisas como:

- "Que horas são em Lisboa agora?"
- "Quanto é 100°F em Celsius?"
- "Que horas são em Nova York e quanto é 0°C em Kelvin?"
