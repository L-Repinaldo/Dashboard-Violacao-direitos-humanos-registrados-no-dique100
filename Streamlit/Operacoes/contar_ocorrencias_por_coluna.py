import pandas as pd

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

    df_contagem = (
        df_total[coluna]
        .value_counts()
        .reset_index()
        .rename(columns={"index": coluna, coluna: "Aparições"})
    )

    df_contagem = df_contagem.sort_values(by="Aparições", ascending=False).reset_index(drop=True)

    return df_contagem
