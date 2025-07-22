import dask.dataframe
from Model.DataBase import data_base

#Carrega os Dados do ano selecionado
def load_data_for_Year(year):
         
    try : 
         
        year = int(year)
          
        #Pega o dicionário que armazena os arquivos referentes ao ano de interesse.
        files = data_base.Years.get(year)

        if not files:

            print(f"Não há dados disponíveis para o ano {year}.")
            return None
        
        categories = ['UF', 'Raça/Cor do suspeito', 'Grupo vulnerável', 'violacao', 'motivacoes', 'Cenário_da_violação', 
                        'Grau_instrução_do_suspeito', 'Faixa_etária_da_vítima','Faixa_etária_do_suspeito', 'Gênero_da_vítima', 
                        'Relação_vítima_suspeito', 'Denunciante']
          
        #Lê os arquivos CSV's dos dois semestres
        firstSemesterData = dask.dataframe.read_csv(files[0], dtype = str, delimiter = ";", usecols = categories)
        secondSemesterData = dask.dataframe.read_csv(files[1], dtype = str, delimiter = ";", usecols = categories)

        result = dask.dataframe.concat([firstSemesterData, secondSemesterData], axis=0, interleave_partitions=True)
        result = result.repartition(npartitions=8) 
            
        return result   
          
    except Exception as e:

        print(f"Erro ao transformas os dados CSV em Database:  {e}")
        return None
