import streamlit as st
import pandas as pd
import google.generativeai as genai

from Operacoes.carregar_dados import carregar_dados_gerais_ano

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
    dados_por_ano = carregar_todos_os_dados()
    lista = []

    for ano, df in dados_por_ano.items():

        df_f = df[df["Grupo vulnerável"].str.strip().str.lower() != "total geral"].copy()
        df_f["Ano"] = ano
        df_f = df_f[df_f["Grupo vulnerável"] == grupo]

        if df_f.empty:
            continue

        for col in df_f.columns:
            if df_f[col].dtype == object:
                df_f = df_f[df_f[col].str.upper() != "N/D"]

        lista.append(df_f)

    if not lista:
        return None

    return pd.concat(lista, ignore_index=True)


# =========================
# Geração de texto pela IA
# =========================
def gerar_texto_global(grupo, df_hist, model):

    resumo = (
        df_hist.groupby("Ano")
        .size()
        .reset_index(name="total")
        .sort_values("Ano")
        .to_string(index=False)
    )

    prompt = (
        f"Você é um analista de políticas públicas. Com base no histórico completo de denúncias envolvendo o grupo '{grupo}', "
        f"presente nos dados a seguir, elabore um texto informativo.\n\n"
        f"Resumo de denúncias por ano (linhas=ano e total de registros):\n{resumo}\n\n"
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
            df_hist = carregar_historico_grupo(grupo_escolhido)
            if df_hist is None or df_hist.empty:
                st.warning("Sem dados históricos para este grupo.")
                return
            texto = gerar_texto_global(grupo_escolhido, df_hist, model)
            st.session_state["ia_texto"] = texto
            st.success("Análise gerada.")

    if "ia_texto" in st.session_state:
        st.markdown("### Texto gerado pela IA")
        st.markdown(st.session_state["ia_texto"])

        if st.button("🔄 Refazer análise"):
            with st.spinner("Gerando nova versão..."):
                df_hist = carregar_historico_grupo(grupo_escolhido)
                st.session_state["ia_texto"] = gerar_texto_global(grupo_escolhido, df_hist, model)
                st.experimental_rerun()

    st.info(
        "⚠️ Observação: o texto gerado é um apoio interpretativo, não substitui fontes oficiais."
    )
