import pandas as pd
import unicodedata


def normalizar_categoria_faixa_etaria(df, coluna):
    """
    Normaliza valores de uma coluna categórica para evitar duplicações.
    - Converte para minúsculas
    - Remove espaços extras
    - Substitui padrões conhecidos (ex: 'ou mais' -> 'ou mais anos')
    """
    def normalizar_texto(x):
        if pd.isna(x):
            return ""
        x = str(x)
        x = unicodedata.normalize("NFKD", x).encode("ASCII", "ignore").decode("utf-8")
        x = " ".join(x.strip().split())
        return x.lower()

    df = df.copy()
    df[coluna] = df[coluna].apply(normalizar_texto)

    df[coluna] = df[coluna].replace({
        "00 a 1 ano" : '00 a 01 ano'
    })

    df_consolidado = (
        df.groupby(coluna, as_index=False)["count"]
          .sum()
          .sort_values(by="count", ascending=False)
          .reset_index(drop=True)
    )

    return df_consolidado

def normalizar_categoria_motivacao(df, coluna):
    """
    Normaliza categorias de motivação sem depender de substituições manuais.
    - Remove acentos, espaços extras e coloca em minúsculas
    - Remove prefixos como 'motivacao.' ou similares
    - Consolida duplicatas somando 'count'
    """

    def limpar_texto(x):
        if pd.isna(x):
            return ""
        x = str(x)
        # remove acentos
        x = unicodedata.normalize("NFKD", x).encode("ASCII", "ignore").decode("utf-8")
        x = " ".join(x.strip().split())
        x = x.lower()
        # remove prefixos antes de um ponto (ex: "motivacao.em razao" -> "em razao")
        if "." in x:
            x = x.split(".", 1)[1]
        return x

    df = df.copy()
    df[coluna] = df[coluna].apply(limpar_texto)

    df = (
        df.groupby(coluna, as_index=False)["count"]
          .sum()
          .sort_values(by="count", ascending=False)
          .reset_index(drop=True)
    )

    return df
