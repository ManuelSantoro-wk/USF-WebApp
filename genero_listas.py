import pandas as pd
import os

df = pd.read_csv('simulacao_listas.csv')

output_dir = 'Listas_Individuais'
os.makedirs(output_dir, exist_ok=True)


for genre in df['Género'].unique():
    # Filtra pelo género
    df_genre = df[df['Género'] == genre]
    
    # Guarda o número de utente em CSV separados
    output_file = os.path.join(output_dir, f'{genre}.csv')
    df_genre['Num Utente SNS'].to_csv(output_file, index=False, header=False)

    print(f'Guardaram-se os numeros de utentes pelo genero {genre} na pasta {output_file}')
