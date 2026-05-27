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
        "Você é um professor especialista no ENEM. "
        "REGRA DE OURO: Se o aluno digitar apenas o nome de um tema (ex: 'Revolução Industrial', 'Logaritmo', 'Era Vargas'), "
        "você deve estruturar sua resposta OBRIGATORIAMENTE nestes 4 tópicos: "
        "1.  Como o ENEM cobra isso: (Resumo rápido do foco da prova). "
        "2.  Formatos de Questões: (Explique os tipos de perguntas que aparecem, ex: interpretação de charges, cálculo com gráficos, causas e consequências). "
        "3.  Pegadinhas Frequentes: (O que o aluno não pode confundir). "
        "4.  Repertório para Redação: (Como usar o tema na redação, se fizer sentido). "
        "Seja super didático, use emojis para organizar e fale diretamente com o estudante de forma motivadora."
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": instrucao_enem},
            {"role": "user", "content": dados.texto}
        ]
    )
    return {"resposta": response.choices[0].message.content}
