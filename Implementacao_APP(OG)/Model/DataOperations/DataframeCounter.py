import dask.dataframe as dd
import pandas as pd

def Quantidade_Maxima_que_Um_Valor_Aparece_Por_Categoria(yearData_Dask_Dataframe: dd.DataFrame):
    categories = [
        'UF', 'Raça/Cor do suspeito', 'Grupo vulnerável', 'violacao', 'motivacoes',
        'Cenário_da_violação', 'Grau_instrução_do_suspeito', 'Faixa_etária_da_vítima',
        'Faixa_etária_do_suspeito', 'Gênero_da_vítima', 'Relação_vítima_suspeito', 'Denunciante'
    ]

    try:
        # Verifica se o DataFrame está vazio
        if yearData_Dask_Dataframe.columns.size == 0:
            print('Year Data está vazio')
            return pd.DataFrame(columns=['Categoria', 'Valor', 'Contagem'])

        lista_df = []

        for category in categories:
            # Remove nulos e padroniza para maiúsculas
            coluna = yearData_Dask_Dataframe[category].dropna().str.upper()

            temp_df = coluna.to_frame(name = 'Valor')
            temp_df['Contagem'] = 1

            # Conta as ocorrências de cada valor 
            contagem = temp_df.groupby('Valor')['Contagem'].sum().reset_index()
            contagem['Categoria'] = category

            #Reorganização das colunas
            contagem = contagem[['Categoria', 'Valor', 'Contagem']]

            lista_df.append(contagem)
        
        # Adiciona o DataFrame temporário ao DataFrame principal
        result_Dask_df = dd.concat(lista_df, interleave_partitions  = True)

        result_pandas_df = result_Dask_df.compute()
        result_pandas_df = result_pandas_df.sort_values(by='Contagem', ascending=False)

        return result_pandas_df

    except Exception as e:
        print(f'Erro ao contabilizar as ocorrências de cada atributo: {e}')
        return dd.from_pandas(pd.DataFrame(columns=['Categoria', 'Valor', 'Contagem']), npartitions=1)

