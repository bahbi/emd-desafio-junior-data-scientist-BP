import streamlit as st
#import requests
import pandas as pd
import plotly.express as px


st.title("Título aqui") 

## Visualização no streamlit
aba1, aba2 = st.tabs(['Chamados', 'Sobre o clima'])

Chamados_1746_04_01 = pd.read_csv('./Dados_1/df_chamados_parte1.csv', delimiter=',')

st.markdown("*Streamlit* is **really** ***cool***.")

aba1.subheader("A tab with a chart")
#tab1.line_chart(data)

aba2.subheader("A tab with the data")
#tab2.write(data)

st.dataframe(Chamados_1746_04_01)

