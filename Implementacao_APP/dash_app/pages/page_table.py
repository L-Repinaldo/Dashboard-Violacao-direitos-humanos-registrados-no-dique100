import dash
from dash.dependencies import Input, Output
from dash import dash_table
from dash import html, dcc
from DataOperations import MaioresOcorrências 


dash.register_page(__name__, path = "/table_page")



try: 

    layout = html.Div([

        html.H1("Tabela"),
        html.Div(id = 'session-year'),
        dcc.Dropdown(
            id = 'table-dropdown',

            options = [
                {'label': 'Grupo vulnerável',
                 'value': 'Grupo vulnerável'},
                {'label': 'UF',
                 'value': 'UF'},
     
                
            ]
        ),
        html.Div(id = 'table'),
        html.A("Voltar ao Menu de Ano", href = "/"),
        dcc.Store(id="year-data-store-max"),  # Garante que o componente exista no layout desta página
        dcc.Store(id="year-data-store"),      # Se você também usa este store aqui
        
    ])


    #Esse callback cria a tabela 
    @dash.callback(
        Output('table', 'children'),
        Input('table-dropdown', 'value'),
        Input('year-data-store-max', 'data'),
        Input('year-data-store', 'data'),
        prevent_initial_call=True
    )
    def display_table( selected_category, yearDataMaxQuantityPerCategory, yearData):
        
        


        try:
        
            releventCategories = ['violacao', 'Cenário_da_violação', 'motivacoes', 'Faixa_etária_da_vítima', 'Faixa_etária_do_suspeito', 'Gênero_da_vítima', 'Relação_vítima_suspeito', 'Denunciante']
            df = MaioresOcorrências.Maiores_Ocorrências_por_valor(yearData , releventCategories, selected_category )
    
        
        except Exception as e:

            print(f'Erro ao adiquirir os dados necessários : {e}')

        try: 

            table = dash_table.DataTable(
                
                data=df.to_dict('records'),
                columns=[{'name': col, 'id': col} for col in df.columns],
                style_cell={'textAlign': 'left'},
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                }
            )
            return table
        
        except Exception as e:

            print(f'Erro ao gerar a tabela : {e}')



except Exception as e:

    print(f"Erro ao renderizar página Table : {e}")

