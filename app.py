import streamlit as st
import pandas as pd

st.title("Dashboard Analyse Taxis - Fatiha")


@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/taxis.csv"
    return pd.read_csv(url)


df = load_data()

boroughs = sorted(df["pickup_borough"].dropna().unique())
borough = st.selectbox("Choisissez un quartier de prise en charge :", boroughs)

df_filtre = df[df["pickup_borough"] == borough]

st.metric("Nombre de courses", f"{len(df_filtre):,}")
st.dataframe(df_filtre.head())
