import os

def dicionario_caminho_dados(pasta):
    base_path = os.path.dirname(os.path.abspath(__file__))
    caminhos = {
        "Pasta": os.path.join(base_path, "Dados por Grupos Vulneráveis")
    }
    return caminhos[pasta]