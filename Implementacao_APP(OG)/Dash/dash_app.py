import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import flask
from Model.DataOperations.LoadDataForYear import load_data_for_Year
from Model.DataOperations.DataframeCounter import calculate_max_occurrences_by_category



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

                html.Div(
                    
                    className = "graph_menu",

                    children = [
                        html.H1(id = "display-session-year"),
                        html.Br(),
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
                            brand_href="/dash/",
                            color="primary",
                            dark=True,
                        ),
                        dcc.Store(id = 'year-data-max-occurrences-store' , storage_type= 'session' ),#Armazena os dados contabilizando o número de aparições de cada valor.
                        dcc.Location(id='url', refresh=False),
                        dcc.Store(id='session-year'),  # Store para o ano da sessão

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
    Output('year-data-max-occurrences-store', 'data'), 
    Input('session-year', 'data'),  # Aciona quando o ano da sessão muda

   
)

    
def load_aggregated_data_for_store(year):

    """
        Carrega o Dask DataFrame para o ano selecionado e calcula as ocorrências máximas.
        Armazena os dados agregados (que são pequenos) no dcc.Store.
        O DataFrame Dask completo NÃO é computado e armazenado aqui.
    """

    try:
        
        if year:

            year = int(year)

            year_data_dask = load_data_for_Year(year)

            if year_data_dask is None:
                    print(f"Dados Dask não disponíveis para o ano {year}.")
                    return {}
        
            year_data_max_occurrences_pd = calculate_max_occurrences_by_category(year_data_dask)            
            year_data_max_occurrences_json = year_data_max_occurrences_pd.to_json(orient =  'records')


            return year_data_max_occurrences_json
        
        else:

            return {} 

    except Exception as e:

        print(f'Erro ao carregar os dados agregados no servido Dash: {e}')

        return {}, {}

 # Callback para atualizar o 'session-year' quando o ano estiver na sessão Flask
@dash.callback(
    Output('session-year', 'data'),
    Input('url', 'pathname'),  # Qualquer mudança de página pode indicar que o ano está na sessão

)
def update_session_year(pathname):
    """
        Atualiza o dcc.Store 'session-year' com o ano da sessão Flask.
    """

    year = flask.session.get('year')

    if year:
        return int(year)

    return dash.no_update



@dash.callback(
    Output('display-session-year', 'children'),
    Input('session-year', 'data'),
)
def show_selected_year_in_h1(year):
    """
        Exibe o ano selecionado em um elemento H1.
    """

    if year:
        return f"Ano selecionado: {year}"

    return "Nenhum ano selecionado"