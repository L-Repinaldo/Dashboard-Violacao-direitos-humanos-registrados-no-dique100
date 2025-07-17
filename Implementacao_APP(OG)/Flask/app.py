from flask import Flask, redirect , render_template , request, url_for , session
from Model.DataBase import data_base
from Dash.dash_app import create_dash_aplication



my_server = Flask(__name__)
my_server.secret_key = "mysecretkey" #Adiciona uma chave secreta para a sessão que é fundamentalapara a segurança de cookies

#Seleciona o ano  
def ChooseYear():

     try:   
        
        #Seleciona o anon selecoionado no arquivo html menuYear.
        chosen_year = int(request.form['year'])

        return chosen_year
     
     except Exception as e:

          print(f'Erro ao carregar o ano : {e}')
          return None


#Primeira página do Flask
@my_server.route("/" , methods = ['GET' , 'POST'])

def menu_Year():

     try : 

          if request.method == 'POST':
               
               chosen_year = ChooseYear()

               if chosen_year in data_base.Years:
                    
                    return redirect(url_for('armazenarDados' , year = chosen_year))
               else:
                    return render_template('menuYear.html' , message = "Year not Avalible")
               
          return render_template('menuYear.html')
     
     except Exception as e:

          print(f'Erro no menu_Year : {e}')
          return render_template('menuYear.html', mensage ="Erro inesperado.")
          


#Armazena os dados no redis e alterna para o menu Dash
@my_server.route("/armazenarDados/<year>" , methods = [ 'GET' , 'POST'])

def armazenarDados(year):
    
    try: 
          
          #yearData = LoadDataForYear.load_data_for_Year(year)

          #if yearData is None:
               #return render_template('menuYear.html', mensage = "Erro ao carregar os dados do ano.")
          
          session['year'] = year
          #redis_cliente.set_year_data(year , yearData)  #Armazena os dados do ano no Redis

          return redirect(url_for('render_dash'))
    
    except Exception as e:
         
         print(f'Erro ao armazenar os dados no servidor redis : {e}')
         return render_template('menuYear.html', mensage ="Erro ao processar o ano selecionado.")



dash_app = create_dash_aplication(my_server)

#Reenderiza o Dash
@my_server.route("/dash/")

def render_dash():

     try:

          return dash_app.index()
     
     except Exception as e:

          print(f'Erro ao renderizar a página Dash : {e}')
          return "Erro ao renderizar o Dash."
    


if __name__ == '__main__':
    my_server.run(debug = True)
