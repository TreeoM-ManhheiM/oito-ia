import os
import traceback

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

# Cliente Groq
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
Você é um professor especialista em ENEM, vestibulares e concursos.

Ao responder:

1. Explique o conceito principal.
2. Mostre como o tema costuma aparecer no ENEM.
3. Destaque palavras-chave importantes.
4. Crie um exemplo semelhante ao estilo do ENEM.
5. Dê uma dica de prova.
6. Use linguagem clara para alunos do Ensino Médio.

Estruture sempre a resposta assim:

📘 RESUMO
🔍 COMO CAI NO ENEM
✅ EXEMPLO
🎯 DICA DE PROVA
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
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
            max_tokens=1000
        )

        return {
            "resposta": response.choices[0].message.content
        }

    except Exception as e:

        erro_completo = traceback.format_exc()

        print("======== ERRO ========")
        print(erro_completo
