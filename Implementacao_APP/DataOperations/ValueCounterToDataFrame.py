import pandas as pd

def Transforma_Quantidade_Maxima_de_Aparicoes_em_Dataframe (yearDataMax, category):
        
        try: 
            #Separa o conjunto de dados ,referentes a uma categoria, de cada semestre no dicionário yearData e os transformam num Dataframe pandas.
            first_semester_df = pd.DataFrame.from_dict(yearDataMax['primeiro_semestre'][category], orient='index', columns= ['primeiro_semestre']).reset_index().rename(columns = {'index': category})
            second_semester_df = pd.DataFrame.from_dict(yearDataMax['segundo_semestre'][category], orient = 'index', columns = ['segundo_semestre']).reset_index().rename(columns = {'index': category})

            #Pega os dois Dataframes gerados anteriormente e os junta, gerando um dataframe para o ano inteiro.
            pandas_result = pd.merge(first_semester_df, second_semester_df, on=category, how='outer')
            pandas_result['Total Denúncias'] = pandas_result['primeiro_semestre'].fillna(0) + pandas_result['segundo_semestre'].fillna(0)

            """#Print para que eu possa verificar no terminal se é o resultado esperado
            print(pandas_result.head())
            print(pandas_result.columns)"""

            return pandas_result
        
        except Exception as e:
              print(f'Erro ao transformar yearDataMax em Dataframe :  {e}' )