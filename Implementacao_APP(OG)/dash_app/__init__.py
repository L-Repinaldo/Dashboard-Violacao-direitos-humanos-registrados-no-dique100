import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import flask
from DataBase import redis_cliente as rc
from DataOperations import ValueCounter

#Inicialização do server Dash
def create_dash_aplication(flask_app):

    external_stylesheets = ["/assets/style.css"]

    try: 

        dash_app = dash.Dash( name = __name__ ,
                            use_pages = True,
                            server = flask_app,
                            external_stylesheets=external_stylesheets,
                            ) 
        
    except Exception as e:

        print(f"Erro ao criar o Dash app {e}")
    
    
    try : 
        #App Layout
        dash_app.layout = html.Div(
            className = "content",
            children = [

                dcc.Store(id='session-year'),  # Store para o ano da sessão
                dcc.Location(id='url', refresh=False),
                html.Div(
                    
                    className = "graph_menu",

                    children = [
                        html.H1("Categorias"),
                        html.H2("Selecione uma categoria de análise"),
                        #Cria um barra de Navegação que redireciona para cada página dash
                        dbc.NavbarSimple(
                            children=[
                                dbc.NavItem(dbc.NavLink("Gráficos em Barra",
                                                         href="/graph_bar",
                                                         active="exact",
                                                         class_name="Navegação")),

                                dbc.NavItem(dbc.NavLink("AI",
                                                         href = "/AI_page", 
                                                         active = "exact", 
                                                         class_name = "Navegação")),
                                
                                dbc.NavItem(dbc.NavLink("Tabela",
                                                        href = "/table_page",
                                                        active = "exact",
                                                        class_name = "Navegação")),

                               html.A("Voltar ao Menu de Ano", href = "/"),
                            ],
                            brand = "Página Inicial",
                            brand_href="/initial_page",
                            color="primary",
                            dark=True,
                        ),
                        dcc.Store(id = 'year-data-store'),#Armazena os dados por Dicionário de dicionário, no qual cada dicionário, com exceção dos que separam os semestres, representam uma linha do arquivo csv
                        dcc.Store(id = "year-data-store-max" ),#Armazena os dados contabilizando o número de aparições de cada valor.

                    ]

                ),

                html.Div(
                    className = "graph_content",
                    
                    children = [
                        dash.page_container
                    ],
                    
                )
            ],
        )

        return dash_app
    
    except Exception as e:

        print(f'Erro ao criar o layout dash {e}')





#Carrega os dados que serão utilizados
@dash.callback(
    Output('year-data-store-max', 'data'), 
    Output("year-data-store" , 'data'),
    Input('session-year', 'data'),  # Aciona quando o ano da sessão muda

   
)
def load_year_data(year):

    try:
        
        if year:

            year = int(flask.session.get('year')) #Adiquire o ano selecionado no app Flask
            yearData = rc.get_year_data(year)#Utiliza o ano para adquirir os dados anual armazenado no redis
            #Armazena os dados contabilizando a ocorrêncisa de cada valor
            yearDataMaxQuantityPerCategory = ValueCounter.Quantidade_Maximaque_Um_Valor_Aparece_Por_Categoria(yearData)
                        
            return yearDataMaxQuantityPerCategory , yearData
        
        else:
            return {}, {}
    
    except Exception as e:

        print(f'Erro ao carregar dados: {e}')

        return {} , {}
    

 # Callback para atualizar o 'session-year' quando o ano estiver na sessão Flask
@dash.callback(
    Output('session-year', 'data'),
    Input('url', 'pathname'),  # Qualquer mudança de página pode indicar que o ano está na sessão

)
def update_session_year(pathname):
    year = flask.session.get('year')
    if year:
        return int(year)
    return dash.no_update