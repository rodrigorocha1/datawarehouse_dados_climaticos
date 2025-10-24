from typing import Any, Dict, Union, Tuple

from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook

from dags.src.servicos.banco.i_operaco_banco import IOperacaoBanco


class OperacaoBancoSQLServer(IOperacaoBanco):

    def __init__(self, id_conexao: str):
        self.__id_conexao = id_conexao
        self.__mssql_hook = MsSqlHook(mssql_conn_id=self.__id_conexao)

    def realizar_operacao_banco(
        self,
        consulta: str,
        parametros: Union[Dict[str, Any], Tuple[Any, ...]]
    ) -> None:

        if isinstance(parametros, tuple):
            parametros_generic: tuple[Any, ...] = parametros
            self.__mssql_hook.run(sql=consulta, parameters=parametros_generic)
        else:
            self.__mssql_hook.run(sql=consulta, parameters=parametros)
