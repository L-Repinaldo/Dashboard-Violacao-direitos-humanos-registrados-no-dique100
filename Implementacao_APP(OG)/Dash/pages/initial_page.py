import dash
from dash import html


dash.register_page(__name__, path="/dash/")


layout = html.Div([
        html.H1("Bem-vindo ao Dash App"),
        html.H3("Selecione uma categoria no menu ao lado para começar.")
    ])