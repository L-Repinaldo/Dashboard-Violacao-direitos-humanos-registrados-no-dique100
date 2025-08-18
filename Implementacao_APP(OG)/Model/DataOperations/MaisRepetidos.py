import dask.dataframe as dd
import pandas as pd
from functools import reduce

def calculate_most_frequent_by_category(data: dd.DataFrame, group_by_column: str) :
    """
    Calcula a moda (o valor mais frequente) para diversas colunas de categoria
    em um Dask DataFrame, agrupando os resultados por uma coluna principal.

    Args:
        data: O Dask DataFrame contendo os dados.
        group_by_column: O nome da coluna para agrupar os resultados.

    Returns:
        Um pandas DataFrame contendo a moda de cada coluna de categoria,
        agrupada pela coluna principal. Retorna um DataFrame vazio em caso de erro.
    """

    target_columns = [
        'violacao', 'Cenário_da_violação', 'motivacoes',
        'Faixa_etária_da_vítima', 'Faixa_etária_do_suspeito',
        'Gênero_da_vítima', 'Relação_vítima_suspeito', 'Denunciante'
    ]

    if group_by_column == "UF":
        target_columns.append("Grupo vulnerável")

    try:

        all_required_columns = [group_by_column] + target_columns
        
        existing_columns = [col for col in all_required_columns if col in data.columns]
        
        if not all(col in data.columns for col in [group_by_column]):
            print(f"Erro: A coluna de agrupamento '{group_by_column}' não foi encontrada.")
            return pd.DataFrame()
        
        for col in existing_columns:
            data[col] = data[col].astype(str).str.upper()

        results = []
        for col in target_columns:
            if col not in data.columns:
                print(f"Aviso: A coluna '{col}' não foi encontrada e será ignorada.")
                continue

            freq = (
                data[[group_by_column, col]]
                .dropna()
                [~data[col].isin(["N/D", "<NA>"])]
                .groupby([group_by_column, col])
                .size()
                .compute()  
                .reset_index()
                .rename(columns={0: "count"})
                
            
            )

            # Encontra o índice do valor mais frequente para cada grupo
            idx = freq.groupby(group_by_column)['count'].idxmax()
                    
            # Obtém a moda (valor com o maior "count") e computa o resultado
            moda = freq.loc[idx].reset_index(drop=True)
            
            # Renomeia a coluna para uma identificação clara
            moda = moda.rename(columns={col: f"{col}_mais_frequente"})
            
            # Seleciona apenas as colunas necessárias para o merge posterior
            moda = moda[[group_by_column, f"{col}_mais_frequente"]]
            
            results.append(moda)

        if not results:
            return pd.DataFrame()

        final_df = reduce(
            lambda left, right: pd.merge(left, right, on=group_by_column, how="outer"),
            results
        )

        return final_df

    except Exception as e:
        print(f"Ocorreu um erro ao calcular a moda por categoria: {e}")
        return pd.DataFrame()