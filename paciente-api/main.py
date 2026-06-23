from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from database import select_operation
from connection_api import create_connection


app = FastAPI()


@app.get("/pacientes/")
async def busca_pacientes():
    """
    Retorna uma lista com todos os pacientes cadastrados.
    """

    connection = create_connection()

    if connection is None:
        raise HTTPException(
            status_code=500,
            detail="Erro na conexão com banco de dados."
        )


    pacientes = select_operation(
        connection,
        "paciente"
    )


    return JSONResponse(
        content=pacientes,
        status_code=200
    )



@app.get("/pacientes/{id}")
async def busca_paciente(id: str):
    """
    Retorna um paciente pelo UUID.
    """

    connection = create_connection()

    if connection is None:
        raise HTTPException(
            status_code=500,
            detail="Erro na conexão com banco de dados."
        )


    try:

        paciente = select_operation(
            connection,
            "paciente",
            id
        )

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="ID inválido."
        )


    if not paciente:

        raise HTTPException(
            status_code=404,
            detail="Paciente não encontrado."
        )


    return JSONResponse(
        content=paciente,
        status_code=200
    )