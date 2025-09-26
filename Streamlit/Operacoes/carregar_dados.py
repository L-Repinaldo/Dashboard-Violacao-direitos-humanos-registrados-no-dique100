import os
import dask.dataframe as dd
import pandas as pd

from Dados import caminho_dados

def carregar_dados_grupos_vulneraveis(anos=None, grupos=None, semestre=None, to_pandas=False):
    """
    Carrega dados filtrados por ano(s), grupo(s) e semestre(s).

    Parâmetros:
        anos (int | list[int] | None): Ano ou lista de anos. Se None, pega todos.
        grupos (str | list[str] | None): Grupo ou lista de grupos. Se None, pega todos.
        semestre (str | None): "primeiro", "segundo" ou None para pegar ambos.
        to_pandas (bool): Se True, retorna um DataFrame Pandas; caso contrário, retorna Dask.

    Retorna:
        dask.DataFrame ou pandas.DataFrame
    """

    pasta_dados = caminho_dados("Pasta")
    caminhos = []

    if isinstance(anos, int):
        anos = [anos]
    if isinstance(grupos, str):
        grupos = [grupos]
    if semestre is not None:
        semestre = semestre.lower()

    for ano in sorted(os.listdir(pasta_dados)):
        ano_path = os.path.join(pasta_dados, ano)
        if not os.path.isdir(ano_path):
            continue
        if anos and int(ano) not in anos:
            continue

        grupos_path = os.path.join(ano_path, "Grupos Vulneráveis")
        if not os.path.isdir(grupos_path):
            continue

        for grupo in os.listdir(grupos_path):
            grupo_path = os.path.join(grupos_path, grupo)
            if not os.path.isdir(grupo_path):
                continue
            if grupos and grupo not in grupos:
                continue

            if semestre:
                padrao_semestre = f"{semestre}_semestre_{ano}".lower()
            else:
                padrao_semestre = None

            for arquivo in os.listdir(grupo_path):
                arquivo_lower = arquivo.lower()

                if padrao_semestre and padrao_semestre not in arquivo_lower:
                    continue

                caminhos.append(os.path.join(grupo_path, arquivo))

    if not caminhos:
        print(f"[AVISO] Nenhum arquivo encontrado para os filtros: anos={anos}, grupos={grupos}, semestre={semestre}")
        return None

    df = dd.read_csv(
        caminhos,
        sep=";",
        encoding="utf-8-sig",
        assume_missing=True,
        dtype=str
    )

    return df.compute() if to_pandas else df


def carregar_dados_gerais_ano(remove_total = False):
    """
    Carrega dados resumindo a frequência geral de cada ano.

    Parâmetros:
        remove_total: Se True, remove a linha ,total_geral; caso contrário, essa linha é inclusa no retorno.

    Retorna:
        dict[int, pd.DataFrame]: Dicionário com ano como chave e DataFrame como valor.
    """

    pasta_dados = caminho_dados("Pasta")

    dados = {}

    for ano in sorted(os.listdir(pasta_dados)):
        caminho_csv = os.path.join(pasta_dados, ano, "Grupos Vulneráveis", f"frequencias_{ano}.csv")
        if os.path.exists(caminho_csv):
            df = pd.read_csv(caminho_csv, sep=";", encoding="utf-8-sig")

            if remove_total:
              df = df[df["Grupo vulnerável"].str.strip().str.lower() != "total geral"]

            df["Ano"] = int(ano)
            dados[int(ano)] = df

    return dados
