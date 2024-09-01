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
#aba1.dataframe(Chamados_1746_04_01)

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

subprefeitura_chamados = df_uniao_chamados_bairros['subprefeitura'].value_counts() #.head(10)
subprefeitura_chamados = pd.DataFrame({'subprefeitura':subprefeitura_chamados.index, 'contagem':subprefeitura_chamados.values})
#subprefeitura_chamados.head()

fig_subprefeitura = criar_grafico_barras(subprefeitura_chamados,
                                x='contagem', 
                                y='subprefeitura', 
                                top_n=10, 
                                orientation='h', 
                                titulo='Top 10 Tipos de Subprefeitura',
                                label_x='Quantidade de Ocorrências',
                                label_y='', 
                                paleta=px.colors.qualitative.Pastel2)

fig_subprefeitura.update_layout(yaxis={'categoryorder': 'total ascending'})

# Exibindo o gráfico de barras na aba1
aba1.subheader("Chamados - Gráfico de Subprefeitura")
aba1.plotly_chart(fig_subprefeitura)

chamados_por_subprefeitura = df_uniao_chamados_bairros.groupby('subprefeitura')['id_chamado'].count()
subprefeitura_max = chamados_por_subprefeitura.idxmax()
df_chamados_subprefeitura_max = df_uniao_chamados_bairros[df_uniao_chamados_bairros['subprefeitura'] == subprefeitura_max]
df_tipos_correspondentes = df_chamados_subprefeitura_max.groupby('tipo')['id_chamado'].count().reset_index()
df_tipos_correspondentes.columns = ['tipo', 'contagem']
df_tipos_correspondentes = df_tipos_correspondentes.sort_values(by='contagem', ascending=False)

fig_subprefeitura_ind = criar_grafico_barras(df_tipos_correspondentes,
                                x='contagem', 
                                y='tipo', 
                                top_n=10, 
                                orientation='h', 
                                titulo='Tipos predominantes na Subprefeitura Zona Norte',
                                label_x='Quantidade de Ocorrências',
                                label_y='', 
                                paleta=px.colors.qualitative.Pastel2)

fig_subprefeitura_ind .update_layout(yaxis={'categoryorder': 'total ascending'})

# Exibindo o gráfico de barras na aba1
aba1.subheader("Chamados - Gráfico de Subprefeitura")
aba1.plotly_chart(fig_subprefeitura_ind)

fig_mapa_sub = px.scatter_mapbox(df_uniao_chamados_bairros,
                            lat='latitude',
                            lon='longitude',
                            color='subprefeitura',
                            hover_name='nome',
                            zoom=10,
                            mapbox_style="carto-positron",
                            center=dict(lat=-22.9068467, lon=-43.1728965),
                            title='Pontos de Chamados por Bairro')

#fig_mapa_sub

aba1.subheader("Chamados - distribuição de chamados por subprefeituras")
aba1.plotly_chart(fig_mapa_sub)
#------------------------------------------------------
# Conteúdo da aba1 - exibição do gráfico
#aba1.subheader("Chamados - Gráfico de Linha")
#aba1.line_chart(Chamados_1746_04_01)


#Parte 2


#tab2.write(data)
#st.dataframe(Chamados_1746_04_01)

df_filtrado1 = pd.read_csv('./Dados_1/chamados_parte2.csv', delimiter=',')
df2_selecionado = df_filtrado1[['id_chamado', 'data_inicio','id_bairro','categoria','tipo',
                          'subtipo','status','longitude','latitude','reclamacoes']] #,'geometry'
df3 = pd.read_csv('./Dados_1/hoteleira_ocupacao.csv', delimiter=',')
df_uniao_chamados_bairros_PS = pd.merge(df2_selecionado, df_selecionado_bairros, on='id_bairro', how='left')

aba2.metric('Quantidade de Chamados', df_uniao_chamados_bairros_PS.shape[0])
aba2.subheader("teste") 

#grafico 1
df_chamados = pd.DataFrame(df_filtrado1)
df_categorias = pd.DataFrame(df3)

# Convertendo para datetime
df_chamados['data_inicio'] = pd.to_datetime(df_chamados['data_inicio'])
df_categorias['data_inicial'] = pd.to_datetime(df_categorias['data_inicial'])
df_categorias['data_final'] = pd.to_datetime(df_categorias['data_final'])

# Função para verificar se a data de abertura está dentro do intervalo
def verifica_correspondencia(data_inicio, data_inicial, data_final):
    return (data_inicio >= data_inicial) & (data_inicio <= data_final)

# Iterando sobre os chamados e verificando se correspondem a alguma categoria
chamados_correspondentes = []
for _, chamado in df_chamados.iterrows():
    for _, categoria in df_categorias.iterrows():
        if verifica_correspondencia(chamado['data_inicio'], categoria['data_inicial'], categoria['data_final']):
            chamados_correspondentes.append((chamado['id_chamado'], categoria['evento'], chamado['data_inicio']))
            break

df_correspondencias = pd.DataFrame(chamados_correspondentes, columns=['id_chamado', 'evento', 'data_inicio'])

df_correspondencias['numero_aparicoes'] = df_correspondencias.groupby(['id_chamado', 'evento'])['data_inicio'].transform('count')


contagem_categorias = df_correspondencias['evento'].value_counts().reset_index()
contagem_categorias.columns = ['evento', 'numero_aparicoes']

fig_tipo_2 = px.bar(
    contagem_categorias.head(10),
    x='evento', 
    y='numero_aparicoes',  # Inverter a ordem de x e y
    orientation='v',  # Mudar para vertical
    labels={'numero_aparicoes': 'Quantidade', 'evento': ''}, 
    title='Top 10 Tipos de Ocorrências',
    color_discrete_sequence=px.colors.qualitative.Pastel2  # Escolha da paleta de cores
)

# Ordenar o eixo x (tipos) do maior para o menor com base na contagem
fig_tipo_2.update_layout(xaxis={'categoryorder': 'total descending'})

# Exibindo o gráfico de barras na aba1
aba2.subheader("Chamados - Gráfico de bairros")
aba2.plotly_chart(fig_tipo_2)

# Mostrar o gráfico
#fig_tipo.show()

#Grafico de linhas
df_uniao_chamados_bairros_PS['data_inicio'] = pd.to_datetime(df_uniao_chamados_bairros_PS['data_inicio'])

# Agrupar o número de chamados por data
df_tendencia = df_uniao_chamados_bairros_PS.groupby(df_uniao_chamados_bairros_PS['data_inicio'].dt.date).size().reset_index(name='id_chamado')


fig = px.line(df_tendencia,
                  x='data_inicio',
                  y='id_chamado',
                  title='Tendência de Chamados ao Longo do Tempo',
                  color_discrete_sequence=px.colors.qualitative.Pastel2)

fig.update_xaxes(title_text='Data')
fig.update_yaxes(title_text='Número de Chamados')

aba2.plotly_chart(fig)
#st.plotly_chart(fig)

df_final = pd.merge(df_correspondencias, df_uniao_chamados_bairros_PS, on='id_chamado', how='left')
fig_m1 = px.scatter_mapbox(df_final,
                            lat='latitude',
                            lon='longitude',
                            color='evento',
                            hover_name='nome',
                            zoom=10,
                            mapbox_style="carto-positron",
                            center=dict(lat=-22.9068467, lon=-43.1728965),
                            title='Pontos de Chamados por evento')

#fig_m1
aba2.plotly_chart(fig_m1)

#Parte 3

df_public_holidays = pd.read_csv('./Dados_1/feriados_ano_pt.csv', delimiter=',')
daily_dataframe = pd.read_csv('./Dados_1/clima_temperatura.csv', delimiter=',')
df= pd.read_csv('./Dados_1/classi_tempo_pt.csv', delimiter=',')

aba3.metric('Quantidade de Feriados', df_public_holidays.shape[0])
aba3.subheader("A tab with the data") 
aba3.dataframe(df_public_holidays) 

df_public_holidays['Weekday or Weekend'] = df_public_holidays['Day of Week'].apply(lambda x: 'Semana' if x in ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira'] else 'Fim de Semana')
df_count = df_public_holidays['Weekday or Weekend'].value_counts().reset_index()
df_count.columns = ['Weekday or Weekend', 'Total Ocorrências']

fig_dias_semna = px.bar(
    df_count.head(2),
    x='Weekday or Weekend',
    y='Total Ocorrências',  # Inverter a ordem de x e y
    orientation='v',  # Mudar para vertical
    labels={'Total Ocorrências': 'Quantidade', 'Weekday or Weekend': ''},
    title='Média geral por evento e outro ',
    color_discrete_sequence=px.colors.qualitative.Pastel2  # Escolha da paleta de cores
)

# Ordenar o eixo x (tipos) do maior para o menor com base na contagem
fig_dias_semna.update_layout(xaxis={'categoryorder': 'total descending'})
aba3.plotly_chart(fig_dias_semna)



daily_dataframe['date'] = pd.to_datetime(daily_dataframe['date'])
daily_dataframe['year_month'] = daily_dataframe['date'].dt.to_period('M')
monthly_avg_temp = daily_dataframe.groupby('year_month')['temperature_2m_mean'].mean().reset_index()
monthly_avg_temp.columns = ['Year-Month', 'Average Temperature']


monthly_avg_temp['Average Temperature'] = monthly_avg_temp['Average Temperature'].round(2)
monthly_avg_temp['Month Name'] = monthly_avg_temp['Year-Month'].dt.strftime('%B')

# Criando o gráfico de linha
fig_mes_temp = px.line(
    monthly_avg_temp,
    x='Month Name',
    y='Average Temperature',
    title='Temperatura Média Mensal no Rio de Janeiro de 01/01/2024 a 01/08/2024',
    labels={'Month Name': 'Mês', 'Average Temperature': 'Temperatura Média (°C)'},
    markers=True,
    color_discrete_sequence=px.colors.qualitative.Pastel2
)

# Adicionando layout ao gráfico
fig_mes_temp.update_layout(
    xaxis=dict(
        tickmode='linear',
    ),
    yaxis=dict(
        title='Temperatura Média (°C)'
    )
)

aba3.plotly_chart(fig_mes_temp)
# Exibindo o gráfico
#fig.show()

df_merged = pd.merge(daily_dataframe, df, left_on='weather_code', right_on='cod', how='left')
df_merged = df_merged.drop(columns=['cod'])

df_merged['date'] = pd.to_datetime(df_merged['date'])
df_merged['date'] = df_merged['date'].dt.date

df_public_holidays['Date'] = pd.to_datetime(df_public_holidays['Date'])
df_merged['date'] = pd.to_datetime(df_merged['date'])

start_date = '2024-01-01'
end_date = '2024-08-01'


df_public_holidays_filtered = df_public_holidays[(df_public_holidays['Date'] >= start_date) & (df_public_holidays['Date'] <= end_date)]
df_merged_feriado = pd.merge(df_public_holidays_filtered, df_merged, left_on='Date', right_on='date', how='left')
df_merged_feriado = df_merged_feriado[['Date', 'Name', 'temperature_2m_mean', 'day_description']]

df_merged_feriado['temperature_2m_mean'] = df_merged_feriado['temperature_2m_mean'].round(2)

#df_merged_feriado

aba3.subheader("A tab with the data") 
aba3.dataframe(df_merged_feriado) 