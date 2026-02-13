import streamlit as st
import pandas as pd
import google.generativeai as genai

from Operacoes import carregar_dados_gerais_ano, carregar_dados_grupos_vulneraveis


# =========================
# Configuração do modelo (cacheado)
# =========================
@st.cache_resource(show_spinner = False )
def carregar_modelo():
    return genai.GenerativeModel("gemini-2.5-flash-lite")

# =========================
# Carrega todos os dados de todos os anos
# =========================
@st.cache_data
def carregar_todos_os_dados():
    return carregar_dados_gerais_ano()


# =========================
# Carrega dados detalhados do grupo (todos os anos)
# =========================
@st.cache_data(show_spinner = False)
def carregar_historico_grupo(grupo):

    df = carregar_dados_grupos_vulneraveis( anos = None, grupos = grupo, semestre = None, to_pandas = False  )

    if len(df.index) == 0:
        return None

    # Remover registros inválidos como "N/D"
    for col in df.columns:
        if df[col].dtype == object:
            df = df[df[col].str.upper() != "N/D"]

    return df



@st.cache_data(show_spinner = False)
def preparar_dados_todos_anos(dados_por_ano):

    lista_df = []
    for ano, df in dados_por_ano.items():
        df_f = df[df["Grupo vulnerável"].str.strip().str.lower() != "total geral"].copy()
        df_f["Ano"] = ano
        lista_df.append(df_f)
    return pd.concat(lista_df, ignore_index=True)


# =========================
# Geração de texto pela IA
# =========================
def gerar_texto_global(grupo, df_historico_grupo, model):

    resumo = df_historico_grupo.describe(include = 'all').to_string()

    prompt = (
        f"Você é um analista de políticas públicas. Com base no histórico de denúncias envolvendo o grupo '{grupo}', "
        f"presente nos dados a seguir, elabore um texto analítico e informativo.\n\n"
        f"Resumo das estatísticas :\n{resumo}\n\n"
        "Instruções:\n"
        "- Contextualize os tipos de violações mais frequentes e seus possíveis impactos sociais.\n"
        "- Discuta possíveis razões sociais ou institucionais que expliquem a incidência dessas denúncias, em tom condicional.\n"
        "- Sugira recomendações exploratórias de políticas públicas, apresentando alternativas realistas.\n"
        "- NÃO invente estatísticas além das fornecidas.\n"
        "- Use linguagem clara, objetiva, técnica e adequada a um relatório acadêmico.\n"
    )

    try:
        response = model.generate_content(prompt)
        return getattr(response, "text", "⚠️ Nenhum texto gerado pela IA.")
    except Exception as e:
        return f"Erro ao chamar a IA: {e}"


# =========================
# Página principal
# =========================
def mostrar():

    st.set_page_config(page_title="Análise IA — Histórico Global", layout="wide")
    st.title("🤖 Análise Assistida por IA — Histórico Global de Grupo Vulnerável")

    model = carregar_modelo()


    dados_por_ano = carregar_todos_os_dados()
    if not dados_por_ano:
        st.error("Nenhum dado carregado.")
        return

    df_todos = preparar_dados_todos_anos(dados_por_ano = dados_por_ano)

    grupos = sorted(df_todos["Grupo vulnerável"].unique())

    with st.container():
        grupo_escolhido = st.selectbox("Selecione o grupo vulnerável:", grupos)

    with st.form("form_geracao"):
        gerar = st.form_submit_button("Gerar análise IA")


    if gerar:

        with st.spinner("Carregando histórico e gerando análise..."):
            df_hist_grupo = carregar_historico_grupo(grupo_escolhido)


            if df_hist_grupo is None :
                st.warning("Sem dados históricos para este grupo.")
                return
            

            texto = gerar_texto_global(grupo = grupo_escolhido, df_historico_grupo = df_hist_grupo,  model = model)
            st.session_state["ia_texto"] = texto

    if "ia_texto" in st.session_state:

        with st.expander("### Texto gerado pela IA", expanded = True):
        
            st.markdown(st.session_state["ia_texto"])

        if st.button("🔄 Refazer análise"):

            with st.spinner("Gerando nova versão..."):

                df_hist_grupo = carregar_historico_grupo(grupo_escolhido)
                st.session_state["ia_texto"] = gerar_texto_global(grupo = grupo_escolhido, df_historico_grupo = df_hist_grupo, model = model)
                st.rerun()

    st.info(
        "⚠️ Observação: o texto gerado é um apoio interpretativo, não substitui fontes oficiais."
    )
