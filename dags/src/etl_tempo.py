from .servicos.api_tempo.i_tempo_api import ITempoAPI


class EtlTempo:
    def __init__(self, servico_api: ITempoAPI):
        self.__servico_api = servico_api

    def gravar_dados_tabela_temporaria(self, cidade, **kwargs):
        dados = self.__servico_api.buscar_dados_tempo(cidade, **kwargs)
        print(dados)
