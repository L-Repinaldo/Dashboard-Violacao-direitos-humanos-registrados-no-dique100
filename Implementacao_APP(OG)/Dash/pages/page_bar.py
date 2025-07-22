import dash
from dash.dependencies import Input, Output
from dash import html, dcc 
import plotly.express as px
import pandas as pd
import json

dash.register_page(__name__, path = "/graph_bar")

try : 


    layout = html.Div([

    html.H1("Gráfico de Barras"),
    html.H3("Esse gráfico mostra a quantidade de vezes cada dado apareceu por determinada categoria"),
    dcc.Dropdown(

        id='bar-dropdown',

        options=[

            {'label': 'UF',
            'value': 'UF'},
            {'label': 'Raça/Cor do suspeito',
            'value': 'Raça/Cor do suspeito'},
            {'label': 'Grupo vulnerável',
            'value': 'Grupo vulnerável'},
            {'label': 'Grau de Instrução do Suspeito',
            'value' : 'Grau_instrução_do_suspeito'},


        ],

        value = "Grupo vulnerável",
 
    ),
    dcc.Graph(id='bar-graph', className = 'meu-grafico ', style = { 'width' : '100%' , 'height' : '100%'}),

    ])

except Exception as e :

    print(f'Erro ao criar o layout da página do gráfico em barras : {e}')




@dash.callback(
        
    Output('bar-graph', 'figure'),
    Input('bar-dropdown', 'value'),
    Input('year-data-store-max', 'data'),
    prevent_initial_call=True

)
def update_bar_graph(selected_category, yearDataMaxQuantityPerCategory):


    try : 


        print(f"Update_bar_graph : {selected_category}")

        dict_data = json.loads(yearDataMaxQuantityPerCategory)

        if dict_data:

            data = pd.DataFrame(dict_data)
            filtered_data = data[data['Categoria'] == selected_category]
            
            fig = px.bar(filtered_data,
                         x = 'Valor',
                         y = 'Contagem',
                         labels={'Valor': selected_category, 'Contagem': 'Total Denúncias'},
                         color= 'Valor',
                         )
            
            #Filtra o gráfico para não mostrar a quantidade dos valores não preenchidos ("N/D")
            fig.for_each_trace(lambda trace: trace.update(visible = "legendonly")
                            if trace.name == "N/D" else None )

            return fig
        
        else:

            return {'data': [], 'layout': {'title': 'Dados não disponíveis'}}
        
    except Exception as e:
         
         print(f'Erro ao obter os dados para o gráfico em barras')
         return {'data': [], 'layout': {'title': 'Dados não disponíveis'}}






























