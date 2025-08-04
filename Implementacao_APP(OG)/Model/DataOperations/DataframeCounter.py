import dask.dataframe as dd
import pandas as pd


def calculate_max_occurrences_by_category(data_dask_dataframe: dd.DataFrame):
    
    """
    Calcula a contagem de ocorrências de cada valor em diversas colunas categóricas
    de um Dask DataFrame e retorna um Pandas DataFrame consolidado, ordenado por contagem.

    Args:
        data_dask_dataframe: O Dask DataFrame contendo os dados.

    Returns:
        Um Pandas DataFrame com as colunas 'Categoria', 'Valor' e 'Contagem',
        ordenado pela contagem de forma decrescente.
        Retorna um DataFrame Pandas vazio em caso de erro ou dados vazios.
    """

    categories = [
        'UF', 'Raça/Cor do suspeito', 'Grupo vulnerável', 'violacao', 'motivacoes',
        'Cenário_da_violação', 'Grau_instrução_do_suspeito', 'Faixa_etária_da_vítima',
        'Faixa_etária_do_suspeito', 'Gênero_da_vítima', 'Relação_vítima_suspeito', 'Denunciante'
    ]

    try:
        # Verifica se o DataFrame está vazio
        if data_dask_dataframe.columns.size == 0:
            print('Year Data está vazio')
            return pd.DataFrame(columns=['Categoria', 'Valor', 'Contagem'])

        list_of_dask_dfs = []

        for category in categories:

            if category not in data_dask_dataframe.columns:
                print(f"Aviso: Coluna '{category}' não encontrada no DataFrame e será ignorada.")
                continue

            # Remove nulos e padroniza para maiúsculas
            column = data_dask_dataframe[category].dropna().str.upper()

            temp_dask_df = column.to_frame(name = 'Valor')
            temp_dask_df['Contagem'] = 1

            # Conta as ocorrências de cada valor 
            counts_dask = temp_dask_df.groupby('Valor')['Contagem'].sum().reset_index()
            counts_dask['Categoria'] = category

            #Reorganização das colunas
            counts_dask = counts_dask[['Categoria', 'Valor', 'Contagem']]

            list_of_dask_dfs.append(counts_dask)
        
            if not list_of_dask_dfs:
                print("Nenhuma categoria válida foi processada. Retornando DataFrame vazio.")
                return pd.DataFrame(columns=['Categoria', 'Valor', 'Contagem'])
        
        # Adiciona o DataFrame temporário ao DataFrame principal
        result_dask_df = dd.concat(list_of_dask_dfs, interleave_partitions  = True)

        result_pandas_df = result_dask_df.compute()
        result_pandas_df = result_pandas_df.sort_values(by='Contagem', ascending=False)

        return result_pandas_df

    except Exception as e:
        print(f'Erro ao contabilizar as ocorrências de cada atributo: {e}')
        return pd.DataFrame(columns=['Categoria', 'Valor', 'Contagem'])
