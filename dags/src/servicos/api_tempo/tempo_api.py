import inspect
import json
import os
from typing import Dict

import requests
from requests.exceptions import HTTPError
from src.config.config import Config
from src.servicos.api_tempo.i_tempo_api import ITempoAPI
from src.servicos.banco.i_operaco_banco import IOperacaoBanco
from unidecode import unidecode


class TempoApi(ITempoAPI):

    def __init__(self):
        self.__url_api = Config.URL_OPEN_API
        self.__key_api = Config.KEY_OPEN_API
        self.__units = Config.UNITS_OPEN_API
        self.__langs = Config.LANG_OPEN_API
        self.__log_banco = IOperacaoBanco

    def buscar_dados_tempo(self, cidade: str, **kwargs) -> Dict:
        params = {
            'appid': self.__key_api,
            'units': self.__units,
            'lang': self.__langs,
            'q': f'{cidade}, BR'
        }
        try:
            data = requests.get(url=self.__url_api, params=params)
            data.raise_for_status()
            req = data.json()
            json_retorno_str = json.dumps(req, ensure_ascii=False)

            frame = inspect.currentframe()

            erro = {
                'Consulta': None,
                'Nome': os.path.basename(__file__),
                'NomeArquivo': os.path.basename(__file__),
                'Funcao': self.__class__.__name__ + "." + (frame.f_code.co_name if frame else ''),
                'NumeroLinha': frame.f_lineno if frame else None,
                'url': self.__url_api + data.request.path_url,
                'Codigo': data.status_code,
                'JsonRetorno': json_retorno_str,
                'Mensagem': 'Sucesso ao Conectar na API',
                'NIVEL_LOG': 'INFO'
            }

            kwargs['ti'].xcom_push(
                key=f'mensagem_log_sucesso_{unidecode(cidade.lower().replace(",", "_", ).replace(" ", "_"))}',
                value=erro)

            return req

        except HTTPError as http_error:
            exc_frame = http_error.__traceback__.tb_frame if http_error.__traceback__ else None
            erro = {
                'Consulta': None,
                'Nome': os.path.basename(__file__),
                'NomeArquivo': os.path.basename(__file__),
                'Funcao': self.__class__.__name__ + "." + (exc_frame.f_code.co_name if exc_frame else ''),
                'NumeroLinha': exc_frame.f_lineno if exc_frame else None,
                'url': http_error.response.request.url if http_error.response else None,
                'Codigo': http_error.response.status_code if http_error.response else None,
                'JsonRetorno': None,
                'Mensagem': f'Erro HTTP ao buscar dados do tempo para {cidade}',
                'NIVEL_LOG': 'ERROR'
            }

            kwargs['ti'].xcom_push(
                key=f'mensagem_log_erro_{unidecode(cidade.lower().replace(",", "_", ).replace(" ", "_"))}', value=erro)

            raise RuntimeError(f"Falha ao buscar dados do tempo para {cidade}") from http_error


if __name__ == '__main__':
    ta = TempoApi()
    dados = ta.buscar_dados_tempo(cidade='Ribeirão Preto, BR')
    print(dados)
