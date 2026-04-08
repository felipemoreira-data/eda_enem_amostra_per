import pandas as pd
import streamlit as st
from utils.data_loader import get_df

st.set_page_config(page_title= "Enem amostra perfeita 2024",
                   layout = "wide")

st.sidebar.markdown('Desenvolvido por **Felipe Moreira**')
st.title('Análise exploratória do conjunto de dados ENEM amostra perfeita 2024')
st.subheader('Aluno: Felipe Melo')
st.subheader('Cursando: Ciência de Dados e IA')
st.subheader('Insituição: IESB')

st.divider()
df = get_df()

st.success("Dados carregados: ")
st.divider()

st.markdown('''
            O Exame Nacional do Ensino Médio (ENEM) constitui atualmente a principal avaliação educacional em larga escala do Brasil, 
            sendo utilizado tanto para mensurar o desempenho acadêmico dos estudantes ao final da educação básica quanto como mecanismo
            de acesso ao ensino superior por meio de programas como o Sistema de Seleção Unificada (SISU), o Programa Universidade para
            Todos (ProUni) e o Fundo de Financiamento Estudantil (FIES). Aplicado anualmente em todo o território nacional, o exame avalia
            competências e habilidades em diferentes áreas do conhecimento, incluindo Linguagens, Ciências Humanas, Ciências da Natureza, Matemática e Redação.

            ''')
st.divider()
st.dataframe(df.sample(10).dropna())    



