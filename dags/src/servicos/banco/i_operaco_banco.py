from abc import ABC, abstractmethod
from typing import Dict, Any


class IOperacaoBanco(ABC):

    @abstractmethod
    def realizar_operacao_banco(self, consulta: str, parametros: Dict[str, Any]):
        """
        Método para realizar consulta no banco
        :param consulta: realizar consulta
        :type consulta: str
        :param parametros: parâmetros
        :type parametros: Dict[str, Any]
        :return:
        :rtype:
        """
        pass

