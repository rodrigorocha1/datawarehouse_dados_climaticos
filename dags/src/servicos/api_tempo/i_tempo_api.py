from abc import ABC, abstractmethod
from typing import Dict


class ITempoAPI(ABC):

    @abstractmethod
    def buscar_dados_tempo(self, cidade: str, **kwargs) -> Dict:
        pass
