import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

# Configuração da API do Groq
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

class Mensagem(BaseModel):
    texto: str

@app.get("/")
def pagina_inicial():
    return FileResponse("index.html")

@app.post("/perguntar")
def perguntar_ia(dados: Mensagem):
    # O "Cochicho" turbinado com o filtro automático de formatos de questões!
    instrucao_enem = (
        "Você é um professor especialista na Programação em Python"
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": instrucao_enem},
            {"role": "user", "content": dados.texto}
        ]
    )
    return {"resposta": response.choices[0].message.content}
