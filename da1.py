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

# Inicjalizacja aplikacji Dash
app = dash.Dash(__name__)

# Definiowanie layoutu aplikacji Dash
app.layout = html.Div(children=[
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
        value=['Year', 'Month', 'age of criminal'],
        inline=True
    ),

    dcc.Graph(
        id='sunburst-graph'
    ),

    dcc.Graph(
        id='bar-graph'
    ),
])

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

# Uruchomienie serwera
if __name__ == '__main__':
    app.run_server(debug=True)
