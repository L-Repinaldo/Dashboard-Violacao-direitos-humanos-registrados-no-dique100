import os

def dicionario_caminho_dados(pasta):

    base_path = os.path.dirname(os.path.abspath(__file__))  # diretório do script
    caminhos = {
        "Pasta": os.path.join(base_path, "Dados", "Dados por Grupos Vulneráveis")
    }
    return caminhos[pasta]


