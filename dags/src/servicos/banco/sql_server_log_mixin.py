import json
import logging
from typing import Dict, Any

from dags.src.config.config import Config
from dags.src.servicos.banco.ilog import Ilog
from dags.src.servicos.banco.operacao_banco_sqlserver import OperacaoBancoSQLServer


class SqlServerLogMixin(Ilog,  OperacaoBancoSQLServer):

    def __init__(self):
        self.__mssql_conn_id = Config.ID_BANCO_LOG
        super().__init__(id_conexao=self.__mssql_conn_id)

    def emit(self, record: logging.LogRecord):
        mensagem = self.format(record)
        kwargs = getattr(record, "kwargs", {})
        url = kwargs.pop('url', None)

        parametros = json.dumps(kwargs) if kwargs else None
        log_level = record.levelname