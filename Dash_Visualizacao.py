import streamlit as st
#import requests
import pandas as pd
import plotly.express as px


st.title("Título aqui") 

## Visualização no streamlit
aba1, aba2 = st.tabs(['Chamados', 'Sobre o clima'])

Chamados_1746_04_01 = pd.read_csv('./Dados_1/df_chamados_parte1.csv', delimiter=',')

st.markdown("*Streamlit* is **really** ***cool***.")

# Conteúdo da aba1 - exibição do DataFrame
aba1.subheader("Chamados - DataFrame Visualização")
aba1.dataframe(Chamados_1746_04_01)

# Conteúdo da aba1 - exibição do gráfico
aba1.subheader("Chamados - Gráfico de Linha")
aba1.line_chart(Chamados_1746_04_01)

aba2.subheader("A tab with the data") 
#tab2.write(data)
#st.dataframe(Chamados_1746_04_01)

