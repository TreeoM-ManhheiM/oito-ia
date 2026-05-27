import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

# Inicializa a OpenAI pegando a chave das Variáveis de Ambiente do Render
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class Mensagem(BaseModel):
    texto: str

#  ROTA 1: Entrega o seu arquivo index.html na página inicial
@app.get("/")
def pagina_inicial():
    return FileResponse("index.html")

#  ROTA 2: Recebe a pergunta do JavaScript e envia para a OpenAI
@app.post("/perguntar")
def perguntar_ia(dados: Mensagem):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": dados.texto}]
    )
    return {"resposta": response.choices[0].message.content}