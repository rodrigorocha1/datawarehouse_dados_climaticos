from .servicos.api_tempo.i_tempo_api import ITempoAPI
from .servicos.banco.i_operaco_banco import IOperacaoBanco

class EtlTempo:
    def __init__(self, servico_api: ITempoAPI, operacao_banco = IOperacaoBanco):
        self.__servico_api = servico_api
        self.__operacao_banco = operacao_banco

    def gravar_dados_tabela_temporaria(self, cidade, **kwargs):
        dados = self.__servico_api.buscar_dados_tempo(cidade, **kwargs)
        valores = {
            'ID_CIDADE': dados['id'],
            'NOME': dados['name'],
            'TEMP': dados['main']['temp'],
            'PRESSAO': dados['main']['pressure'],
            'HUMIDADE': dados['main']['humidity'],
            'VELOCIDADE_VENTO': dados['wind']['speed'],
            'ANGULO_VENTO': dados['wind']['deg'],
        }
        tabela = 'STG_DADOS_TEMPO'
        placeholders = ", ".join(
            [f"%({coluna})s" for coluna in valores.keys()])
        sql_banco = f"""
                                    INSERT INTO {tabela}
                                    VALUES ({placeholders})
                                """

        self.__operacao_banco.realizar_operacao_banco(consulta=sql_banco, parametros=valores)
