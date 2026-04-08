import streamlit as st

def sidebar_filters(df):

    st.sidebar.header("Filtros Globais")

    uf = st.sidebar.selectbox(
        "UF",
        sorted(df["sg_uf_prova"].dropna().unique()),
        key="uf"
    )

    nota_range = st.sidebar.slider(
        "Faixa Nota CN",
        0,
        1000,
        (400, 800),
        key="nota_range"
    )

    return uf, nota_range