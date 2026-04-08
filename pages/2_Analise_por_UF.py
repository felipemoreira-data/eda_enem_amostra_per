import pandas as pd
import streamlit as st
import plotly.express as px
import geopandas as gpd

from utils.data_loader import get_df

url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"

brasil = gpd.read_file(url)

st.title('Análise por UF do conjunto amostral do ENEM')

df = get_df()

uf_selecionada = st.sidebar.selectbox('UF', 
                     df['nome_uf_prova'].sort_values(ascending= True).unique().tolist())


dist_uf = (df['sg_uf_prova'].value_counts().reset_index())
dist_uf.columns = ['UF', 'Quantidade']

fig = px.bar(dist_uf.sort_values('Quantidade', ascending= False),
             x = 'UF',
             y = 'Quantidade',
             text_auto= True,
             title = "Número de Participantes por UF")


st.plotly_chart(fig, use_container_width= True)


st.divider()

mapa_df = df.groupby('sg_uf_prova').agg(
    média_5_notas_uf = ('nota_media_5_notas', 'mean'),
    participantes = ('nu_sequencial', 'count')
).reset_index()

mapa = brasil.merge(mapa_df, left_on='sigla', right_on= 'sg_uf_prova')

import plotly.express as px

fig = px.choropleth_mapbox(
    mapa,
    geojson=mapa.geometry,
    locations=mapa.index,
    color='média_5_notas_uf',
    hover_name='sigla',
    hover_data=['participantes'],
    mapbox_style="carto-positron",
    center={"lat": -14, "lon": -52},
    zoom=3.5,
    opacity=0.7,
    color_continuous_scale= 'Reds',
    title="Média de notas da prova geral por UF"
)

fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})

col1, col2 = st.columns(2)
col1.plotly_chart(fig)
col2.write(mapa_df.sort_values(by = 'média_5_notas_uf', ascending= False))

st.divider()

intervalo_selecionado = st.sidebar.slider('Intervalo de nota desejado',
                  min_value=300,
                  max_value = 1_000,
                  value =300)

st.subheader(f'Quantidade de Alunos por Nota — {uf_selecionada}')
st.caption(f'Notas ≥ {intervalo_selecionado}')

col3, col4, col5, col6, col7 = st.columns(5)
col3.metric(f'Ciências da natureza', value = f'{df[(df['nome_uf_prova'] == uf_selecionada) & (df['nota_cn_ciencias_da_natureza'] >= intervalo_selecionado)].shape[0]}')
col4.metric(f'Ciências humanas', value = f'{df[(df['nome_uf_prova'] == uf_selecionada) & (df['nota_ch_ciencias_humanas'] >= intervalo_selecionado)].shape[0]}')
col5.metric(f'Redação', value = f'{df[(df['nome_uf_prova'] == uf_selecionada) & (df['nota_redacao'] >= intervalo_selecionado)].shape[0]}')
col6.metric(f'Linguagens e códigos', value = f'{df[(df['nome_uf_prova'] == uf_selecionada) & (df['nota_lc_linguagens_e_codigos'] >= intervalo_selecionado)].shape[0]}')
col7.metric(f'Matemática', value = f'{df[(df['nome_uf_prova'] == uf_selecionada) & (df['nota_mt_matematica'] >= intervalo_selecionado)].shape[0]}')

import pandas as pd

dados = pd.DataFrame({
    'Área': [
        'Ciências da Natureza',
        'Ciências Humanas',
        'Linguagens',
        'Matemática',
        'Redação'
    ],
    'Quantidade': [
        df[(df['nome_uf_prova'] == uf_selecionada) & (df['nota_cn_ciencias_da_natureza'] >= intervalo_selecionado)].shape[0],
        df[(df['nome_uf_prova'] == uf_selecionada) & (df['nota_ch_ciencias_humanas'] >= intervalo_selecionado)].shape[0],
        df[(df['nome_uf_prova'] == uf_selecionada) & (df['nota_redacao'] >= intervalo_selecionado)].shape[0],
        df[(df['nome_uf_prova'] == uf_selecionada) & (df['nota_lc_linguagens_e_codigos'] >= intervalo_selecionado)].shape[0],
        df[(df['nome_uf_prova'] == uf_selecionada) & (df['nota_mt_matematica'] >= intervalo_selecionado)].shape[0]
    ]
})
fig = px.scatter(
    dados,
    x='Quantidade',
    y='Área',
    size='Quantidade',        # tamanho do ponto
    text='Quantidade',        # mostra valor
    title=f'Alunos com nota ≥ {intervalo_selecionado}'
)

fig.update_traces(textposition='middle right')

st.plotly_chart(fig, use_container_width=True)
