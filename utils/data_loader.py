import streamlit as st
import pandas as pd
from db_connect import conectar

@st.cache_data
def carregar_dados():
    conn = conectar()

    query = """
    SELECT *
    FROM ed_enem_2024_resultados_amos_per
    """

    df = pd.read_sql(query, conn)
    conn.close()

    return df


def get_df():

    if "df_enem" not in st.session_state:
        st.session_state.df_enem = carregar_dados()

    return st.session_state.df_enem