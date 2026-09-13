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

Formate sempre a resposta com:

📘 RESUMO
🔍 COMO CAI NO ENEM
✅ EXEMPLO
🎯 DICA DE PROVA
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": instrucao_enem},
                {"role": "user", "content": dados.texto}
            ]
        )

        return {
            "resposta": response.choices[0].message.content
        }

    except Exception as e:
        return {
            "erro": str(e),
            "tipo": type(e).__name__,
            "detalhes": traceback.format_exc()
        }
