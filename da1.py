# %%
import pandas as pd

# Wczytanie danych z pliku CSV
df = pd.read_csv(r'afteretl.csv')

# %%
df.head()

# %%
# Grupowanie danych i agregacja
df['count'] = 1
df = df.groupby(
    ["Year", "Quarter", "Month", "Day", "AREA NAME", "gender of criminal", "age of criminal"]
).agg({'count': 'sum'}).reset_index()

# Zmieniamy nazwę kolumny 'count' na 'IncidentCount'
df.rename(columns={'count': 'IncidentCount'}, inplace=True)

# %%
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

# Inicjalizacja aplikacji Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Definiowanie layoutu aplikacji Dash
app.layout = dbc.Container([
    html.H1(children='Dashboard Incydentów Kryminalnych'),
    
    dcc.Checklist(
        id='grouping-options',
        options=[
            {'label': 'Rok', 'value': 'Year'},
            {'label': 'Kwartał', 'value': 'Quarter'},
            {'label': 'Miesiąc', 'value': 'Month'},
            {'label': 'Dzień', 'value': 'Day'},
            {'label': 'Nazwa Obszaru', 'value': 'AREA NAME'},
            {'label': 'Płeć przestępcy', 'value': 'gender of criminal'},
            {'label': 'Wiek przestępcy', 'value': 'age of criminal'},
        ],
        value=['Year', 'Quarter', 'age of criminal'],
        inline=True
    ),


    
    dbc.Row([
        dbc.Col(dcc.Graph(id='sunburst-graph'), width=6),
        dbc.Col(dcc.Graph(id='bar-graph'), width=6),
    ]),
        dcc.Dropdown(
        id='area-dropdown',
        options=[{'label': area, 'value': area} for area in df['AREA NAME'].unique()],
        value=df['AREA NAME'].unique().tolist(),
        multi=True,
        placeholder='Wybierz nazwę obszaru'
    ),

    dbc.Row([
        dbc.Col(dcc.Graph(id='age-gender-bar-graph'), width=6),
        dbc.Col(html.Div(id='forecast-graph-container'), width=6)
    ]),

    
], fluid=True)

# Aktualizacja wykresu sunburst na podstawie wybranych opcji checkboxów
@app.callback(
    Output('sunburst-graph', 'figure'),
    Input('grouping-options', 'value')
)
def update_sunburst(selected_groupings):
    if not selected_groupings:
        selected_groupings = ["Year", "Month", "age of criminal"]
    
    fig_sunburst = px.sunburst(df, path=selected_groupings, values='IncidentCount')
    fig_sunburst.update_traces(textinfo='label+percent entry')
    return fig_sunburst

# Aktualizacja wykresu słupkowego dla lat i kwartałów
@app.callback(
    Output('bar-graph', 'figure'),
    Input('grouping-options', 'value')
)
def update_bar(selected_groupings):
    fig_bar = px.bar(df, x='Year', y='IncidentCount', color='Quarter', title='Liczba incydentów w poszczególnych latach i kwartałach', barmode='group')
    return fig_bar

# Aktualizacja wykresu słupkowego dla wieku przestępcy podzielonego na płeć i filtrowanego po nazwie obszaru
@app.callback(
    Output('age-gender-bar-graph', 'figure'),
    [Input('grouping-options', 'value'),
     Input('area-dropdown', 'value')]
)
def update_age_gender_bar(selected_groupings, selected_areas):
    filtered_df = df[df['AREA NAME'].isin(selected_areas)]
    fig_age_gender_bar = px.bar(filtered_df, x='age of criminal', y='IncidentCount', color='gender of criminal', 
                                title='Liczba incydentów według wieku i płci przestępcy', barmode='group')
    return fig_age_gender_bar

# Aktualizacja wykresu z HTML
@app.callback(
    Output('forecast-graph-container', 'children'),
    Input('grouping-options', 'value')
)
def update_forecast_graph(selected_groupings):
    with open('forecast_plot.html', 'r', encoding='utf-8') as f:
        plot_html = f.read()
    return html.Iframe(srcDoc=plot_html, style={"width": "100%", "height": "600px"})

# Uruchomienie serwera
if __name__ == '__main__':
    app.run_server(debug=True)
