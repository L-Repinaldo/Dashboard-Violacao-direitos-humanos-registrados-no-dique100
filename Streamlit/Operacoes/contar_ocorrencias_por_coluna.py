import pandas as pd
import numpy as np

def contar_ocorrencias_por_coluna(df_primeiro, df_segundo, coluna):
    """
    Conta a quantidade de ocorrências por valor de uma coluna,
    consolidando os dados do primeiro e segundo semestre.

    Parâmetros:
        df_primeiro (pd.DataFrame): Dados do primeiro semestre.
        df_segundo (pd.DataFrame): Dados do segundo semestre.
        coluna (str): Nome da coluna a ser contabilizada.

    Retorna:
        pd.DataFrame: DataFrame com a contagem consolidada, ordenado em ordem decrescente.
    """

    df_total = pd.concat([df_primeiro, df_segundo], ignore_index=True)

    col_array = df_total[coluna].dropna().to_numpy()

    valores, contagens = np.unique(col_array, return_counts=True)

    df_contagem = pd.DataFrame({
        "Aparições": valores,
        "count": contagens
    }).sort_values(by="Aparições", ascending=False, ignore_index=True)

    return df_contagem
