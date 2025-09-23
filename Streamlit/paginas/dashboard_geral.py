import pandas as pd
import streamlit as st

from operacoes import grafico_barra, grafico_linhas, carregar_dados_gerais_ano


def mostrar():
    # =========================
    # CONFIGURAÇÕES INICIAIS
    # =========================
    st.set_page_config(
        page_title="Dashboard de Violações",
        page_icon="📊",
        layout="wide"
    )

    # =========================
    # CAMINHO DOS DADOS
    # =========================
    
    dados_por_ano = carregar_dados_gerais_ano(remove_total = True)

    # Concatenar todos os anos para análises gerais
    df_geral = pd.concat(dados_por_ano.values(), ignore_index=True)

    # =========================
    # TÍTULO E INTRODUÇÃO
    # =========================
    st.title("📊 Panorama Geral das Violações de Direitos Humanos")
    st.markdown(
        """
        Esta página apresenta uma **visão geral** das denúncias de violações de direitos humanos registradas,
        destacando os **grupos mais vulneráveis** e a evolução dos casos ao longo dos anos.
        Use o menu lateral para explorar análises mais detalhadas.
        """
    )
    st.markdown("---")

    # =========================
    # KPIs — RESUMO ANUAL
    # =========================
    st.subheader("📌 Resumo Anual")
    colunas = st.columns(len(dados_por_ano))

    for idx, (ano, df) in enumerate(dados_por_ano.items()):
        total = df["Frequência absoluta"].sum()

        # Identificar o grupo mais afetado
        grupo_top = df.sort_values("Frequência absoluta", ascending=False).iloc[0]

        colunas[idx].metric(
            label=f"📅 {ano}",
            value=f"{total:,}".replace(",", "."),
            delta=f"{grupo_top['Grupo vulnerável']} ({grupo_top['Frequência absoluta']:,})"
        )

    st.markdown("---")

    # =========================
    # EVOLUÇÃO TOTAL DAS DENÚNCIAS
    # =========================
    st.subheader("📈 Evolução do Total de Violações")
    df_totais = df_geral.groupby("Ano")["Frequência absoluta"].sum().reset_index()

    grafico_linhas(
        df = df_totais,
        x = "Ano",
        y = "Frequência absoluta",
        titulo ="Evolução do Total de Violações",
    )


    st.markdown("---")

    # =========================
    # TOP 5 GRUPOS MAIS AFETADOS POR ANO
    # =========================
    st.subheader("🏆 Top 5 Grupos Vulneráveis por Ano")
    anos = st.multiselect(
        "Selecione os anos para visualizar",
        options=list(dados_por_ano.keys()),
        default=list(dados_por_ano.keys())
    )

    for ano in anos:
        df = dados_por_ano[ano]
        top5 = df.sort_values("Frequência absoluta", ascending=False).head(5)

        grafico_barra(
            df = top5,
            x = "Grupo vulnerável",
            y ="Frequência absoluta",
            titulo = f"Top 5 Grupos Vulneráveis em {ano}",
            color = "Grupo vulnerável"
        )


    st.markdown("---")

    # =========================
    # RANKING GERAL DOS GRUPOS
    # =========================
    st.subheader("📌 Ranking Geral dos Grupos Vulneráveis")
    df_ranking = df_geral.groupby("Grupo vulnerável")["Frequência absoluta"].sum().reset_index()
    df_ranking = df_ranking.sort_values("Frequência absoluta", ascending=False).head(10)

    grafico_barra(
        df = df_ranking,
        x = "Grupo vulnerável",
        y = "Frequência absoluta",
        titulo = "Top 10 Grupos Vulneráveis (Geral)",
        color = "Grupo vulnerável",
    )

    st.markdown("---")
    st.success("✅ Dashboard carregado com sucesso! Use o menu lateral para explorar análises detalhadas.")
