import dash
from dash import  html, dcc
from dash.dependencies import Input, Output
import flask
#from AI import gemini  # Importa  módulo de configuração da Gemini
import google.generativeai as genai


dash.register_page(__name__, path="/AI_page")

try:
    layout = html.Div([
        html.Div(id = 'session-year'),
        html.H1("Prompt IA"),
        html.H3("Análise focada na categoria Grupo Vulnerável"),
        dcc.Dropdown(
            id='AI-dropdown',
            options=[],  # Inicialmente vazio
            value=None,
        ),
        html.Div(id = "AI-page"),
        dcc.Store(id="ai-dropdown-options"),  # Store para as opções do dropdown
        html.Div(id='ai-generated-text', className="ai-output"),  # Div para a saída da IA
        html.A("Voltar ao Menu de Ano", href="/"),
    ])

   
except Exception as e:

    print(f'Erro ao renderizar o layout da página de AI: {e}')






# Carrega os dados e as opções do dropdown
@dash.callback(

    Output('AI-dropdown', 'options'),
    Input('AI-page', 'id'),  # Input fictício para acionar o callback na carga da página
    Input('year-data-store-max', 'data' ),
    allow_duplicate=True,
    prevent_initial_call=True
)
def load_ai_page_data(id, yearDataMaxQuantityPerCategory):
    try:


        if  'primeiro_semestre' in yearDataMaxQuantityPerCategory and 'Grupo vulnerável' in yearDataMaxQuantityPerCategory['primeiro_semestre']:

            keys_dict = list(yearDataMaxQuantityPerCategory['primeiro_semestre']['Grupo vulnerável'].keys())
            options = [{'label': key, 'value': key} for key in keys_dict]

        else:

            options = []
            print("Dados para 'Grupo vulnerável' não encontrados.")

        return options
    
    except Exception as e:

        print(f'Erro ao carregar dados para a página de IA: {e}')

        return {}, {}, []




#Gera os textos de IA
@dash.callback(
    Output('ai-generated-text', 'children'),  # Onde o texto da IA será exibido
    Input('AI-dropdown', 'value'),  # Valor selecionado no dropdown da IA
    Input('year-data-store-max', 'data'),
    prevent_initial_call=True
)
def generate_ai_text(ai_value, yearDataMaxQuantityPerCategory):

    model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp')

    if model and ai_value and yearDataMaxQuantityPerCategory and 'primeiro_semestre' in yearDataMaxQuantityPerCategory and 'Grupo vulnerável' in yearDataMaxQuantityPerCategory['primeiro_semestre']:
        try:
            year = flask.session.get('year')
            # Construa o prompt para a IA
            prompt = f"Gere um texto informativo sobre o '{ai_value}' dentro da categoria 'Grupo vulnerável' com base nos dados de denúncias do ano {year}. Forneça insights relevantes e possíveis soluções para minimizar esse tipo de violação."

            response = model.generate_content(prompt)
            ai_text = response.text
            return html.Div([html.H4("Texto Gerado pela IA:"), dcc.Markdown(ai_text)])
        
        except Exception as e:

            error_message = f"Erro ao gerar texto com a IA: {e}"
            print(error_message)
            return html.Div(f"Erro ao gerar texto com a IA: {e}", style={'color': 'red'})
        
    elif not model:

        return html.Div("A API da IA não está configurada.", style={'color': 'orange'})
    
    else:

        return html.Div("Selecione uma opção no dropdown para gerar o texto.")