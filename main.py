import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

# Configuração da API do Groq (utilizando a biblioteca padrão da OpenAI)
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
    # Definindo as instruções de comportamento da IA como especialista do ENEM
    instrucao_enem = (
        "Você é um professor de cursinho brasileiro, mentor e especialista absoluto no ENEM. "
        "Suas respostas devem ser extremamente didáticas, organizadas e focadas em como o assunto "
        "é cobrado nas matrizes de referência do ENEM. Sempre que fizer sentido, dê dicas de como "
        "usar o tema como repertório sociocultural na Redação, cite eixos temáticos ou dê macetes "
        "de resolução de questões. Use uma linguagem encorajadora, clara e use quebras de linha "
        "e tópicos para deixar a leitura fácil para o estudante."
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", # Modelo atualizado, robusto e gratuito do Groq
        messages=[
            {"role": "system", "content": instrucao_enem}, # O "cérebro" assume a profissão aqui
            {"role": "user", "content": dados.texto}        # A pergunta que o estudante digitou
        ]
    )
    return {"resposta": response.choices[0].message.content}
