import dask.dataframe as dd
import pandas as pd

def Quantidade_Maxima_que_Um_Valor_Aparece_Por_Categoria(yearData_Pandas_Dataframe):
    categories = [
        'UF', 'Raça/Cor do suspeito', 'Grupo vulnerável', 'violacao', 'motivacoes',
        'Cenário_da_violação', 'Grau_instrução_do_suspeito', 'Faixa_etária_da_vítima',
        'Faixa_etária_do_suspeito', 'Gênero_da_vítima', 'Relação_vítima_suspeito', 'Denunciante'
    ]

    try:
        # Verifica se o DataFrame está vazio
        if yearData_Pandas_Dataframe.size == 0:
            print('Year Data está vazio')
            return dd.from_pandas(pd.DataFrame(columns=['Categoria', 'Valor', 'Contagem']), npartitions=1)

        # Inicializa um DataFrame vazio para armazenar os resultados
        result_df = pd.DataFrame(columns=['Categoria', 'Valor', 'Contagem'])

        for category in categories:
            # Remove nulos e padroniza para maiúsculas
            valores_validos = yearData_Pandas_Dataframe[category].dropna().str.upper()

            # Conta as ocorrências de cada valor
            contagem = valores_validos.value_counts()

            # Para cada valor e sua contagem, cria um DataFrame
            temp_df = pd.DataFrame({
                'Categoria': [category] * len(contagem),
                'Valor': contagem.index,
                'Contagem': contagem.values
            })

            # Adiciona o DataFrame temporário ao DataFrame principal
            result_df = pd.concat([result_df, temp_df], ignore_index=True)

        print(result_df.head())


        return result_df

    except Exception as e:
        print(f'Erro ao contabilizar as ocorrências de cada atributo: {e}')
        return dd.from_pandas(pd.DataFrame(columns=['Categoria', 'Valor', 'Contagem']), npartitions=1)
