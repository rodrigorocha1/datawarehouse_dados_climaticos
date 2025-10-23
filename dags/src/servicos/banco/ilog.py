from abc import ABC, abstractmethod
from typing import Dict, Any


class Ilog(ABC):

    @abstractmethod
    def log_info_sql(
            self,
            msg: str,
            tabela: str, colunas: str,
            parametros: Dict[str, Any],
            **kwags,
    ):
        pass
