import dash
from dash import html, dcc


dash.register_page(__name__, path="/initial_page")


try:
    layout = html.Div([
        html.H1("Bem-vindo ao Dash App"),
        html.H3("Selecione uma categoria no menu ao lado para começar.")
    ])

except Exception as e:
    print(f"Erro ao criar a págian inicial:  {e}")