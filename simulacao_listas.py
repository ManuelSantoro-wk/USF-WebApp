from faker import Faker
import pandas as pd
import numpy as np

fake = Faker(['pt_PT'])
np.random.seed(42)

def gerar_dados(num_entradas):
    data = []

    for _ in range(num_entradas):
        num_utente_sns = fake.random_int(min=100000000, max=999999999)
        genero = np.random.choice(['Masculino', 'Feminino'])
        idade = max(0, min(90, np.random.poisson(40)))
        equipa = np.random.choice(['SM', 'PD', 'PM', 'MJG', 'Não Aplicável - NA'])
        data_ultima_consulta = fake.date_between(start_date='-365d', end_date='today')
        
        cronico = np.random.choice([0, 1])#ter doença crónica
        hipertenso = np.random.choice([0,1])#ser hipertenso
        pa=fake.random_int(min=90,max=150)
        cv=np.random.choice([0,1]) #ter risco de CV
        dm=np.random.choice([0,1])#ter DM
        grt=np.random.choice([0,1]) #ter registo de GRT
        hba1c=fake.random_int(min=0, max=10) #registo de última hba1c
        dpoc=np.random.choice([0,1]) #ter dpoc
        fev1=np.random.choice([0,1]) #ter FeV1 em 3 anos
        ulcera_pe=np.random.choice([0,1]) #ter avaliação de risco de ulcera no pé
        dm2=np.random.choice([0,1]) #ter dm2
        terapia_insul=np.random.choice([0,1]) #em terapia insulina
        terapia_metform=np.random.choice([0,1]) #em terapia metformina
        cldl=fake.random_int(min=10,max=250) #registo de C-LDL
        asma=np.random.choice([0,1]) #com asma
        bronq_cr=np.random.choice([0,1]) if cronico == 1 else 0 #com bronquite cronica
        diagn=np.random.choice([0,1]) #com diagnostico
        vigil_1a=np.random.choice([0,1]) #com vigilancia 1A

        #Gestão da Sáude
        gravida=np.random.choice([0,1]) if genero == "Feminino" and 14 <= idade <= 50 else 0 #estar gravida
        trim1=np.random.choice([0,1]) if gravida == 1 else 0 #gravida no 1ºtrimestre
        trim2=np.random.choice([0,1]) if gravida == 1 and trim1 == 0 else 0 #gravida no 2ºtrimestre
        trim3=1 if gravida == 1 and trim1 == 0 and trim2 == 0 else 0 #gravida no 3ºtrimestre
        vigil_1trim=np.random.choice([0,1]) if trim1 == 1 else 0 #com vigilancia 1ºtrim.
        obesidade=np.random.choice([0,1]) #com obesidade
        vigil_2a=np.random.choice([0,1]) #com vigilancia 2A
        canc_colo=np.random.choice([0,1]) if genero == "Feminino" else 0 #com rastreio do cancro colo útero
        cons_alcool=np.random.choice([0,1]) #com consumo de alcool
        cons_3A=np.random.choice([0,1]) #com consulta 3A
        cons_med_vig=np.random.choice([0,1]) #com consulta médica vigiada
        PNV=np.random.choice([0,1]) # com PNV
        PNV_ex=np.random.choice([0,1]) #  PNV em execução
        vac_tet=np.random.choice([0,1]) #  com vacina do tetano
        gravida_eco2t=np.random.choice([0,1]) if trim2 == 1 else 0 # grávidas no 2º trimestre com ecografia
        rg=np.random.choice([0,1]) #ter registo de gravidez
        fum=np.random.choice([0,1]) #ser fumador
        abs_tab=np.random.choice([0,1]) if fum == 0 else 0 #abstinencia tabagica de 12 meses
        int_breve=np.random.choice([0,1]) #int. breve
        int_mt_breve=np.random.choice([0,1]) #int. muito breve
        vac_gripe=np.random.choice([0,1]) #ter vacina gripe
        prescr=np.random.choice([0,1]) #ter prescrição...
        rastreio_cancro=np.random.choice([0,1]) #ter rastreio de cancro CR
        n_filhos=fake.random_int(min=0,max=10) if genero == "Feminino" and 30 <= idade <= 50 else 0 #número de filhos
        rp=np.random.choice([0,1]) if genero == "Feminino" and 30 <= idade <= 50 else 0  #ter registo de parto

        #Acesso
        indicador8 = np.random.choice([0, 1]) if genero == "Feminino" and 14 <= idade <= 50 else 0 #Taxa de utilização de consultas de PF (méd./enf.)
        indicador294 = np.random.choice([0, 1]) if idade >= 60 else 0 #Taxa domicílios enferm. p/ 1000 inscritos idosos
        indicador330 = np.random.choice([0, 1]) #Índice de utilização anual de consultas médicas
        indicador331 = np.random.choice([0, 1]) #Índice de utilização anual de consultas enferm.
        indicador335 = np.random.choice([0, 1]) if cronico == 1 else 0 #Prop. cons. ind. receit. c/ resposta 3 dias úteis
        
        #Gestão da Doença
        indicador20 = 1 if hipertenso == 1 and pa <= 150 and idade <= 65 else 0 #Proporção hipertensos < 65 A, com PA < 150/90
        indicador23 = 1 if hipertenso == 1 and cv == 1 else 0 #Proporção hipertensos com risco CV (3 A)
        indicador36 = 1 if dm == 1 and grt == 1 else 0 #Proporção utentes DM com registo de GRT
        indicador37 = 1 if dm == 1 and indicador331 == 1 else 0 #Proporção DM c/ cons. enf. vigil. DM último ano
        indicador39 = 1 if dm == 1 and hba1c <= 8 else 0 #Proporção DM c/ última HbA1c <= 8,0%
        indicador49 = 1 if dpoc == 1 and fev1 == 1 else 0 #Proporção utentes c/ DPOC, c/ FeV1 em 3 anos
        indicador261 = 1 if dm == 1 and ulcera_pe == 1 else 0 #Proporção utentes DM c/ aval. risco úlcera pé
        indicador274 = 1 if dm2 == 1 and terapia_insul == 1 else 0 #Propor. DM2 c/ indic. insul., em terap. adequada
        indicador275 = 1 if dm2 == 1 and terapia_metform == 1 else 0 #Proporção novos DM2 em terap. c/ metform. monot.
        indicador314 = 1 if dm == 1 and pa >= 140 else 0 #Proporção DM com PA >= 140/90 mmHg
        indicador315 = 1 if dm == 1 and cldl < 100 else 0 #Proporção DM com C-LDL < 100 mg/dl
        indicador380 = 1 if idade >= 18 and dpoc == 1 and asma == 1 and bronq_cr == 1 and diagn == 1 else 0 #Prop. adultos c/ asma/DPOC/bronq. cr., com diagn.
        indicador436 = 1 if dpoc == 1 and idade >= 40 and vigil_1a == 1 else 0 #Proporção DPOC >= 40A, c/ cons. vigil. DPOC 1A
        indicador437 = 1 if asma == 1 and idade >= 18 and vigil_1a == 1 else 0 #Proporção asma >= 18A, c/ cons. vigil. asma 1A

        #Gestão da Sáude
        indicador11 = 1 if trim1 == 1 and vigil_1trim == 1 else 0 #proporção de grávidas c/ cons. vigil 1º Trim
        indicador34 = 1 if obesidade == 1 and idade >= 14 and vigil_2a == 1 else 0 #Proporção obesidade >= 14A, c/ cons. vigil. obesid. 2A
        indicador45 = 1 if canc_colo == 1 and genero == "Feminino" and 25 <= idade <= 60 else 0 #Prop. mulheres 25-60 anos c/ rastr. c. colo út.
        indicador46 = 1 if 50 >= idade >=75 and rastreio_cancro == 1 else 0 #Proporção utentes [50; 75[A, c/ rastreio cancro CR
        indicador54 = 1 if cons_alcool == 1 and cons_3A == 1 else 0 #Proporção de utentes consum alcool, c/ cons. 3A
        indicador63 = 1 if 0 <= idade <= 7 and cons_med_vig == 1 and PNV == 1 else 0 #Proporção crianças 7A, c/ cons. méd. vig. e  com PNV
        indicador95 = 1 if 8 <= idade <= 14 and PNV == 1 or PNV_ex == 1 else 0 #Proporção jovens 14A, com PNV cumprido ou execução
        indicador98 = 1 if 25 <= idade and vac_tet == 1 else 0 #Proporção utentes >= 25 A, c/ vacina tetano
        indicador269 = np.random.choice([0, 1]) if idade == 2 else 0 #Índice de acompanham. adequado s. infantil 2º ano
        indicador295 = 1 if n_filhos >= 5 and rp == 1 and indicador331 == 1 else 0 #Propor. puérp. 5+ cons. vig. enf. grav. e c/ RP
        indicador302 = np.random.choice([0, 1]) if idade == 1 else 0 #Índice de acompanham. adequado s. infantil 1º ano
        indicador308 = 1 if gravida_eco2t == 1 else 0 #Proporção grávidas com ecografia 2º trimestre
        indicador310 = np.random.choice([0, 1]) if trim1 == 1 else 0 #Índice realização exames laborat. 1º trim. grav.
        indicador311 = np.random.choice([0, 1]) if trim2 == 1 else 0 #Índice realização exames laborat. 2º trim. grav.
        indicador312 = np.random.choice([0, 1]) if trim3 == 1 else 0 #Índice realização exames laborat. 3º trim. grav.
        indicador384 = 1 if idade <= 1 and rg == 1 else 0 #Propor. RN cuja mãe tem registo de gravidez
        indicador397 = 1 if fum == 1 and int_breve == 1 or int_mt_breve == 1 else 0 #Prop. fumador c/ int. breve ou muito breve 1 ano
        indicador404 = 1 if abs_tab == 1 else 0 #Incidência anual de pessoas em abstin. tabág. 12M
        indicador435 = 1 if vac_gripe == 1 else 0 #Proporção utentes com vacina gripe gratuita SNS
        indicador409 = 1 if prescr == 0 else 0 #Prop ute sem prescr prolo ansio/seda/hipn (ajust) 
        
        data.append([
            num_utente_sns, genero, idade, equipa, data_ultima_consulta, indicador8, indicador294,
            indicador330, indicador331, indicador335, indicador20, indicador23, indicador36, indicador37,
            indicador39, indicador49, indicador261, indicador274, indicador275, indicador314, indicador315,
            indicador380, indicador436, indicador437, indicador11, indicador34, indicador45, indicador46, indicador54, 
            indicador63, indicador95, indicador98, indicador269, indicador295, indicador302, indicador308, indicador310, 
            indicador311, indicador312, indicador384, indicador397, indicador404, indicador435, indicador409
        ])

    return data

num_utentes = 6000
simulacao = gerar_dados(num_utentes)

colunas = [
    'Num Utente SNS', 'Género', 'Idade', 'Equipa Médica', 'Data Última Consulta', '2013.008.01 FL',
    '2013.294.01 FL', '2017.330.01 FL', '2017.331.01 FL','2017.335.01 FL', '2013.020.01 FL', '2013.023.01 FL',
    '2013.036.01 FL', '2013.037.01 FL', '2013.039.01 FL', '2013.049.01 FL', '2013.261.01 FL', '2013.274.01 FL',
    '2013.275.01 FL','2015.314.01 FL','2015.315.01 FL','2017.380.01 FL', '2021.436.01 FL', '2021.437.01 FL',
    '2013.011.01 FL', '2013.034.01 FL', '2013.045.01 FL', '2013.046.01 FL', '2013.054.01 FL', '2013.063.01 FL',
    '2013.095.01 FL', '2013.098.01 FL', '2013.269.01 FL', '2013.295.01 FL', '2013.302.01 FL', '2015.308.01 FL',
    '2015.310.01 FL', '2015.311.01 FL', '2015.312.01 FL', '2017.384.01 FL', '2018.397.01 FL', '2018.404.01 FL',
    '2020.435.01 FL', '2018.409.01 FL'
]

df = pd.DataFrame(simulacao, columns=colunas)

df.to_csv('simulacao_listas.csv', index=False,  encoding='utf-8')