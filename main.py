import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

# 💡 O PULO DO GATO: Continuamos usando a biblioteca OpenAI, 
# mas apontamos para o servidor gratuito do Groq!
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
    response = client.chat.completions.create(
        model="llama3-8b-8192", # Modelo super inteligente e gratuito da Meta
        messages=[{"role": "user", "content": dados.texto}]
    )
    return {"resposta": response.choices[0].message.content}