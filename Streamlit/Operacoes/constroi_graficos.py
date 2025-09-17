import streamlit as st
import plotly.express as px


# =========================
# Função criação de gráficos de barras
# =========================
def grafico_barra(df, x, y, titulo, color=None):
    fig = px.bar(df,
                 x = x, 
                 y = y, 
                 color = color or x, 
                 text = y, 
                 title = titulo)
    fig.update_traces(texttemplate='%{text:,}', textposition="outside")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)



# =========================
# Função criação de gráficos de linhas
# =========================
def grafico_linhas(df, x, y, titulo):

    fig_totais = px.line(
        df,
        x = "Ano",
        y = "Frequência absoluta",
        markers = True,
        title = titulo,
        color_discrete_sequence = ["#007BFF"]
    )
    fig_totais.update_traces(line=dict(width=3))
    st.plotly_chart(fig_totais, use_container_width=True)


# =========================
# Função criação de gráficos de pizza
# =========================
def grafico_pizza(df, titulo, df_total = None):

    if df_total is None:
        
        df["Percentual (%)"] = ( ( df["count"] / ( df["count"].sum() ) ) * 100).round(2)
    else:
        df["Percentual (%)"] = ( ( df["count"] / ( df_total["count"].sum() ) ) * 100).round(2)

    fig = px.pie(
        df,
        values='Percentual (%)',
        names='Aparições',
        title=titulo,
        color_discrete_sequence=px.colors.qualitative.Set3,
        hole=0.4  # transforma em donut
    )

    fig.update_traces(
        textinfo='percent+label',
        hovertemplate="<b>%{label}</b><br>Casos: %{value}<br>Percentual: %{percent}"
    )

    st.plotly_chart(fig, use_container_width=True)


