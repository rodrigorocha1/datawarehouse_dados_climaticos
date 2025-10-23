from typing import Dict

import requests

from dags.src.config.config import Config
from dags.src.servicos.api_tempo.i_tempo_api import ITempoAPI


class TempoApi(ITempoAPI):

    def __init__(self):
        self.__url_api = Config.URL_OPEN_API
        self.__key_api = Config.KEY_OPEN_API
        self.__units = Config.UNITS_OPEN_API
        self.__langs = Config.LANG_OPEN_API

    def buscar_dados_tempo(self, cidade: str) -> Dict:
        params = {
            'appid': self.__key_api,
            'units': self.__units,
            'lang': self.__langs,
            'q': f'{cidade}, BR'
        }

        data = requests.get(url=self.__url_api, params=params)
        req = data.json()

        return req


if __name__ == '__main__':
    ta = TempoApi()
    dados = ta.buscar_dados_tempo(cidade='Ribeirão Preto, BR')
    print(dados)
