from typing import Any, Dict, Union

from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
from sqlalchemy.sql.elements import Tuple

from dags.src.servicos.banco.i_operaco_banco import IOperacaoBanco


class OperacaoBancoSQLServer(IOperacaoBanco):

    def __init__(self, id_conexao: str):
        self.__id_conexao = id_conexao
        self.__msqql_hook = MsSqlHook(MsSqlHook(mssql_conn_id=self.__id_conexao))

    def realizar_operacao_banco(self, consulta: str, parametros: Union[Dict[str, Any], Tuple]):
        self.__msqql_hook.run(sql=consulta, parameters=parametros)
