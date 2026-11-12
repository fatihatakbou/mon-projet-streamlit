import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu

# ------------------------------
# Authentification
# ------------------------------

def verifier_connexion(username, password):
    users = pd.read_csv("accounts.csv")

    user = users[
        (users["username"] == username)
        & (users["password"] == password)
    ]

    return not user.empty


if "connected" not in st.session_state:
    st.session_state.connected = False


# ------------------------------
# Page Login
# ------------------------------

if not st.session_state.connected:

    st.title("Connexion")

    username = st.text_input("Nom utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):

        if verifier_connexion(username, password):
            st.session_state.connected = True
            st.rerun()

        else:
            st.error("Identifiants incorrects")

# ------------------------------
# Application
# ------------------------------

else:

    with st.sidebar:

        selected = option_menu(
            "Menu",
            ["Accueil", "Dashboard", "Galerie"],
            icons=["house", "bar-chart", "images"],
            default_index=0
        )

        st.divider()

        if st.button("Déconnexion"):
            st.session_state.connected = False
            st.rerun()

    # --------------------------
    # Accueil
    # --------------------------

    if selected == "Accueil":

        st.title("DataInsight Solutions")

        st.success("Authentification réussie")

        st.write(
            "Bienvenue sur l'application d'analyse des taxis."
        )

    # --------------------------
    # Dashboard
    # --------------------------

    elif selected == "Dashboard":

        st.title("Dashboard Analyse Taxis - Fatiha")

        @st.cache_data
        def load_data():
            url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/taxis.csv"
            return pd.read_csv(url)

        df = load_data()

        boroughs = sorted(
            df["pickup_borough"].dropna().unique()
        )

        borough = st.selectbox(
            "Choisissez un quartier de prise en charge :",
            boroughs
        )

        df_filtre = df[
            df["pickup_borough"] == borough
        ]

        st.metric(
            "Nombre de courses",
            f"{len(df_filtre):,}"
        )

        st.dataframe(df_filtre.head())

        st.divider()

        st.subheader(
            "Visualisation interactive"
        )

        num_cols = df_filtre.select_dtypes(
            include="number"
        ).columns.tolist()

        col_x = st.selectbox(
            "Axe X",
            num_cols,
            index=num_cols.index("distance")
        )

        col_y = st.selectbox(
            "Axe Y",
            num_cols,
            index=num_cols.index("fare")
        )

        chart_type = st.radio(
            "Type de graphique",
            [
                "Streamlit",
                "Plotly"
            ],
            horizontal=True
        )

        if chart_type == "Streamlit":

            st.scatter_chart(
                df_filtre,
                x=col_x,
                y=col_y
            )

        else:

            fig = px.scatter(
                df_filtre,
                x=col_x,
                y=col_y,
                color="payment",
                hover_data=["pickup_zone"]
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.divider()

        if st.checkbox(
            "Afficher la matrice de corrélation"
        ):

            corr = df_filtre[num_cols].corr()

            fig_corr, ax = plt.subplots(
                figsize=(6, 4)
            )

            sns.heatmap(
                corr,
                annot=True,
                cmap="coolwarm",
                fmt=".2f",
                ax=ax
            )

            st.pyplot(fig_corr)

    # --------------------------
    # Galerie
    # --------------------------

    elif selected == "Galerie":

        st.title("Galerie")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.image(
                "https://picsum.photos/300/200?1"
            )

        with col2:
            st.image(
                "https://picsum.photos/300/200?2"
            )

        with col3:
            st.image(
                "https://picsum.photos/300/200?3"
            )