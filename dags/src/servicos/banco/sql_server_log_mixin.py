import json
import logging

from dags.src.config.config import Config
from dags.src.servicos.banco.ilog import Ilog
from dags.src.servicos.banco.operacao_banco_sqlserver import OperacaoBancoSQLServer


class SqlServerLogMixin(Ilog, OperacaoBancoSQLServer):

    def __init__(self):
        self.__mssql_conn_id = Config.ID_BANCO_LOG
        super().__init__(id_conexao=self.__mssql_conn_id)

    def emit(self, record: logging.LogRecord):
        # Mensagem formatada (opcional, pode ser usada como 'Consulta')
        consulta = getattr(record, "consulta", None)
        kwargs = getattr(record, "kwargs", {})

        url = kwargs.pop('url', None)
        codigo = kwargs.pop('codigo', None)
        json_retorno = kwargs.pop('json_retorno', None)

        # Colunas adicionais como JSON
        parametros_adicionais = json.dumps(kwargs) if kwargs else None

        sql = """
        INSERT INTO dbo.LogOperacoesBanco
        (Consulta, Nome, NomeArquivo, Funcao, NumeroLinha, url, Codigo, JsonRetorno, NIVEL_LOG)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        params = (
            consulta,
            record.name,
            record.filename,
            record.funcName,
            record.lineno,
            url,
            codigo,
            str(json_retorno) if json_retorno else None,
            record.levelname
        )

        self.realizar_operacao_banco(consulta=sql, parametros=params)