import pandas as pd
import streamlit as st

from Operacoes.carregar_dados import carregar_dados_gerais_ano, carregar_dados_grupos_vulneraveis
from Operacoes.contar_ocorrencias_por_coluna import contar_ocorrencias_por_coluna
from Operacoes.constroi_graficos import grafico_barra, grafico_pizza
from Operacoes.normaliza_dados import normalizar_categoria_faixa_etaria, normalizar_categoria_motivacao


# =========================
# Cache dos dados gerais
# =========================
@st.cache_data
def carregar_dados_ano():
    return carregar_dados_gerais_ano()


# =========================  
# Cache dos dados detalhados por grupo
# =========================
@st.cache_data
def carregar_dados_grupo(ano, grupo):
    primeiro = carregar_dados_grupos_vulneraveis(anos=ano, grupos=grupo, semestre="primeiro", to_pandas=True)
    segundo = carregar_dados_grupos_vulneraveis(anos=ano, grupos=grupo, semestre="segundo", to_pandas=True)
    return primeiro, segundo


# =========================
# Contar ocorrências de colunas
# =========================
def contar_frequencias(df1, df2, colunas):
    return {coluna: contar_ocorrencias_por_coluna(df1, df2, coluna) for coluna in colunas}


# =========================
# Resumo geral
# =========================
def resumo_geral(frequencias, total_grupo, perc_grupo, grupo, ano):
    partes = []

    partes.append(f"**Resumo Geral — {grupo} ({ano})**")
    partes.append(f"- Total de denúncias: {total_grupo:,}".replace(",", "."))
    partes.append(f"- Participação no ano: {perc_grupo:.2f}%")

    principais = {
        "UF": frequencias["UF"],
        "Gênero da vítima": frequencias["Gênero_da_vítima"],
        "Faixa etária vítima": frequencias["Faixa_etária_da_vítima"],
        "Faixa etária suspeito": frequencias["Faixa_etária_do_suspeito"],
        "Tipo de violação": frequencias["violacao"],
        "Cenário": frequencias["Cenário_da_violação"],
        "Relação vítima x suspeito": frequencias["Relação_vítima_suspeito"],
        "Motivação": frequencias["motivacoes"],
        "Denunciante": frequencias["Denunciante"],
    }

    for nome, df in principais.items():
        if not df.empty:
            df = df.copy()
            # Remover "N/D" e similares
            df = df[~df["Aparições"].str.upper().isin(["N/D", "ND", "NÃO INFORMADO"])]
            
            if not df.empty:
                maior = df.sort_values(by="count", ascending=False).iloc[0]
                percentual = (maior["count"] / total_grupo) * 100
                partes.append(
                    f"- {nome} mais recorrente: **{maior['Aparições']}** ({percentual:.2f}%)"
                )

    return "\n".join(partes)




# =========================
# Página principal
# =========================
def mostrar():
    dados_por_ano = carregar_dados_ano()

    st.title("📅 Análise Anual")
    anos = sorted(dados_por_ano.keys())
    ano_escolhido = st.selectbox("Selecione o ano:", anos)
    df_ano = dados_por_ano[ano_escolhido]

    # Remove "Total Geral" para gráficos, mas mantém para KPIs
    df_sem_total = df_ano[df_ano["Grupo vulnerável"].str.strip().str.lower() != "total geral"]
    grupos = sorted(df_sem_total["Grupo vulnerável"].unique())
    grupo_escolhido = st.selectbox("Selecione o grupo vulnerável:", grupos)

    # Dados filtrados
    df_grupo_total = df_ano[df_ano["Grupo vulnerável"] == grupo_escolhido]
    df_total_ano = df_ano[df_ano["Grupo vulnerável"].str.strip().str.lower() == "total geral"]

    # Carregar detalhamento por semestre
    df_primeiro, df_segundo = carregar_dados_grupo(ano_escolhido, grupo_escolhido)


    # =========================
    # Contagem de frequências para múltiplas colunas
    # =========================
    colunas_freq = [
        "Cenário_da_violação", "UF", "Denunciante", "violacao",
        "Relação_vítima_suspeito", "motivacoes", "Gênero_da_vítima",
        "Faixa_etária_da_vítima", "Faixa_etária_do_suspeito"
    ]
    frequencias = contar_frequencias(df_primeiro, df_segundo, colunas_freq)


    # =========================
    # KPIs principais
    # =========================
    total_ano = df_total_ano["Frequência absoluta"].iloc[0]
    total_grupo = df_grupo_total["Frequência absoluta"].iloc[0]
    perc_grupo = df_grupo_total["Frequência relativa (%)"].iloc[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total no Ano", f"{total_ano:,}".replace(",", "."))
    col2.metric(f"Total — {grupo_escolhido}", f"{total_grupo:,}".replace(",", "."))
    col3.metric("Participação (%)", f"{perc_grupo:.2f}%")

    st.markdown("---")


    # =========================
    # Resumo Geral
    # =========================
    st.subheader("📌 Resumo Geral")
    st.markdown(resumo_geral(frequencias, total_grupo, perc_grupo, grupo_escolhido, ano_escolhido))
    st.markdown("---")

    # =========================
    # Comparativo entre semestres
    # =========================
    st.subheader(f"Comparação entre semestres ({grupo_escolhido} — {ano_escolhido})")

    total_primeiro = len(df_primeiro)
    total_segundo = len(df_segundo)

    freq_primeiro = total_primeiro / total_grupo
    freq_segundo = total_segundo / total_grupo

    df_compara_semestres = pd.DataFrame({
        "Semestre": ["Primeiro", "Segundo", "Total"],
        "Total denúncias": [total_primeiro, total_segundo, total_grupo],
        "Frequência relativa (%)": [freq_primeiro * 100, freq_segundo * 100, 100],
    })

    grafico_barra(
        df=df_compara_semestres,
        x="Semestre",
        y="Total denúncias",
        titulo=f"Ocorrências do grupo '{grupo_escolhido}' em {ano_escolhido}",
        color="Semestre"
    )

    col4, col5 = st.columns(2)
    col4.metric("Percentual Primeiro Semestre", f"{df_compara_semestres.iloc[0, 2]:.2f}%")
    col5.metric("Percentual Segundo Semestre", f"{df_compara_semestres.iloc[1, 2]:.2f}%")

    st.markdown("---")


    # =========================
    # Comparativo gênero das vítimas 
    # =========================
    st.subheader("Comparativo gênero das vítimas")
    df_genero = frequencias['Gênero_da_vítima']
    df_genero = df_genero.sort_values(by="count", ascending=False)
    grafico_barra(
        df=df_genero,
        x="Aparições",
        y="count",
        titulo=f"Número de casos por Gênero_da_vítima ({grupo_escolhido} — {ano_escolhido})",
        color="Aparições"
    )

    st.markdown("---")


    
    # =========================
    # Denúncias por UF
    # =========================
    st.subheader("Denúncias por UF")
    df_uf = frequencias["UF"]
    df_uf = df_uf.sort_values(by="count", ascending=False)
    grafico_barra(
        df=df_uf,
        x="Aparições",
        y="count",
        titulo=f"Número de casos por UF ({grupo_escolhido} — {ano_escolhido})",
        color="Aparições"
    )

    st.markdown("---")

    # =========================
    # Relações vítima x suspeito
    # =========================

    st.subheader("Relação Vítima x Suspeito")
    df_relacao_vitima_x_suspeito = frequencias["Relação_vítima_suspeito"]
    df_relacao_vitima_x_suspeito_top5 = df_relacao_vitima_x_suspeito.sort_values(by="count", ascending=False).head(5)
    grafico_pizza(df = df_relacao_vitima_x_suspeito_top5, titulo="Distribuição Relação Vítima x Suspeito - Top5", df_total = df_relacao_vitima_x_suspeito)

    st.markdown("---")

    # =========================
    # Tabelas Faixa etária Vítima e Suspeito
    # =========================
    st.subheader("Tabela Faixa etária vítima - Top5")

    df_idade_vitima = frequencias['Faixa_etária_da_vítima']
    df_idade_vitima = normalizar_categoria_faixa_etaria(df = df_idade_vitima , coluna = "Aparições")

    if not df_idade_vitima.empty:
        total_de_classes = df_idade_vitima['count'].sum()
        df_idade_vitima['Frequência Relativa (%)'] = (df_idade_vitima['count'] / total_de_classes) * 100
        df_top5_idades_vit = df_idade_vitima.sort_values(by="count", ascending=False).head(5)
        st.table(df_top5_idades_vit)
    else:
        st.info("Sem dados para faixa etária vítimas.")

    st.markdown("---")

    st.subheader("Tabela Faixa etária suspeito - Top5")

    df_idade_suspeito = frequencias['Faixa_etária_do_suspeito']
    df_idade_suspeito = normalizar_categoria_faixa_etaria(df = df_idade_suspeito , coluna = "Aparições")

    if not df_idade_suspeito.empty:
        total_de_classes = df_idade_suspeito['count'].sum()
        df_idade_suspeito['Frequência Relativa (%)'] = (df_idade_suspeito['count'] / total_de_classes) * 100
        df_top5_idades_susp = df_idade_suspeito.sort_values(by="count", ascending=False).head(5)
        st.table(df_top5_idades_susp)
    else:
        st.info("Sem dados para faixa etária vítimas.")

    st.markdown("---")

    # =========================
    # Distribuição Violações 
    # =========================
    st.subheader("Distribuição dos Tipos de Violações")
    df_violacoes = frequencias['violacao']
    df_violacoes_top5 = df_violacoes.sort_values(by="count", ascending=False).head(5)
    grafico_barra(
        df = df_violacoes_top5,
        x = 'Aparições',
        y = 'count',
        titulo = f"Top 5 tipos de violações ({grupo_escolhido} - {ano_escolhido})",
        color = 'Aparições'
    )

    st.markdown("---")

    # =========================
    # Cenários de violação
    # =========================
    st.subheader("Cenários de Violação")
    df_cenario = frequencias["Cenário_da_violação"]
    if not df_cenario.empty:
        total_cenario = df_cenario['count'].sum()
        df_cenario["Frequência Relativa (%)"] = (df_cenario['count'] / total_cenario) * 100
        df_cenario = df_cenario.sort_values(by="count", ascending=False)
        st.table(df_cenario)
        st.caption(
            "As categorias foram mantidas conforme registradas no sistema de origem, "
            "podendo apresentar variações de grafia ou duplicações aparentes."
        )
    else:
        st.info("Sem dados para cenários de violação.")

    st.markdown("---")

    # =========================
    # Motivações
    # =========================
    st.subheader("Motivações - Top5")
    df_motivacao = frequencias['motivacoes']
    df_motivacao = normalizar_categoria_motivacao(df = df_motivacao, coluna ="Aparições" )

    if not df_motivacao.empty:
        total_motivacao = df_motivacao['count'].sum()
        df_motivacao['Frequência Relativa (%)'] = (df_motivacao['count'] / total_motivacao) * 100
        df_top5_motivacoes = df_motivacao.sort_values(by="count", ascending=False).head(5)
        st.table(df_top5_motivacoes)
    else:
        st.info("Sem dados para motivações.")
    
    st.markdown("---")


    # =========================
    # Tipo de denunciantes
    # =========================
    st.subheader("Distribuição dos Denunciantes")
    grafico_pizza(df=frequencias["Denunciante"], titulo="Distribuição dos denunciantes", df_total = None)

    st.markdown("---")