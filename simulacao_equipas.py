import random
from faker import Faker
from datetime import datetime, timedelta
import pandas as pd

'''
Criação de dados fictícios de consultas médicas.
Criação de uma lista de dados sobre o número de consultas por dia de cada equipa médica
(equipa médica, número de consultas, dia da consulta), conversão para um DataFrame e,
armazenamento dos dados num file CSV 'simulacao_consultas.csv'.
'''

fake = Faker(['pt_PT'])

def gerar_dados(num_entradas):
    data = []
    for _ in range(num_entradas):
        
        #Ficheiro Médico
        equipa = random.choice(['SM', 'PD', 'PM', 'MJG', 'Não Aplicável - NA'])

        n_consultas = random.randint(5,15)

        # Data de última consulta (nos últimos 365 dias)
        d_consultas = fake.date_between(start_date='-365d', end_date='today')
    
        # Adiciona os dados à lista
        data.append([
            equipa, n_consultas, d_consultas
        ])

    return data

# Define o número de utentes a serem gerados
num_consulta = 6000

# Gera dados fictícios
simulacao = gerar_dados(num_consulta)

# Converte a lista de dados em um DataFrame do pandas para facilitar a manipulação
colunas = ['Equipa Médica', 'Número de Consultas','Data Consulta']

df = pd.DataFrame(simulacao, columns=colunas)

df.to_csv('simulacao_consultas.csv', index=False)