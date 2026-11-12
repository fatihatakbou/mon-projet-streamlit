import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Dashboard Analyse Taxis - Fatiha")


@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/taxis.csv"
    return pd.read_csv(url)


df = load_data()

# --- Filtre par quartier ---
boroughs = sorted(df["pickup_borough"].dropna().unique())
borough = st.selectbox("Choisissez un quartier de prise en charge :", boroughs)
df_filtre = df[df["pickup_borough"] == borough]

st.metric("Nombre de courses", f"{len(df_filtre):,}")
st.dataframe(df_filtre.head())

# --- Visualisation interactive ---
st.divider()
st.subheader("Visualisation interactive")

num_cols = df_filtre.select_dtypes(include="number").columns.tolist()

col_x = st.selectbox("Axe X :", num_cols, index=num_cols.index("distance"))
col_y = st.selectbox("Axe Y :", num_cols, index=num_cols.index("fare"))
chart_type = st.radio(
    "Type de graphique :",
    ["Streamlit (scatter)", "Plotly (interactif)"],
    horizontal=True,
)

if chart_type == "Streamlit (scatter)":
    st.scatter_chart(df_filtre, x=col_x, y=col_y)
else:
    fig = px.scatter(
        df_filtre,
        x=col_x,
        y=col_y,
        color="payment",
        hover_data=["pickup_zone"],
        title=f"{col_y} en fonction de {col_x}",
    )
    st.plotly_chart(fig, width="stretch")

# --- Matrice de corrélation ---
st.divider()
if st.checkbox("Afficher la matrice de corrélation"):
    st.subheader("Matrice de corrélation")
    corr = df_filtre[num_cols].corr()
    fig_corr, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig_corr)
