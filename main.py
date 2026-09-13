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
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um professor especialista em Python."
                },
                {
                    "role": "user",
                    "content": dados.texto
                }
            ]
        )

        return {
            "resposta": response.choices[0].message.content
        }

    except Exception as e:
        return {
            "erro": str(e),
            "tipo": type(e).__name__
        }
        
        return {
            "resposta": response.choices[0].message.content
        }

    except Exception as e:
        erro_completo = traceback.format_exc()

        print("======== ERRO ========")
        print(erro_completo)
        print("======================")

        return {
            "erro": str(e),
            "tipo": type(e).__name__,
            "detalhes": erro_completo
        }
