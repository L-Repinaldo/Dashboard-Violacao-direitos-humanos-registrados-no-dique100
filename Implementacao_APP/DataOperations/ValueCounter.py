

#Contabiliza todas as vezes que um dado se repete e contabiliza, Ex: SP apareceu 13.445 vezes, e os armazenam num dicionário com a categoria sendo a chave
def Quantidade_Maximaque_Um_Valor_Aparece_Por_Categoria (yearData):


    categories = ['UF', 'Raça/Cor do suspeito', 'Grupo vulnerável', 'violacao', 'motivacoes', 'Cenário_da_violação', 'Grau_instrução_do_suspeito']

    try :

      all_firstSemesterCounts = {}
      all_secondSemesterCounts = {}
       
      for category in categories: #Seleciona uma categoria por vez
         
         
         
         #Como yearData é um dicionário de dicionário, deve-se separar os semestres para analisar os dados isoladamente 
         firstSemesterData = yearData['primeiro_semestre']
         secondSemesterData = yearData['segundo_semestre']

         firstSemesterCounts = {}
         secondSemesterCounts = {}

         for row in firstSemesterData:#A variável firstSemesterDta também é um  dicionário de dicionário, então row seleccionará cada dicionário interno individualmente
            value = row.get(category)


            if value :
   
               value = value.upper()
               firstSemesterCounts[value] = firstSemesterCounts.get(value, 0) + 1
         
         for row in secondSemesterData:
            
            value = row.get(category)
            if value :
               
               value = value.upper()
               secondSemesterCounts[value] = secondSemesterCounts.get(value, 0) + 1

         all_firstSemesterCounts[category] = firstSemesterCounts
         all_secondSemesterCounts[category] = secondSemesterCounts

      return {
         
         'primeiro_semestre': all_firstSemesterCounts,
         'segundo_semestre': all_secondSemesterCounts
         
      }
    
    except Exception as e:
       
       print(f'Erro ao contabilizar as ocorrências máximas de cada atributo {e} ')
