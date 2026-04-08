import pandas as pd
import streamlit as st
import plotly.express as px
from utils.data_loader import get_df

df = get_df()

st.title('Análise do Perfil do candidato do conjunto amostral do ENEM')


st.header('Quantidade de Candidatos por zona (Rural e Urbana)')


valores_sit= ['Rural', 'Urbana']
df['tp_localizacao_esc'] = df['tp_localizacao_esc'].str.strip()
df['tp_dependencia_adm_esc'] = df['tp_dependencia_adm_esc'].str.strip()

df_bar = df.groupby(['sg_uf_prova','tp_localizacao_esc']).agg(
    quantidade = ('tp_localizacao_esc', 'count'),
    media = ('nota_media_5_notas', 'mean')
).reset_index()

df_bar= df_bar[(df_bar['tp_localizacao_esc']).isin(valores_sit)]

fig = px.bar(
    df_bar,
    x = 'sg_uf_prova',
    y = 'quantidade',
    color = 'tp_localizacao_esc',
    barmode = 'group',
    text = 'quantidade'
)
fig.update_traces(textposition = 'outside')
st.plotly_chart(fig, use_container_width= True)

st.divider()

df2 = df.copy()
df2 = df2[(df2['tp_localizacao_esc']).isin(valores_sit)]


st.header('Ditribuição das médias de notas por zona (Rural e Urbana)')
fig = px.box(
    df2,
    x='tp_localizacao_esc',
    y='nota_media_5_notas',
    color='tp_localizacao_esc',
    points = 'outliers'
)

st.plotly_chart(fig, use_container_width=True)



st.divider()
st.header('Candidados por DP escolar')
col3, col4 = st.columns(2)


df_dep = df.groupby('tp_dependencia_adm_esc').agg(
    quantidade = ('nu_sequencial', 'count')
).reset_index()

ls_dependencia = ['Estadual', 'Privada', 'Federal', 'Municipal']
df_dep = df_dep[df_dep['tp_dependencia_adm_esc'].isin(ls_dependencia)]

fig = px.pie(
    df_dep,
    names = 'tp_dependencia_adm_esc',
    values = 'quantidade',
    title = 'Quantidade de candidatos por DP escolar'
)

col3.plotly_chart(fig, use_container_width= True)

uf_selecionada = st.sidebar.selectbox(
    'UF',
    df['sg_uf_prova'].unique().tolist()
)

df_filt = df[df['sg_uf_prova'] == uf_selecionada]

df_tree = (
    df_filt.groupby('tp_dependencia_adm_esc').size().reset_index(name = 'participantes')
)
df_tree = df_tree[(df_tree['tp_dependencia_adm_esc']).isin(ls_dependencia)]


fig = px.treemap(df_tree,
                 path = ['tp_dependencia_adm_esc'],
                 values = 'participantes',
                 color = 'tp_dependencia_adm_esc',
                 title = f'Distribuição dos Participantes por DP escolar - {uf_selecionada}')
fig.update_traces(textinfo = 'label+percent entry')
col4.plotly_chart(fig, use_container_width= True)


st.divider()
st.header('Distribuição das médias de notas em função da dependência admnistrativa')

fig = px.strip(
    df,
    x='tp_dependencia_adm_esc',
    y='nota_media_5_notas',
    color='tp_dependencia_adm_esc'
)

st.plotly_chart(fig)