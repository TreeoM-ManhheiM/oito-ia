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

@app.post("/perguntar")
def perguntar_ia(dados: Mensagem):
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": instrucao_enem},
                {"role": "user", "content": dados.texto}
            ]
        )

        return {
            "resposta": response.choices[0].message.content
        }

    except Exception as e:
        import traceback

        erro = traceback.format_exc()
        print(erro)

        return {
            "erro": str(e),
            "detalhes": erro
        }
    return {"resposta": response.choices[0].message.content}
