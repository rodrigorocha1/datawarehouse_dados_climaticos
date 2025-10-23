from airflow.utils.log.logging_mixin import LoggingMixin

from dags.src.servicos.banco.i_operaco_banco import IOperacaoBanco
from dags.src.servicos.banco.operacao_banco_sqlserver import OperacaoBancoSQLServer


class SqlServerLogMixin(LoggingMixin, OperacaoBancoSQLServer):

    def __init__(self, ):

