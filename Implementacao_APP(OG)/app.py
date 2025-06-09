from flask import Flask, redirect , render_template , request, url_for , session
from DataOperations import DataFrameToDict
from DataBase import data_base, redis_cliente 
import dask.dataframe
from dash_app import create_dash_aplication



my_server = Flask(__name__)
my_server.secret_key = "mysecretkey" #Adiciona uma chave secreta para a sessão que é fundamentalapara a segurança de cookies

#Carrega os Dados do ano selcionado
def load_data_for_Year(year):
         
     try : 
         
          year = int(year)
          
          #Pega o dicionário que armazena os arquivos referentes ao ano de interesse.
          files = data_base.Years.get(year)

          categories = ['UF', 'Raça/Cor do suspeito', 'Grupo vulnerável', 'violacao', 'motivacoes', 'Cenário_da_violação', 
                        'Grau_instrução_do_suspeito', 'Faixa_etária_da_vítima','Faixa_etária_do_suspeito', 'Gênero_da_vítima', 
                        'Relação_vítima_suspeito', 'Denunciante']

          if files:
               
               #Pega os arquivos CSV's que representam os dados anuais, separados em semestres, armazenados no dicionário files
               firstSemesterData = dask.dataframe.read_csv(files[0], dtype = str, delimiter = ";", usecols = categories, low_memory = False)
               secondSemesterData = dask.dataframe.read_csv(files[1], dtype = str, delimiter = ";", usecols = categories, low_memory = False)
               
              #Armazena os dados por Dicionário de dicionário, no qual cada dicionário, com exceção dos que separam os semestres, representam uma linha do arquivo csv
               result = DataFrameToDict.Transforma_Dataframe_em_Dicionario(categories, firstSemesterData, secondSemesterData)   

               """  #Exemplo da saída de Result:
               print("Saída esperada para a primeira linha do primeiro semestre de 2020 : ")
               print(result['primeiro_semestre'][0])"""
               
               return result       
               
          else:
                    
                    print(f"Não há dados disponíveis para o ano {year}.")

                    return None
          
     except Exception as e:

          print(f"Erro ao carregar os dados {e}")

#Seleciona o ano  
def ChooseYear():

     try:   
        
        #Seleciona o anon selecoionado no arquivo html menuYear.
        chosen_year = int(request.form['year'])

        return chosen_year
     
     except Exception as e:

          print(f'Erro ao carregar o ano : {e}')


#Primeira página do Flask
@my_server.route("/" , methods = ['GET' , 'POST'])

def menu_Year():

     try : 

          if request.method == 'POST':
               
               chosen_year = ChooseYear()

               if chosen_year in data_base.Years:
                    
                    return redirect(url_for('armazenarDados' , year = chosen_year))
               else:
                    return render_template('/' , "Year not Avalible")
               
          return render_template('menuYear.html')
     
     except Exception as e:

          print(f'Erro no menu_Year : {e}')
          


#Armazena os dados no redis e alterna para o menu Dash
@my_server.route("/armazenarDados/<year>" , methods = [ 'GET' , 'POST'])

def armazenarDados(year):
    
    try: 
          
          yearData = load_data_for_Year(year)
          session['year'] = year
          redis_cliente.set_year_data(year , yearData)  #Armazena os dados do ano no Redis

          return redirect(url_for('render_dash'))
    
    except Exception as e:
         
         print(f'Erro ao armazenar os dados no servidor redis : {e}')



dash_app = create_dash_aplication(my_server)

#Reenderiza o Dash
@my_server.route("/dash/")

def render_dash():

     try:

          return dash_app.index()
     
     except Exception as e:

          print(f'Erro ao renderizar a página Dash : {e}')
    


if __name__ == '__main__':
    my_server.run(debug = True)
