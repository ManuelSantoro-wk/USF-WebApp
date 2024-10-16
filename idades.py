import pandas as pd
import os

# Leitura do arquivo CSV
df = pd.read_csv('simulacao_listas.csv')

# Diretório de saída
output_dir = 'Listas_Individuais'
os.makedirs(output_dir, exist_ok=True)

# Gerar arquivos CSV para cada faixa etária de 5 anos
for start_age in range(0, 101, 5):
    end_age = start_age + 4
    
    # Filtra pela faixa etária
    df_age_range = df[(df['Idade'] >= start_age) & (df['Idade'] <= end_age)]
    
    # Guarda o número de utente em CSV separados
    output_file = os.path.join(output_dir, f'{start_age}-{end_age}.csv')
    df_age_range['Num Utente SNS'].to_csv(output_file, index=False, header=False)

    print(f'Guardaram-se os numeros de utentes pela faixa etária {start_age}-{end_age} na pasta {output_file}')