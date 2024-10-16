'''
Criação de função calcular_risco, uma função de avaliação de risco que calcula um valor numérico com base em vários fatores,
como idade, situação familiar, escolaridade, hábitos de fumo e álcool, Índice de Massa Corporal (IMC),
antecedentes obstétricos e ginecológicos e condições de saúde atuais.
Fonte:MS: Manual Técnico Gestação de Alto Risco e Caderno de
Atenção Básica Nº 32 ‐ Atenção ao Pré Natal de Baixo Risco e Material Fundação SESP
'''


def calcular_risco(idade, situacao_familiar, escolaridade, fumador, alcool, imc, antecedentes_obgyn, patologias_riscoatual):
    risco = 0

    if idade < 15 or idade > 35:
        risco += 1

    if situacao_familiar == 'Instável' or situacao_familiar == 'NA':
        risco += 1

    if not escolaridade:
        risco += 1

    if fumador:
        risco += 1

    if alcool:
        risco += 1

    if imc < 18 or (imc > 25 and imc <= 30):
        risco += 1
    elif imc > 30:
        risco += 5

    if antecedentes_obgyn or antecedentes_obgyn == 'NA':
        risco += 10

    if patologias_riscoatual or patologias_riscoatual == 'NA':
        risco += 10

    return risco