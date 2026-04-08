import streamlit as st
import pandas as pd
import plotly.express as px


from utils.data_loader import get_df



st.title('Análise Geral do Conjunto Amostral do ENEM')
st.subheader('Análise da Média das 5 notas dos candidatos')


df = get_df()

#uf, nota_range = sidebar_filters(df)

#df_filtrado = df[df['sg_uf_prova'] == uf]


col1, col2, col3 = st.columns(3)
col1.metric(f'**Número total de participantes da amostra:**', value = f'{df['nu_sequencial'].nunique()}')
col2.metric(f'**Média geral das notas dos participantes da amostra**', value = f'{df['nota_media_5_notas'].mean():.2f}')
col3.metric(f'**Mediana das notas dos participantes da amostra**', value = f'{df['nota_media_5_notas'].median():.2f}')


fig = px.histogram(data_frame= df,
                   x = 'nota_media_5_notas',
                   nbins = 70,
                   title = 'Distribuição da Média dos Participantes',
                   opacity= 0.7)
st.plotly_chart(fig)


st.divider()



areas_dic = {'nota_mt_matematica' : 'Matemática',
            'nota_cn_ciencias_da_natureza' : 'Ciências da Natureza',
            'nota_ch_ciencias_humanas': 'Ciências Humanas',
            'nota_lc_linguagens_e_codigos': 'Linguagens e Códigos',
            'nota_redacao': 'Redação'}

area_selecionada = st.sidebar.selectbox('Área: ',
                                        areas_dic.values())
st.subheader(f'Análise da nota de {area_selecionada} dos candidatos')

coluna_escolhida = [key for key, value in areas_dic.items() if value == area_selecionada][0]

col4, col5, col6, col7 = st.columns(4)
col4.metric(f'**Média da Dsitribuição**', value = f'{df[coluna_escolhida].mean():.2f}')
col5.metric(f'**Mediana da distribuição**', value = f'{df[coluna_escolhida].median():.2f}')
col6.metric(f'**Desvio Padrão da distribuição**', value = f'{df[coluna_escolhida].std():.2f}')
col7.metric(f'**Valor modal da distribuição**', value = f'{df[coluna_escolhida].mode().iloc[0]:.2f}')

fig = px.histogram(data_frame= df,
                   x = coluna_escolhida,
                   nbins = 70,
                   marginal = 'box',
                   title = f'Distribuição da nota de {area_selecionada} dos Participantes',
                   opacity= 0.7)
st.plotly_chart(fig)