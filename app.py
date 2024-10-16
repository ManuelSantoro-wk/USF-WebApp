# type: ignore
import pandas as pd
from dash import Dash, dcc, html, dash_table, no_update
import plotly.express as px
from dash.exceptions import PreventUpdate
from reportlab.pdfgen import canvas
from dash.dependencies import Input, Output, State
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import webbrowser
from datetime import datetime
import io
import dash
import base64
import pdfkit
import os 
import csv
from flask import send_file
from itertools import combinations
from datetime import datetime

#equipa_options = [{'label': equipa, 'value': equipa} for equipa in df['Equipa Médica'].unique()]
equipos_medicos = ['PM', 'SM','MJG','PD', 'Não Aplicável - NA']
indicador_options = [{'label': indicador, 'value': indicador} for indicador in ['2013.008.01 FL',
    '2013.294.01 FL', '2017.330.01 FL', '2017.331.01 FL','2017.335.01 FL', '2013.020.01 FL', '2013.023.01 FL',
    '2013.036.01 FL', '2013.037.01 FL', '2013.039.01 FL', '2013.049.01 FL', '2013.261.01 FL', '2013.274.01 FL',
    '2013.275.01 FL','2015.314.01 FL','2015.315.01 FL','2017.380.01 FL', '2021.436.01 FL', '2021.437.01 FL',
    '2013.011.01 FL', '2013.034.01 FL', '2013.045.01 FL', '2013.046.01 FL', '2013.054.01 FL', '2013.063.01 FL',
    '2013.095.01 FL', '2013.098.01 FL', '2013.269.01 FL', '2013.295.01 FL', '2013.302.01 FL', '2015.308.01 FL',
    '2015.310.01 FL', '2015.311.01 FL', '2015.312.01 FL', '2017.384.01 FL', '2018.397.01 FL', '2018.404.01 FL',
    '2020.435.01 FL', '2018.409.01 FL']]

external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap"
]
csv_directory = 'Listas_Individuais'
csv_directory2 = 'Listas_Individuais/Listas'

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Utentes USF"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Utentes USF", className="header-title"
                ),
                html.P(
                    children=(
                        "Análise da lista de Utentes da USF Fénix de Aveiro"
                    ),
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            className="box",
            children=[
                html.A(
                    className="button",
                    href="#popup1",
                    children="Sobre Nós"
                )
            ]
        ),
        html.Div(
            children=[
                html.Div(
                    id="popup1",
                    className="overlay",
                    children=[
                        html.Div(
                            className="popup",
                            children=[
                                html.H2("Sobre Nós"),
                                html.A(className="close", href="#", children="×"),
                                html.Div(
                                    className="content",
                                    children=[
                                        html.B("Autor:"),
                                        html.Br(),
                                        "Esta aplicação foi desenvolvida por ",
                                        html.B("Manuel Graça"),
                                        ", sob orientação do ",
                                        html.B("Professor Doutor Bruno Gago"),
                                        ", e supervisão do ",
                                        html.B("Dr.Pedro Damião"),
                                        ".",
                                        html.Br(),
                                        "Faz parte do relatório de estágio do Mestrado em Bioinformática Clínica da Universidade de Aveiro.",
                                        html.Br(),
                                        html.B("Finalidade:"),
                                        html.Br(),
                                        "Apoiar a decisão dos profissionais da saúde a desenhar e implementar as priorizações dos utentes com base nos indicadores",
                                        html.Br(),
                                        html.B("Ferramentas Utilizadas:"),
                                        html.Br(),
                                        html.Div(
                                            className="image-container",
                                            children=[
                                                html.Img(src="assets/python.png"),
                                                html.Img(src="assets/plotly.png"),
                                                html.Img(src="assets/dash.png"),
                                            ],
                                        ),
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Equipa de Saúde:", className="menu-title"),
                        dcc.Checklist(
                            id="equipo-medico-checklist",
                            options=[{'label': equipo, 'value': equipo} for equipo in equipos_medicos],
                            value=[],
                            className="checklist equipo-medico-checklist",
                        ),
                        dcc.Upload(
                            id='upload-data',
                            children=html.Button('Carregar Arquivo CSV', className='reset-button'),
                            multiple=True
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.Div(children="Indicador:", className="menu-title"),
                                dcc.Checklist(
                                    id="indicador-checklist",
                                    options=indicador_options,
                                    value=[indicador_options[0]['value']],
                                    className="checklist indicador-checklist",
                                ),
                            ],
                            style={'width': '10%', 'display': 'inline-block', 'margin':'0%'},
                        ),
                    ],
                ),
                html.Button(id="ver-indicadores",children="Mostrar Mais", n_clicks=0,className="reset-button"),
                html.Button("Reset", id="reset-button", n_clicks=0, className="reset-button", style={"marginLeft": "20px"}),
                dcc.Location(id='url', refresh=True),
                html.Br(),
                html.Br(),
                html.Button("Interseção", id="intersecao-button", n_clicks=0, className="reset-button"),
                html.Button("Reunião", id="reuniao-button", n_clicks=0, className="reset-button", style={"marginLeft": "20px"}),
                html.Br(),
                html.A(html.Button("Exportar Tabela", id="download-csv", n_clicks=0, className="reset-button", style={"marginBottom": "100px"}), id="csv-link", download="table_data.csv", href=""),
                html.Label("Nome do Ficheiro:", className="menu-title", style={"marginBottom": "100px"}),
                    dcc.Input(
                        id="file-name-input",
                        type="text",
                        placeholder="Nome do Ficheiro",
                    ),
            ],
            className="left-column",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id='indicador-bar-chart',
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div([
                        dcc.Input(
                            id='numero_utente',
                            type='number',
                            placeholder='Número de Utente',
                            debounce=True,
                            style={'display': 'inline-block', 'width': '25%'}
                        ),
                    ]),
                html.Div(
                    children=dash_table.DataTable(
                        id="table-1",
                        style_table={'overflowX': 'auto','height': '250px'},
                    ),
                    className="card",
                ),
            ],
            className="right-column",
        ),
    ]
)

@app.callback(
    Output('indicador-bar-chart', 'figure'),
    Output('table-1', 'data'),
    [Input('indicador-checklist', 'value'),
     Input('equipo-medico-checklist', 'value'),  
     Input('upload-data', 'contents'),
     Input('numero_utente', 'value'),
     Input('intersecao-button', 'n_clicks'),
     Input('reuniao-button', 'n_clicks')],
    [State('upload-data', 'filename'),
     State('upload-data', 'last_modified')]
)
def update_output(selected_values, selected_equipos, list_of_contents, numero_utente, intersecao_click, reuniao_click, list_of_names, list_of_dates):
    ctx = dash.callback_context

    if not ctx.triggered or not selected_values and not list_of_contents and not selected_equipos:
        return {}, []

    df_uploaded = pd.DataFrame(columns=['Numero utente', 'Indicador'])

    # Carregar arquivos CSV enviados pelo usuário
    if list_of_contents:
        data_frames = []
        for contents, filename, last_modified in zip(list_of_contents, list_of_names, list_of_dates):
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            try:
                if '.csv' in filename:
                    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), header=None, names=['Numero utente'])
                    df['Indicador'] = os.path.splitext(filename)[0]
                    data_frames.append(df)
            except Exception as e:
                print(e)
                return {}, []

        if data_frames:
            df_uploaded = pd.concat(data_frames)
            df_uploaded = df_uploaded.drop_duplicates()

    if numero_utente:
        df_filtered = df_uploaded[df_uploaded['Numero utente'] == numero_utente]
    else:
        df_filtered = df_uploaded.copy()

    utentes_por_indicador = {}
    utentes_presentes = set()
    indicador_utentes = {indicador: set() for indicador in selected_values}
    equipo_utentes = {equipo: set() for equipo in selected_equipos}

    # Carregar listas de indicadores
    for indicador in selected_values:
        data_file = os.path.join(csv_directory, f'{indicador}.csv')
        if os.path.exists(data_file):
            df = pd.read_csv(data_file, header=None, names=['Numero utente'])
            if numero_utente:
                df = df[df['Numero utente'] == numero_utente]
            utentes_por_indicador[indicador] = df.shape[0]
            utentes_presentes.update(df['Numero utente'].tolist())
            indicador_utentes[indicador].update(df['Numero utente'].tolist())

    # Carregar listas das equipas médicas
    for equipo in selected_equipos:
        data_file = os.path.join(csv_directory, f'{equipo}.csv')
        if os.path.exists(data_file):
            df = pd.read_csv(data_file, header=None, names=['Numero utente'])
            if numero_utente:
                df = df[df['Numero utente'] == numero_utente]
            equipo_key = f'Equipa_{equipo}'
            utentes_por_indicador[equipo_key] = df.shape[0]
            utentes_presentes.update(df['Numero utente'].tolist())
            equipo_utentes[equipo].update(df['Numero utente'].tolist())

    if not df_uploaded.empty:
        for indicador in df_uploaded['Indicador'].unique():
            df_indicador = df_uploaded[df_uploaded['Indicador'] == indicador]
            if numero_utente:
                df_indicador = df_indicador[df['Numero utente'] == numero_utente]
            count = df_indicador['Numero utente'].nunique()
            utentes_por_indicador[indicador] = count
            utentes_presentes.update(df_indicador['Numero utente'].tolist())

    table_data = []
    if ctx.triggered[0]['prop_id'] == 'intersecao-button.n_clicks':
        # Interseção apenas entre listas selecionadas
        common_utentes = utentes_presentes
        if selected_values and df_uploaded.empty:
            # Intersecção apenas entre listas de indicadores
            common_utentes = set.intersection(*[indicador_utentes[indicador] for indicador in selected_values])
        elif not selected_values and not df_uploaded.empty:
            # Intersecção apenas entre uploads
            common_utentes = set.intersection(*[set(df_uploaded[df_uploaded['Indicador'] == indicador]['Numero utente']) for indicador in df_uploaded['Indicador'].unique()])
        else:
            # Intersecção entre listas de indicadores e uploads
            common_utentes = set.intersection(
                *[indicador_utentes[indicador] for indicador in selected_values],
                set(df_uploaded['Numero utente'])
            )
        if selected_values:
            common_utentes = set.intersection(*[indicador_utentes[indicador] for indicador in selected_values])
        if selected_equipos:
            common_utentes = set.intersection(common_utentes, *[equipo_utentes[equipo] for equipo in selected_equipos])
        if not df_uploaded.empty:
            common_utentes = set.intersection(common_utentes, set(df_uploaded['Numero utente']))

        if numero_utente:
            common_utentes = set.intersection(common_utentes, set(df_filtered['Numero utente']))
        
        for utente in common_utentes:
            row = {'Numero utente': utente}
            for indicador in selected_values:
                row[indicador] = 1 if utente in indicador_utentes[indicador] else 0
            for indicador in df_uploaded['Indicador'].unique():
                if indicador not in row:
                    row[indicador] = 1 if utente in df_uploaded[df_uploaded['Indicador'] == indicador]['Numero utente'].tolist() else 0
            for equipo in selected_equipos:
                equipo_key = f'Equipa_{equipo}'
                row[equipo_key] = 1 if utente in equipo_utentes[equipo] else 0
            table_data.append(row)
            
        # Calcular o número total de utentes comuns
        total_utentes_comuns = len(common_utentes)
        
        # Atualizar a altura de todas as barras para o número total de utentes comuns
        #utentes_por_indicador = {indicador: total_utentes_comuns for indicador in utentes_por_indicador}

    elif ctx.triggered[0]['prop_id'] == 'reuniao-button.n_clicks':
        # União das listas selecionadas
        all_utentes = set()
        for indicador in selected_values:
            all_utentes.update(indicador_utentes[indicador])
        for equipo in selected_equipos:
            all_utentes.update(equipo_utentes[equipo])
        if not df_uploaded.empty:
            all_utentes.update(df_uploaded['Numero utente'])
        
        if numero_utente:
            all_utentes = {utente for utente in all_utentes if utente == numero_utente}
        
        for utente in all_utentes:
            row = {'Numero utente': utente}
            for indicador in selected_values:
                row[indicador] = 1 if utente in indicador_utentes[indicador] else 0
            for indicador in df_uploaded['Indicador'].unique():
                if indicador not in row:
                    row[indicador] = 1 if utente in df_uploaded[df_uploaded['Indicador'] == indicador]['Numero utente'].tolist() else 0
            for equipo in selected_equipos:
                equipo_key = f'Equipa_{equipo}'
                row[equipo_key] = 1 if utente in equipo_utentes[equipo] else 0
            table_data.append(row)

        # Calcular o número total de utentes na reunião
        total_utentes_reuniao = len(all_utentes)
        
        # Atualizar a altura de todas as barras para o número total de utentes na reunião
        #utentes_por_indicador = {indicador: total_utentes_reuniao for indicador in utentes_por_indicador}

    else:
        for utente in utentes_presentes:
            row = {'Numero utente': utente}
            for indicador in selected_values:
                row[indicador] = 1 if utente in indicador_utentes[indicador] else 0
            for indicador in df_uploaded['Indicador'].unique():
                if indicador not in row:
                    row[indicador] = 1 if utente in df_uploaded[df_uploaded['Indicador'] == indicador]['Numero utente'].tolist() else 0
            for equipo in selected_equipos:
                equipo_key = f'Equipa_{equipo}'
                row[equipo_key] = 1 if utente in equipo_utentes[equipo] else 0
            table_data.append(row)

    if ctx.triggered[0]['prop_id'] == 'intersecao-button.n_clicks' or ctx.triggered[0]['prop_id'] == 'reuniao-button.n_clicks':
        if ctx.triggered[0]['prop_id'] == 'intersecao-button.n_clicks':
            bar_label = 'Interseção'
        else:
            bar_label = 'Reunião'
        fig = px.bar(x=list(utentes_por_indicador.keys()) + [bar_label], 
                    y=list(utentes_por_indicador.values()) + [total_utentes_comuns if ctx.triggered[0]['prop_id'] == 'intersecao-button.n_clicks' else total_utentes_reuniao],
                    labels={'x': 'Listas', 'y': 'Número de Utentes'},
                    title=f'Número de Utentes por Listas ({bar_label})')

        fig.update_layout(showlegend=False)
    else:
        fig = px.bar(x=list(utentes_por_indicador.keys()), y=list(utentes_por_indicador.values()),
                    labels={'x': 'Listas', 'y': 'Número de Utentes'},
                    title='Número de Utentes por Listas')

        fig.update_layout(showlegend=False)

    return fig, table_data

@app.callback(
    Output("csv-link", "href"),
    [Input("download-csv", "n_clicks")],
    [State("table-1", "data"),
     State("file-name-input", "value")]
)
def download_csv(n_clicks, table_data, file_name):
    if n_clicks:
        if not table_data:
            return ""
        
        # Extraer la columna de números de utentes
        numeros_utente = [row["Numero utente"] for row in table_data]
        
        # Crear un archivo CSV con el nombre especificado por el usuario
        csv_path = os.path.join(csv_directory2, f"{file_name}.csv")
        with open(csv_path, "w") as f:
            #f.write("Numero utente\n")
            for numero in numeros_utente:
               f.write(f"{numero}\n")
        

@app.callback(
    [Output('ver-indicadores', 'children'),
     Output('indicador-checklist', 'options')],
    [Input('ver-indicadores', 'n_clicks')],
    prevent_initial_call=False
)
def mostrar_mas_indicadores(n_clicks):
    if n_clicks % 2 == 1:
        options = indicador_options
        button_text = "Mostrar Menos"
    else:
        options = indicador_options[:6]
        button_text = "Mostrar Mais"

    return [button_text, options]


@app.callback(
    [Output('indicador-checklist', 'value'),
     Output('upload-data', 'contents'),
     Output('equipo-medico-checklist', 'value')],
    Input('reset-button', 'n_clicks'),
    prevent_initial_call=True
)
def reset_checklists(reset_clicks):
    if reset_clicks > 0:
        default_indicador_value = [indicador_options[0]['value']]
        return default_indicador_value, None, []
    raise dash.exceptions.PreventUpdate




if __name__ == '__main__':
    app.run_server(debug=True)