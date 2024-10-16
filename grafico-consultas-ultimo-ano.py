import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

'''
Análise e visualização de dados de um ficheiro CSV que contem informações sobre consultas médicas.
O script cria um gráfico de caixa com sobreposição de gráficos de linhas para cada equipa médica,
mostrando o número de consultas por semana.
'''

df = pd.read_csv("simulacao_consultas.csv")
df['Data Consulta'] = pd.to_datetime(df['Data Consulta'])
df = df.sort_values(by="Data Consulta")


df['Week'] = df['Data Consulta'].dt.strftime('%Y-%U')


grouped_df = df.groupby(['Week', 'Equipa Médica']).size().reset_index(name='Número de Consultas')

fig = px.box(df, x='Week', y='Número de Consultas', color='Equipa Médica',
              labels={'Número de Consultas': 'Número de Consultas por Semana'},
              title='Número de Consultas por Semana por Equipa Médica')

for team in grouped_df['Equipa Médica'].unique():
    team_data = grouped_df[grouped_df['Equipa Médica'] == team]
    line = go.Scatter(x=team_data['Week'], y=team_data['Número de Consultas'],
                      mode='lines+markers',
                      name=team)
    fig.add_trace(line)

fig.show()
