import dash
from dash import  html, dcc
from dash.dependencies import Input, Output
import flask
import json
import google.generativeai as genai


dash.register_page(__name__, path="/AI_page")

try:
    layout = html.Div([
   
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
        html.Div([
                  html.H2("⚠️ Observação: O texto acima foi gerado por IA com base em padrões linguísticos. " \
                    "Algumas afirmações podem não ter respaldo empírico ou jurídico. Use como apoio interpretativo, não como fonte oficial.", 
                    style={'color': 'orange'})]),
    
    ])

   
except Exception as e:

    print(f'Erro ao renderizar o layout da página de AI: {e}')



# Carrega os dados e as opções do dropdown
@dash.callback(

    Output('AI-dropdown', 'options'),
    Input('AI-page', 'id'),  # Input fictício para acionar o callback na carga da página
    Input('year-data-max-occurrences-store', 'data' ),
    allow_duplicate=True,
    prevent_initial_call=True
)


def load_ai_page_data(id, year_data_max_occurrences_json):

    try:
        dict_data = json.loads(year_data_max_occurrences_json)

        options = []

        if dict_data:
               
            options = [
                {'label': item['Valor'], 'value': item['Valor']} 
                for item in dict_data 
                if item['Categoria'] == 'Grupo vulnerável'
            ]       
            print("Dados para 'Grupo vulnerável' encontrados.")
            
        return options

    except Exception as e:

        print(f'Erro ao carregar dados para a página de IA: {e}')

        return []



#Gera os textos de IA
@dash.callback(
    Output('ai-generated-text', 'children'),  # Onde o texto da IA será exibido
    Input('AI-dropdown', 'value'),  # Valor selecionado no dropdown da IA
    prevent_initial_call=True
)
def generate_ai_text(ai_value):

    try:

        model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp')

        if model and ai_value :
            
            try:
                year = flask.session.get('year')
                # Construa o prompt para a IA
                prompt = (
                          f"Com base nos dados de denúncias do ano {year}, elabore um texto informativo sobre o grupo '{ai_value}' "
                          f"dentro da categoria 'Grupo vulnerável'. Apresente possíveis razões para a incidência de denúncias envolvendo esse grupo, "
                          f"inclua observações relevantes sobre tendências ou padrões e proponha estratégias realistas para mitigar esse tipo de violação. "
                          f"Não invente estatísticas, nem afirme dados que não constem nos registros disponíveis."
                          f"O texto deve ser claro, objetivo e com tom profissional, voltado para leitores interessados em direitos humanos e políticas públicas. "
                         )

                response = model.generate_content(prompt)
                ai_text = response.text
                return html.Div([
                                 html.H4("Texto Gerado pela IA:"), 
                                 dcc.Markdown(ai_text),
                                 ])
 
            
            except Exception as e:

                error_message = f"Erro ao gerar texto com a IA: {e}"
                print(error_message)
                return html.Div(f"Erro ao gerar texto com a IA: {e}", style={'color': 'red'})
            
        elif not model:

            return html.Div("A API da IA não está configurada.", style={'color': 'orange'})
        
        else:

            return html.Div("Selecione uma opção no dropdown para gerar o texto." , style = {'color': '#3498DB'})
    
    except Exception as e : 

        print(f'Erro  ao carregar o modelo Gemini : {e}')
        return html.Div("Erro ao carregar o modelo Gemin")