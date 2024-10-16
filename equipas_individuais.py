import pandas as pd
import os

df = pd.read_csv('simulacao_listas.csv')

output_dir = 'Listas_Individuais'
os.makedirs(output_dir, exist_ok=True)

# Iterar sobre cada equipo médico único
for equipe in df['Equipa Médica'].unique():
    # Filtrar el DataFrame por equipo médico
    df_equipe = df[df['Equipa Médica'] == equipe]
    
    # Guardar solo los números de usuarios en un archivo CSV separado
    output_file = os.path.join(output_dir, f'{equipe}.csv')
    df_equipe['Num Utente SNS'].to_csv(output_file, index=False, header=False)

    print(f'Se han guardado los números de utentes para el equipo {equipe} en {output_file}')
