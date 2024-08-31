import streamlit as st
#import requests
import pandas as pd
import plotly.express as px


st.title("Título aqui") 

## Visualização no streamlit
aba1, aba2, aba3 = st.tabs(['Chamados', 'Chamados por evento','Sobre o clima'])

#PARTE 1
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

#função
def criar_grafico_barras(df, x='x', y='y', 
                         top_n=10, orientation='h',
                         titulo='Top Ocorrências',
                         label_x='Quantidade', 
                         label_y='', 
                         paleta=px.colors.qualitative.Pastel2):

    # Selecionar as primeiras top_n linhas
    df_top = df.head(top_n)
    
    # Criar o gráfico de barras
    fig = px.bar(
        df_top,
        x=x,  # Ajuste de acordo com a orientação
        y=y,
        orientation=orientation,
        labels={x: label_x, y: label_y},
        title=titulo,
        color_discrete_sequence=paleta
    )
    
    #labels={x: label_x, y: label_y}, labels={x: 'Quantidade', y: ''}, 
    #fig_tipo.update_layout(yaxis={'categoryorder': 'total ascending'})

    return fig


# Exemplo de uso da função
fig_tipo = criar_grafico_barras(df_ocorrencias_por_tipo,
                                x='contagem', 
                                y='tipo', 
                                top_n=10, 
                                orientation='h', 
                                titulo='Top 10 Tipos de Ocorrências',
                                label_x='Quantidade de Ocorrências',
                                label_y='', 
                                paleta=px.colors.qualitative.Pastel2)

fig_tipo.update_layout(yaxis={'categoryorder': 'total ascending'})

# Exibindo o gráfico de barras na aba1
aba1.subheader("Chamados - gráfico dos tipos")
aba1.plotly_chart(fig_tipo)

bairros_mais_chamados = df_uniao_chamados_bairros['nome'].value_counts()#.head(10)
bairros_mais_chamados_df = pd.DataFrame({'nome':bairros_mais_chamados.index, 'contagem':bairros_mais_chamados.values})
bairros_mais_chamados_df.head()



fig_bairros = criar_grafico_barras(bairros_mais_chamados_df,
                                x='contagem', 
                                y='nome', 
                                top_n=10, 
                                orientation='h', 
                                titulo='Top 10 Tipos de bairros',
                                label_x='Quantidade de Ocorrências',
                                label_y='', 
                                paleta=px.colors.qualitative.Pastel2)

fig_bairros.update_layout(yaxis={'categoryorder': 'total ascending'})

# Exibindo o gráfico de barras na aba1
aba1.subheader("Chamados - Gráfico de bairros")
aba1.plotly_chart(fig_bairros)

#------------------------------------------------------
# Conteúdo da aba1 - exibição do gráfico
aba1.subheader("Chamados - Gráfico de Linha")
aba1.line_chart(Chamados_1746_04_01)


#Parte 2

aba2.subheader("A tab with the data") 
#tab2.write(data)
#st.dataframe(Chamados_1746_04_01)

#Parte 3
aba3.subheader("A tab with the data") 