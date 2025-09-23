import streamlit as st

from paginas import dashboard_geral, analise_por_ano, analise_todos_os_anos, analise_com_ia

st.set_page_config(
    page_title="Análise de Violações",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# Sidebar (menu de navegação)
# =========================
st.sidebar.title("📊 Menu de Navegação")
pagina = st.sidebar.radio(
    "Selecione a página:",
    ("Dashboard Geral", "Análise por Ano", "Análise Todos os Anos", "Análises com IA")
)

if pagina == "Dashboard Geral":
    dashboard_geral()
elif pagina == "Análise por Ano":
    analise_por_ano()
elif pagina == "Análise Todos os Anos":
    analise_todos_os_anos()
elif pagina == "Análises com IA":
    analise_com_ia()
