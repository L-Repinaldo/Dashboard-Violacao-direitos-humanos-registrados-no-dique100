import streamlit as st
import pandas as pd
import plotly.express as px

from Operacoes.carregar_dados import carregar_dados_gerais_ano, carregar_dados_grupos_vulneraveis

# =========================
# Carrega todos os dados de todos os anos (visão geral)
# =========================
@st.cache_data
def carregar_todos_os_dados():
    return carregar_dados_gerais_ano()

# =========================  
# Cache dos dados detalhados por grupo
# =========================
@st.cache_data
def carregar_dados_grupo(ano, grupo):
    primeiro = carregar_dados_grupos_vulneraveis(
        anos=ano, grupos=grupo, semestre="primeiro", to_pandas=True
    )
    segundo = carregar_dados_grupos_vulneraveis(
        anos=ano, grupos=grupo, semestre="segundo", to_pandas=True
    )
    if primeiro is None or segundo is None:
        return None
    return pd.concat([primeiro, segundo], ignore_index=True)

# =========================
# Contar moda por coluna (removendo N/D e NaN)
# =========================
def moda_coluna(df, coluna):
    if df is None or coluna not in df.columns:
        return None, 0

    # remove N/D e valores nulos
    df_valid = df[df[coluna].notna() & (df[coluna].str.strip().str.upper() != "N/D")]

    if df_valid.empty:
        return None, 0

    contagem = df_valid[coluna].value_counts()
    return contagem.index[0], contagem.iloc[0]

# =========================
# Página principal
# =========================
def mostrar():
    dados_por_ano = carregar_todos_os_dados()

    lista_df = []
    for ano, df in dados_por_ano.items():
        df_filtrado = df[df["Grupo vulnerável"].str.strip().str.lower() != "total geral"].copy()
        df_filtrado["Ano"] = ano
        lista_df.append(df_filtrado)

    df_todos = pd.concat(lista_df, ignore_index=True)

    grupos = sorted(df_todos["Grupo vulnerável"].unique())
    grupo_escolhido = st.selectbox("Selecione o grupo vulnerável:", grupos)

    df_filtrado = df_todos[df_todos["Grupo vulnerável"] == grupo_escolhido]

    # =========================
    # KPIs principais
    # =========================
    total = df_filtrado["Frequência absoluta"].sum()
    pico_ano = df_filtrado.groupby("Ano")["Frequência absoluta"].sum().idxmax()
    pico_valor = df_filtrado.groupby("Ano")["Frequência absoluta"].sum().max()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de denúncias (2020-2024)", f"{total:,}".replace(",", "."))
    col2.metric("Ano com maior volume", f"{pico_ano}", f"{pico_valor:,}".replace(",", "."))
    col3.metric("Crescimento 2020 → 2024", 
                f"{(df_filtrado[df_filtrado['Ano']==2024]['Frequência absoluta'].sum() / df_filtrado[df_filtrado['Ano']==2020]['Frequência absoluta'].sum() - 1):.1%}")

    # =========================
    # Gráfico temporal
    # =========================
    st.write(f"### Evolução temporal — {grupo_escolhido}")
    df_agrupado = df_filtrado.groupby("Ano")["Frequência absoluta"].sum().reset_index()
    fig = px.line(df_agrupado, x="Ano", y="Frequência absoluta", markers=True,
                  title=f"Evolução das ocorrências ({grupo_escolhido})")
    fig.update_traces(line=dict(width=3))
    st.plotly_chart(fig, use_container_width=True)

    # =========================
    # Modas por ano em categorias selecionadas
    # =========================
    categorias = [
        "Cenário_da_violação", "UF", "Denunciante", "violacao",
        "Relação_vítima_suspeito", "motivacoes", 
        "Gênero_da_vítima", "Faixa_etária_da_vítima", "Faixa_etária_do_suspeito"
    ]

    st.write("### Categorias mais recorrentes por ano")
    modas = []
    for ano in sorted(dados_por_ano.keys()):
        df_detalhe = carregar_dados_grupo(ano, grupo_escolhido)
        if df_detalhe is None:
            continue
        linha = {"Ano": ano}
        for cat in categorias:
            valor, freq = moda_coluna(df_detalhe, cat)
            linha[cat] = valor
        modas.append(linha)

    if modas:
        df_modas = pd.DataFrame(modas)
        st.dataframe(df_modas, use_container_width=True)

    # =========================
    # Narrativa automática
    # =========================
    st.write("### Resumo automático")
    resumo = f"""
    Entre 2020 e 2024, o grupo **{grupo_escolhido}** acumulou **{total:,} denúncias**.  
    O ano de maior ocorrência foi **{pico_ano}**, com **{pico_valor:,} registros**.  
    As categorias mais frequentes variaram por ano, mas a tabela acima mostra os destaques.
    """
    st.info(resumo)
