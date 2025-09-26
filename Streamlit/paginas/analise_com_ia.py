import streamlit as st
import pandas as pd
import google.generativeai as genai

from Operacoes import carregar_dados_gerais_ano, carregar_dados_grupos_vulneraveis

# =========================
# Configuração do modelo (cacheado)
# =========================
@st.cache_resource
def carregar_modelo():
    return genai.GenerativeModel("gemini-2.0-flash-thinking-exp")


# =========================
# Carrega todos os dados de todos os anos
# =========================
@st.cache_data
def carregar_todos_os_dados():
    return carregar_dados_gerais_ano()


# =========================
# Carrega dados detalhados do grupo (todos os anos)
# =========================
@st.cache_data
def carregar_historico_grupo(grupo):

    df = carregar_dados_grupos_vulneraveis( anos = None, grupos = grupo, semestre = None, to_pandas = False  )

    if len(df.columns) == 0:
        return None

    # Remover registros inválidos como "N/D"
    for col in df.columns:
        if df[col].dtype == object:
            df = df[df[col].str.upper() != "N/D"]

    return df


# =========================
# Geração de texto pela IA
# =========================
def gerar_texto_global(grupo, df_hist_grupo, dados_por_ano, model):

    prompt = (
        f"Você é um analista de políticas públicas. Com base no histórico completo de denúncias envolvendo o grupo '{grupo}', "
        f"presente nos dados a seguir, elabore um texto informativo.\n\n"
        f"Resumo de denúncias por ano (linhas=ano e total de registros):\n{dados_por_ano}\n\n"
        f"Dados das denúncias em Dask DataFrame: \n{df_hist_grupo}\n\n "
        "Instruções:\n"
        "- Analise as tendências históricas do grupo (crescimento, redução, estabilidade).\n"
        "- Discuta possíveis razões sociais/institucionais para a incidência dessas denúncias.\n"
        "- Sugira estratégias realistas de mitigação e políticas públicas.\n"
        "- NÃO invente estatísticas além das fornecidas. Use linguagem condicional quando a explicação for inferência.\n"
        "- Seja claro, objetivo e mantenha tom profissional.\n"
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

    dados_por_ano = carregar_todos_os_dados()
    if not dados_por_ano:
        st.error("Nenhum dado carregado.")
        return

    lista_df = []
    for ano, df in dados_por_ano.items():
        df_f = df[df["Grupo vulnerável"].str.strip().str.lower() != "total geral"].copy()
        df_f["Ano"] = ano
        lista_df.append(df_f)
    df_todos = pd.concat(lista_df, ignore_index=True)

    grupos = sorted(df_todos["Grupo vulnerável"].unique())
    grupo_escolhido = st.selectbox("Selecione o grupo vulnerável:", grupos)

    model = carregar_modelo()

    if st.button("Gerar análise da IA"):
        with st.spinner("Carregando histórico e gerando análise..."):
            df_hist_grupo = carregar_historico_grupo(grupo_escolhido)

            if df_hist_grupo is None or len(df_hist_grupo.columns) == 0:
                st.warning("Sem dados históricos para este grupo.")
                return
            texto = gerar_texto_global(grupo = grupo_escolhido, df_hist_grupo= df_hist_grupo, 
                                       dados_por_ano = df_todos[df_todos["Grupo vulnerável"] == grupo_escolhido], model = model)
            st.session_state["ia_texto"] = texto
            st.success("Análise gerada.")

    if "ia_texto" in st.session_state:
        st.markdown("### Texto gerado pela IA")
        st.markdown(st.session_state["ia_texto"])

        if st.button("🔄 Refazer análise"):
            with st.spinner("Gerando nova versão..."):
                df_hist_grupo = carregar_historico_grupo(grupo_escolhido)
                st.session_state["ia_texto"] = gerar_texto_global(grupo = grupo_escolhido, df_hist_grupo= df_hist_grupo, 
                                       dados_por_ano = df_todos[df_todos["Grupo vulnerável"] == grupo_escolhido], model = model)
                st.rerun()

    st.info(
        "⚠️ Observação: o texto gerado é um apoio interpretativo, não substitui fontes oficiais."
    )
