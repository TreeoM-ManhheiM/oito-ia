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


@app.get("/modelos")
def listar_modelos():
    try:
        modelos = client.models.list()

        return {
            "modelos": [m.id for m in modelos.data]
        }

    except Exception as e:
        return {
            "erro": str(e)
        }


@app.post("/perguntar")
def perguntar_ia(dados: Mensagem):
    try:

        instrucao_enem = """
Você é um professor especialista em ENEM, vestibulares e concursos.

Sempre responda exatamente nesta estrutura:

📘 RESUMO
Explique o conteúdo de forma simples e objetiva.

🔍 COMO CAI NO ENEM
Explique como o tema costuma aparecer nas provas.

✅ EXEMPLO
Crie um exemplo semelhante ao estilo ENEM.

🎯 DICA DE PROVA
Dê uma dica prática para o aluno acertar questões.

Utilize linguagem clara para estudantes do Ensino Médio.
"""

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
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

        return {
            "resposta": response.choices[0].message.content
        }

    except Exception as e:

        erro_completo = traceback.format_exc()

        print("========== ERRO ==========")
        print(erro_completo)
        print("==========================")

        return {
            "erro": str(e),
            "tipo": type(e).__name__,
            "detalhes": erro_completo
        }
