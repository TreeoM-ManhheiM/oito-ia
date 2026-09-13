import os
import traceback

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


class Mensagem(BaseModel):
    texto: str


@app.get("/")
def pagina_inicial():
    return FileResponse("index.html")


@app.get("/teste")
def teste():
    return {
        "status": "online",
        "groq_key_configurada": os.environ.get("GROQ_API_KEY") is not None
    }


@app.post("/perguntar")
def perguntar_ia(dados: Mensagem):
    try:

        instrucao_enem = """
Você é um professor especialista em ENEM.

Sempre responda exatamente nesta estrutura:

📘 RESUMO
Explique o conteúdo de forma simples.

🔍 COMO CAI NO ENEM
Mostre como o tema costuma aparecer na prova.

✅ EXEMPLO
Crie um exemplo semelhante ao estilo ENEM.

🎯 DICA DE PROVA
Dê um macete ou dica para acertar questões.

Use linguagem clara para alunos do Ensino Médio.
"""

        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": instrucao_enem
                },
                {
                    "role": "user",
                    "content": dados.texto
                }
            ],
            temperature=0.7,
            max_tokens=1200
        )

        resposta = response.choices[0].message.content

        return {
            "resposta": resposta
        }

    except Exception as e:

        erro_completo = traceback.format_exc()

        print(erro_completo)

        return {
            "resposta": f"Erro: {str(e)}"
        }
