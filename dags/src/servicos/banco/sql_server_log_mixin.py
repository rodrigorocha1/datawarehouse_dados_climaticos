from typing import Dict, Any

from airflow.utils.log.logging_mixin import LoggingMixin

from dags.src.config.config import Config
from dags.src.servicos.banco.ilog import Ilog
from dags.src.servicos.banco.operacao_banco_sqlserver import OperacaoBancoSQLServer


class SqlServerLogMixin(Ilog, LoggingMixin, OperacaoBancoSQLServer):

    def __init__(self):
        self.__mssql_conn_id = Config.ID_BANCO_LOG
        super().__init__(id_conexao=self.__mssql_conn_id)

    def log_info_sql(
            self,
            msg: str,
            tabela: str, colunas: str,
            parametros: Dict[str, Any],
            **kwags,
    ):
        self.log.info(msg, **kwags)
        placeholders = ", ".join([f"%({coluna})s" for coluna in colunas])
        sql_banco = f"""
            INSERT INTO {tabela} ({colunas})
            VALUES ({placeholders})
        """

        self.realizar_operacao_banco(consulta=sql_banco, parametros=parametros)
