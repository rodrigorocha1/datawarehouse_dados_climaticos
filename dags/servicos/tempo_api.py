from typing import Dict

import requests

from dags.config.config import Config
from dags.servicos.i_tempo_api import ITempoAPI


class TempoApi(ITempoAPI):

    def __init__(self):
        self.__url_api = Config.URL_API
        self.__key_api = Config.KEY_API

    def buscar_dados_tempo(self, cidade: str) -> Dict:
        params = {
            'appid': self.__key_api,
            'units': 'metric',
            'lang': 'pt_br',
            'q': f'{cidade}, BR'
        }

        data = requests.get(url=self.__url_api, params=params)
        req = data.json()
        return req
