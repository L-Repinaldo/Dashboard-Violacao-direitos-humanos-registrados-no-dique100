import dask.dataframe
from Model.DataBase import data_base_original

#Carrega os Dados do ano selecionado
def carrega_os_dados_por_ano(year):
         
    try : 
         
        year = int(year)
          
        #Pega o dicionário que armazena os arquivos referentes ao ano de interesse.
        files = data_base_original.Years.get(year)

        if not files:

            print(f"Não há dados disponíveis para o ano {year}.")
            return None
        
        categories = ['UF', 'Raça/Cor do suspeito', 'Grupo vulnerável', 'violacao', 'motivacoes', 'Cenário_da_violação', 
                        'Grau_instrução_do_suspeito', 'Faixa_etária_da_vítima','Faixa_etária_do_suspeito', 'Gênero_da_vítima', 
                        'Relação_vítima_suspeito', 'Denunciante']
          
        #Lê os arquivos CSV's dos dois semestres
        first_semester_data = dask.dataframe.read_csv(files[0], dtype = str, delimiter = ";", usecols = categories)
        second_semester_data = dask.dataframe.read_csv(files[1], dtype = str, delimiter = ";", usecols = categories)

        return first_semester_data, second_semester_data   
          
    except Exception as e:

        print(f"Erro ao transformas os dados CSV em Database:  {e}")
        return None
