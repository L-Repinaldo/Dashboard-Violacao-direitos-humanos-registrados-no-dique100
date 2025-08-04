import dash
from dash.dependencies import Input, Output
from dash import dash_table, html, dcc
import dask.dataframe as dd
import pandas as pd
from Model.DataOperations.LoadDataForYear import load_data_for_Year
from Model.DataOperations.MaisRepetidos import calculate_most_frequent_by_category

# Renomeia a função importada para usar o nome aprimorado do código anterior
# Importa pandas para lidar com o DataFrame vazio em caso de erro

dash.register_page(__name__, path="/table_page")

# ---
# Layout da página
# ---

# É melhor evitar blocos try/except para a definição do layout.
# Se houver um erro aqui, a aplicação falha ao iniciar, o que é o comportamento esperado.
# Em vez disso, separe as partes lógicas e de apresentação.
layout = html.Div([
    html.H1("Análise de Maiores Ocorrências por Categoria"),
    html.P("Selecione uma categoria para visualizar as ocorrências mais frequentes nas demais colunas."),
    dcc.Dropdown(
        id='table-dropdown',
        options=[
            {'label': 'Grupo Vulnerável', 'value': 'Grupo vulnerável'},
            {'label': 'UF', 'value': 'UF'},
        ],
        placeholder = "Selecione uma categoria",
        style={'width': '50%', 'margin-bottom': '20px'}
    ),
    html.Div(id='table-container'), # Renomeado para maior clareza

])

# ---
# Callback para criar e exibir a tabela
# ---

@dash.callback(
    Output('table-container', 'children'),
    Input('table-dropdown', 'value'),
    Input('session-year', 'data'),
    prevent_initial_call=True
)
def display_table(selected_category, year):

    """
    Recebe o ano e a categoria selecionada para gerar a tabela,
    carregando o Dask DataFrame sob demanda.
    """
    
    if not year:
        return html.Div("Dados não disponíveis. Por favor, selecione um ano.", style={'color': 'red'})

    try:
        
        year_data_dask = load_data_for_Year(year)
        
        if year_data_dask is None:
            return html.Div(f"Não foi possível carregar os dados para o ano {year}.", style={'color': 'red'})

        df = calculate_most_frequent_by_category(year_data_dask, selected_category)
        
        if df.empty:
            return html.Div(f"Não há dados para a categoria '{selected_category}' ou a análise resultou em um DataFrame vazio.", style={'color': 'orange'})

    except Exception as e:
        print(f'Erro ao processar dados ou calcular a moda para a tabela: {e}')
        return html.Div("Erro ao carregar ou processar os dados para a tabela.", style={'color': 'red'})

    try:
        table = dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': col.replace('_', ' ').title(), 'id': col} for col in df.columns],
            page_size=15,
            style_cell={'textAlign': 'left', 'padding': '5px'},
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }
            ],
            tooltip_data=[
                {
                    column: {'value': str(value), 'type': 'markdown'}
                    for column, value in row.items()
                } for row in df.to_dict('records')
            ],
            tooltip_duration=None
        )
        return table

    except Exception as e:
        print(f'Erro ao gerar a tabela Dash: {e}')
        return html.Div("Erro ao gerar a tabela de visualização.", style={'color': 'red'})
