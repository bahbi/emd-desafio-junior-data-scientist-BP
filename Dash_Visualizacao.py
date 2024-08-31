import streamlit as st
#import requests
import pandas as pd
import plotly.express as px


st.title("Título aqui") 

## Visualização no streamlit
aba1, aba2 = st.tabs(['Chamados', 'Sobre o clima'])

#Dados
Chamados_1746_04_01 = pd.read_csv('./Dados_1/df_chamados_parte1.csv', delimiter=',')
#df1 = pd.read_csv('/content/chamados_parte1.csv', delimiter=',')
df_bairros = pd.read_csv('./Dados_1/bairros_rj.csv', delimiter=',')

# Selecionar os dados relevantes
df1_selecionado = Chamados_1746_04_01[['id_chamado', 'data_inicio', 'id_bairro', 'tipo',
                       'subtipo', 'status', 'longitude', 'latitude', 'reclamacoes']] #, 'geometry'
df_selecionado_bairros = df_bairros[['id_bairro', 'nome', 'subprefeitura']]
df_uniao_chamados_bairros = pd.merge(df1_selecionado, df_selecionado_bairros, on='id_bairro', how='left')

#Funções aqui

#Organiza geral
st.markdown("*Streamlit* is **really** ***cool***.")

# Conteúdo da aba1 - exibição do DataFrame

aba1.metric('Quantidade de Chamados', Chamados_1746_04_01.shape[0])
aba1.subheader("Chamados - DataFrame Visualização")
aba1.dataframe(Chamados_1746_04_01)

# Adição do novo conteúdo na aba1
# Obtendo a contagem de ocorrências por tipo
ocorrencias_por_tipo = Chamados_1746_04_01['tipo'].value_counts()
df_ocorrencias_por_tipo = pd.DataFrame({'tipo': ocorrencias_por_tipo.index, 'contagem': ocorrencias_por_tipo.values})

# Criando o gráfico de barras
fig_tipo = px.bar(df_ocorrencias_por_tipo.head(10), x='contagem', y='tipo', orientation='h',
                  labels={'contagem': 'Quantidade', 'tipo': 'Tipo de Ocorrência'},
                  title='Top 10 Tipos de Ocorrências')

# Personalizando as cores do gráfico
fig_tipo.update_traces(marker_color='rgb(253, 180, 98)')

# Exibindo o gráfico de barras na aba1
aba1.subheader("Chamados - Gráfico de Barras por Tipo de Ocorrência")
aba1.plotly_chart(fig_tipo)

#------------------------------------------------------
# Conteúdo da aba1 - exibição do gráfico
aba1.subheader("Chamados - Gráfico de Linha")
aba1.line_chart(Chamados_1746_04_01)

aba2.subheader("A tab with the data") 
#tab2.write(data)
#st.dataframe(Chamados_1746_04_01)

