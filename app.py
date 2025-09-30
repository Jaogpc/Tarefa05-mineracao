import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------------------------
# 2. Configuração do Dashboard (deve ser a 1ª chamada Streamlit)
# -----------------------------------------------------------
st.set_page_config(
    page_title="Dashboard Spotify",
    page_icon="🎵",
    layout="wide"
)

# -----------------------------------------------------------
# 1. Carregamento e Preparação dos Dados
# -----------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    # Tratamento de valores ausentes
    df = df.dropna(subset=["artists", "year", "popularity"])
    df["year"] = df["year"].astype(int)
    return df

df = load_data()

st.title("🎶 Dashboard Spotify")
st.markdown("""
Este dashboard interativo foi desenvolvido a partir do **Spotify Dataset (Kaggle)**, 
com músicas lançadas entre 1921 e 2020.  
Aqui você pode explorar tendências, artistas e métricas relacionadas ao dataset.
""")

# -----------------------------------------------------------
# 3. Filtros na Barra Lateral
# -----------------------------------------------------------
st.sidebar.header("Filtros")

anos = st.sidebar.slider(
    "Selecione o intervalo de anos:",
    int(df["year"].min()),
    int(df["year"].max()),
    (1990, 2020)
)

artistas = st.sidebar.multiselect(
    "Selecione artistas:",
    options=sorted(df["artists"].unique()),
    default=[]
)

# Aplicação dos filtros
df_filtrado = df[(df["year"] >= anos[0]) & (df["year"] <= anos[1])]

if artistas:
    df_filtrado = df_filtrado[df_filtrado["artists"].isin(artistas)]

# -----------------------------------------------------------
# 4. KPIs (Métricas Principais)
# -----------------------------------------------------------
total_musicas = len(df_filtrado)
artista_mais_frequente = df_filtrado["artists"].mode()[0] if total_musicas > 0 else "-"
media_popularidade = round(df_filtrado["popularity"].mean(), 2) if total_musicas > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("🎵 Total de músicas", total_musicas)
col2.metric("👨‍🎤 Artista mais frequente", artista_mais_frequente)
col3.metric("⭐ Média de Popularidade", media_popularidade)

# -----------------------------------------------------------
# 5. Gráficos Interativos
# -----------------------------------------------------------

if total_musicas > 0:
    # Top 10 artistas
    top_artistas = (
        df_filtrado["artists"].value_counts().head(10).reset_index()
    )
    top_artistas.columns = ["Artista", "Quantidade"]

    fig_bar = px.bar(
        top_artistas,
        x="Artista",
        y="Quantidade",
        title="Top 10 Artistas com Mais Músicas",
        text="Quantidade"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Distribuição por década
    df_filtrado["Década"] = (df_filtrado["year"] // 10) * 10
    dist_decada = df_filtrado["Década"].value_counts().reset_index()
    dist_decada.columns = ["Década", "Quantidade"]

    fig_pizza = px.pie(
        dist_decada,
        names="Década",
        values="Quantidade",
        title="Distribuição das Músicas por Década"
    )
    st.plotly_chart(fig_pizza, use_container_width=True)

# -----------------------------------------------------------
# 6. Tabela Dinâmica
# -----------------------------------------------------------
st.subheader("📋 Dados Filtrados")
st.dataframe(df_filtrado)
