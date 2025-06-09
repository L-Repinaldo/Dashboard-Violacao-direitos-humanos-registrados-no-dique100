
def Transforma_Dataframe_em_Dicionario(categories ,  firstSemesterData , secondSemesterData):
   
   try: 
      
      #Está transformando os Dataframes dask em dicionário python, separando os valores em categorias.
      firstSemester = firstSemesterData[categories].compute().to_dict(orient='records')
      secondSemester = secondSemesterData[categories].compute().to_dict(orient='records')
      
      #Print para que eu possa verificar no terminal se é o resultado esperado
      #print(firstSemester[0])

      return{

         'primeiro_semestre' : firstSemester,
         'segundo_semestre' : secondSemester
      }
   
   except Exception as e:

      print(f'Erro ao armazenar os dados em um dicionário por categorias {e}')