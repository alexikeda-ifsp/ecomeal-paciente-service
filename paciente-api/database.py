from psycopg2.extras import RealDictCursor


def select_operation(connection, table, id_paciente=None):
    """
    Executa SELECT no PostgreSQL e retorna
    dicionários compatíveis com JSONResponse.
    """

    if table is None:
        raise Exception("Tabela não encontrada.")


    cursor = connection.cursor(
        cursor_factory=RealDictCursor
    )


    try:

        if id_paciente is not None:

            cursor.execute(
                f"""
                SELECT *
                FROM {table}
                WHERE id = %s
                """,
                (id_paciente,)
            )

            result = cursor.fetchone()


        else:

            cursor.execute(
                f"""
                SELECT *
                FROM {table}
                """
            )

            result = cursor.fetchall()


        return result


    finally:

        cursor.close()
        connection.close()