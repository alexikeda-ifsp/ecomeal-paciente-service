from fastapi import FastAPI
from fastapi.responses import JSONResponse
from database import select_operation
from connection_api import create_connection
from fastapi import HTTPException
from supabase.client import AuthApiError

app = FastAPI()

@app.get("/pacientes/")
async def busca_pacientes():
    """
    Retorna uma Lista de Objetos Paciente, que são todos os pacientes
    registrados no Banco de Dados. Se não houver, é retornado uma Lista vazia.
    """
    client = create_connection()
    if client is None:
        raise HTTPException(
            status_code=500,
            detail="Erro na Conexão com o Banco de Dados."
        )
    pacientes = select_operation(client,"paciente")
    return JSONResponse(content=pacientes, status_code=200)



@app.get("/pacientes/{id}")
async def busca_paciente(id:str):
    """
    Busca o paciente pelo ID, retornando um Objeto Paciente.
    Se não for encontrado, é retornando 404.
    """
    client = create_connection()
    if client is None:
        raise HTTPException(
            status_code=500,
            detail="Erro na Conexão com o Banco de Dados."
        )
    try:
        paciente = select_operation(client, "paciente",id)
    except Exception as e:
        if e.code == "22P02":
            raise HTTPException(status_code=400, detail="ID deve estar no formato UUID. ID fornecido é Inválido")
    if not paciente:
        raise HTTPException(status_code=404,detail="Paciente não encontrado.")
    return JSONResponse(content=paciente, status_code=200)


