import random
from faker import Faker
import pandas as pd
import numpy as np
'''
Criação de dados simulados referentes a utentes que pertencem às equipas médicas da USF Fénix de Aveiro.
Criação de um conjunto de dados sintéticos com vários atributos relacionados à saúde para um número especificado de indivíduos (4000).
Os dados gerados incluem informações como género, idade, estado de fumador, consumo de álcool, condições médicas
(por exemplo, diabetes, hipertensão), estado de gravidez, situação familiar, educação, índice de massa corporal (IMC) e mais.
Criação de DataFrame a partir dos dados gerados e armazenamento num ficheiro CSV 'simulacao_utentes.csv'.
'''

fake = Faker(['pt_PT'])

def gerar_dados(num_entradas):
    data = []

    for _ in range(num_entradas):
        num_utente_sns = fake.random_int(min=100000000, max=999999999)
        
        genero = random.choice(['Masculino', 'Feminino'])
        
        if genero == 'Masculino':
            nome = fake.first_name_male() + ' ' + fake.last_name()
        else:
            nome = fake.first_name_female() + ' ' + fake.last_name()
        
        idade = max(5, min(90, np.random.poisson(40)))

        if idade < 15:
            fumador = False
        else:
            fumador = random.choice([True, False, 'NA'])
        
        if idade < 15 or idade > 50:
            gravida = False
        else:
            gravida = random.choice([True, False])

        if genero == 'Masculino':
            gravida = False
        
        situacao_familiar = random.choice([True, False, 'NA'])
        escolaridade = random.choice([True, False])
        
        # Calculando o mean para a média desejada de 25
        mean = np.log(25)

        # Definindo um sigma inicial para teste
        sigma = 0.1


        # Gerar amostras com a distribuição lognormal e aplicar as restrições
        imc = max(15, min(30, int(np.random.lognormal(mean, sigma))))
        #imc = max(15, min(30, int(random.gauss(25, 5))))

        alcool = random.choice([True, False, 'NA'])
        hipotenso = random.choice([True, False])
        diabetes = random.choice([True, False])
        doenca_cronica = random.choice([True, False])

        if genero == 'Masculino':
            antecedentes_obgyn = False
        else:
            antecedentes_obgyn = random.choice([True, False, 'NA'])

        if doenca_cronica:
            patologias_riscoatual = True
        else:
            patologias_riscoatual = random.choice([False, 'NA'])

        equipa = random.choice(['SM', 'PD', 'PM', 'MJG', 'Não Aplicável - NA'])

        data_ultima_consulta = fake.date_between(start_date='-365d', end_date='today')
    
        data.append([
            num_utente_sns, nome, genero, idade, hipotenso, fumador, alcool, diabetes,
            doenca_cronica, gravida, situacao_familiar, escolaridade, antecedentes_obgyn, imc, patologias_riscoatual, equipa, data_ultima_consulta
        ])

    return data


num_utentes = 6000


simulacao = gerar_dados(num_utentes)


colunas = [
    'Num Utente SNS', 'Nome', 'Género', 'Idade', 'Hipotenso', 'Fumador', 'Alcool', 'Diabetes',
    'Doença Crónica', 'Grávida', 'Situação Familiar', 'Escolaridade', 'Antecedentes OBGYN', 'IMC', 'Patologia de Risco Atual', 'Equipa Médica', 'Data Última Consulta'
]

df = pd.DataFrame(simulacao, columns=colunas)

df.to_csv('simulacao_utentes.csv', index=False, encoding='utf-8')
