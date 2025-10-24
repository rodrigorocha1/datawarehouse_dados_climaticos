import os
import inspect


class ExemploClasse:
    def metodo(self):
        # Nome do arquivo
        nome_arquivo = os.path.basename(__file__)

        # Frame atual
        frame = inspect.currentframe()

        # Nome do método/função
        nome_funcao = frame.f_code.co_name

        # Número da linha
        numero_linha = frame.f_lineno

        # Nome do método da classe
        nome_metodo_classe = self.__class__.__name__ + "." + nome_funcao

        print(f"Arquivo: {nome_arquivo}")
        print(f"Função/método: {nome_funcao}")
        print(f"Linha: {numero_linha}")
        print(f"Método da classe: {nome_metodo_classe}")


# Teste
obj = ExemploClasse()
obj.metodo()
