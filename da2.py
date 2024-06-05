import pandas as pd

# Wczytanie danych z pliku CSV
df = pd.read_csv(r'afteretl.csv')

# Wyświetlenie nazw kolumn, aby sprawdzić poprawność nazw
print(df.columns)

# Dodanie kolumny 'count' i agregacja danych
df['count'] = 1
df = df.groupby(
    ["Year", "Quarter", "Month", "Day", "AREA NAME", "gender of criminal", "age of criminal", 'country of criminal']
).agg({'kill count': 'sum'}).reset_index()
# Aggregate data and add a count column

# Zmieniamy nazwę kolumny 'kill count' na 'KillCount'
df.rename(columns={'kill count': 'KillCount'}, inplace=True)

import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

# Inicjalizacja aplikacji Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Definiowanie layoutu aplikacji Dash
app.layout = dbc.Container([
    html.H1(children='Dashboard Incydentów Kryminalnych'),

    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in df['country of criminal'].unique()],
        value=df['country of criminal'].unique().tolist(),
        multi=True,
        placeholder='Wybierz kraj przestępcy',
    ),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='age-gender-pie-graph'), width=6),
        dbc.Col(dcc.Graph(id='scatter-graph'), width=6),
    ]),
    
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
            {'label': 'Kraj przestępcy', 'value': 'country of criminal'},
        ],
        value=['Year', 'Quarter', 'gender of criminal'],
        inline=True
    ),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='sunburst-graph'), width=12),
        
    ]),
    dbc.Row([
        dbc.Col(html.Div(id='forecast-graph-container2'), width=4),
        dbc.Col(html.Div(id='forecast-graph-container3'), width=4),
        dbc.Col(html.Div(id='forecast-graph-container4'), width=4),
    ]),
    '''dbc.Row([
        dbc.Col(html.Div(id='forecast-graph-container1'), width=6),
        dbc.Col(html.Div(id='forecast-graph-container2'), width=6),
        ]),'''
    
    
], fluid=True)

# Aktualizacja wykresu sunburst na podstawie wybranych opcji checkboxów
@app.callback(
    Output('sunburst-graph', 'figure'),
    Input('grouping-options', 'value')
)
def update_sunburst(selected_groupings):
    if not selected_groupings:
        selected_groupings = ["Year", "Month", 'gender of criminal']
    
    fig_sunburst = px.treemap(df, path=selected_groupings, values='KillCount')
    fig_sunburst.update_traces(textinfo='label+percent entry')
    return fig_sunburst

# Aktualizacja wykresu rozproszenia dla wieku i płci przestępcy
@app.callback(
    Output('scatter-graph', 'figure'),
    Input('grouping-options', 'value')
)
def update_scatter(selected_groupings):
    fig_scatter = px.scatter(df, x='age of criminal', y='KillCount', color='gender of criminal', 
                             title='Zależność między wiekiem przestępcy a liczbą zabójstw',
                             labels={'age of criminal': 'Wiek przestępcy', 'KillCount': 'Liczba zabójstw'},
                             template='plotly_white',  # Użycie jasnego tła
                             opacity=0.7,  # Przezroczystość punktów
                             size='KillCount',  # Rozmiar punktów na podstawie liczby zabójstw
                             hover_data={'Year': True, 'Quarter': True, 'Month': True, 'Day': True}  # Dodatkowe dane w dymkach
                            )
    fig_scatter.update_layout(
        xaxis_title='Wiek przestępcy',
        yaxis_title='Liczba zabójstw',
        title={'x':0.5, 'xanchor': 'center'}  # Wyśrodkowanie tytułu
    )
    fig_scatter.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))  # Dodanie obramowania do punktów
    return fig_scatter

# Aktualizacja wykresu kołowego dla wieku i płci przestępcy z przypisaniem kolorków
@app.callback(
    Output('age-gender-pie-graph', 'figure'),
    [Input('grouping-options', 'value'),
     Input('country-dropdown', 'value')]
)
def update_age_gender_pie(selected_groupings, selected_countries):
    filtered_df = df[df['country of criminal'].isin(selected_countries)]
    fig_age_gender_pie = px.pie(filtered_df, names='age of criminal', values='KillCount', 
                                title='Proporcja zabójstw według wieku i płci przestępcy',
                                color_discrete_map={'18-35': 'blue', '35-60': 'red', 'Other': 'green'})
    return fig_age_gender_pie

# Aktualizacja wykresu z HTML
@app.callback(
    Output('forecast-graph-container', 'children'),
    Input('grouping-options', 'value')
)
def update_forecast_graph(selected_groupings):
    with open('forecast_plot.html', 'r', encoding='utf-8') as f:
        plot_html = f.read()
    return html.Iframe(srcDoc=plot_html, style={"width": "100%", "height": "600px"})



# Aktualizacja wykresu z HTML

@app.callback(
    Output('forecast-graph-container1', 'children'),
    Input('grouping-options', 'value')
)
def update_forecast_graph(selected_groupings):
    with open('forecast_plot2_1.html', 'r', encoding='utf-8') as f:
        plot_html = f.read()
    return html.Iframe(srcDoc=plot_html, style={"width": "100%", "height": "600px"})
@app.callback(
    Output('forecast-graph-container2', 'children'),
    Input('grouping-options', 'value')
)
def update_forecast_graph(selected_groupings):
    with open('forecast_plot2_2.html', 'r', encoding='utf-8') as f:
        plot_html = f.read()
    return html.Iframe(srcDoc=plot_html, style={"width": "100%", "height": "600px"})
@app.callback(
    Output('forecast-graph-container3', 'children'),
    Input('grouping-options', 'value')
)
def update_forecast_graph(selected_groupings):
    with open('forecast_plot2_3.html', 'r', encoding='utf-8') as f:
        plot_html = f.read()
    return html.Iframe(srcDoc=plot_html, style={"width": "100%", "height": "600px"})
@app.callback(
    Output('forecast-graph-container4', 'children'),
    Input('grouping-options', 'value')
)
def update_forecast_graph(selected_groupings):
    with open('forecast_plot2_4.html', 'r', encoding='utf-8') as f:
        plot_html = f.read()
    return html.Iframe(srcDoc=plot_html, style={"width": "100%", "height": "600px"})


# Uruchomienie serwera
if __name__ == '__main__':
    app.run_server(debug=True)
