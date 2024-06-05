import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

# Load data from CSV file
df = pd.read_csv(r'afteretl.csv')

# Aggregate data and add a count column
df['count'] = 1
df = df.groupby(
    ['Year', 'Quarter', 'Time', 'Day of Week', 'Vict Sex', 'Vict Age', 'annual earnings', 'Vict Descent']
).agg({'count': 'sum'}).reset_index()

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Define the layout of the app
app.layout = dbc.Container([
    html.H1(children='Ilość popełnianych przestępstw w odniesieniu do danych o ofiarach w latach 2020-2023'),

    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='sex-dropdown',
            options=[{'label': sex, 'value': sex} for sex in df['Vict Sex'].unique()],
            value=df['Vict Sex'].unique().tolist(),
            multi=True,
            placeholder='Wybierz płeć ofiary',
            style={'background-color': '#343a40', 'color': '#ffffff', 'margin-bottom': '10px'}  # dark background color and margin
        ), width=6),
        dbc.Col(dcc.Dropdown(
            id='descent-dropdown',
            options=[{'label': descent, 'value': descent} for descent in df['Vict Descent'].unique()],
            value=df['Vict Descent'].unique().tolist(),
            multi=True,
            placeholder='Wybierz pochodzenie ofiary',
            style={'background-color': '#343a40', 'color': '#ffffff', 'margin-bottom': '10px'}  # dark background color and margin
        ), width=6),
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id='day-week-bar-graph'), width=6),
        dbc.Col(dcc.Graph(id='age-earnings-scatter-graph'), width=6),
    ]),



    dcc.Checklist(
        id='grouping-options',
        options=[
            {'label': 'Rok', 'value': 'Year'},
            {'label': 'Kwartał', 'value': 'Quarter'},
            {'label': 'Dzień tygodnia', 'value': 'Day of Week'},
            {'label': 'Płeć ofiary', 'value': 'Vict Sex'},
            {'label': 'Wiek ofiary', 'value': 'Vict Age'},
            {'label': 'Pochodzenie ofiary', 'value': 'Vict Descent'},
        ],
        value=['Year', 'Day of Week', 'Vict Sex'],
        inline=True,
        style={'margin-bottom': '10px'}
    ),
    dbc.Row([
        dbc.Col(dcc.Graph(id='sunburst-graph'), width=12),
    ]),
    
    dbc.Row([ 
        dbc.Col(html.Div(id='forecast-graph-container2'), width=4),
        dbc.Col(html.Div(id='forecast-graph-container3'), width=4),
        dbc.Col(html.Div(id='forecast-graph-container4'), width=4),
    ]),

    
], fluid=True)

@app.callback(
    Output('sunburst-graph', 'figure'),
    Input('grouping-options', 'value')
)
def update_sunburst(selected_groupings):
    if not selected_groupings:
        selected_groupings = ['Year', 'Day of Week', 'Vict Sex']
    else:
        selected_groupings = [col for col in selected_groupings if col in df.columns]  # Filter out columns not in DataFrame
    
    fig_sunburst = px.treemap(df, path=selected_groupings, values='count', template='plotly_dark')
    fig_sunburst.update_traces(textinfo='label+percent entry')
    return fig_sunburst

@app.callback(
    Output('day-week-bar-graph', 'figure'),
    [Input('sex-dropdown', 'value'),
     Input('descent-dropdown', 'value')]
)
def update_day_week_bar(selected_sex, selected_descent):
    filtered_df = df[df['Vict Sex'].isin(selected_sex) & df['Vict Descent'].isin(selected_descent)]
    fig = px.bar(filtered_df, x='Day of Week', y='count', color='Day of Week', 
                 title='Liczba incydentów w poszczególne dni tygodnia', 
                 template='plotly_dark')
    return fig

@app.callback(
    Output('age-earnings-scatter-graph', 'figure'),
    [Input('sex-dropdown', 'value'),
     Input('descent-dropdown', 'value')]
)
def update_age_earnings_scatter(selected_sex, selected_descent):
    filtered_df = df[df['Vict Sex'].isin(selected_sex) & df['Vict Descent'].isin(selected_descent)]
    fig = px.scatter(filtered_df, x='Vict Age', y='annual earnings', size='count', color='Vict Sex',
                     title='Wiek ofiary vs. roczne zarobki', 
                     template='plotly_dark')
    return fig

@app.callback(
    Output('annual-earnings-bar-graph', 'figure'),
    [Input('sex-dropdown', 'value'),
     Input('descent-dropdown', 'value')]
)
def update_annual_earnings_bar(selected_sex, selected_descent):
    filtered_df = df[df['Vict Sex'].isin(selected_sex) & df['Vict Descent'].isin(selected_descent)]
    fig = px.bar(filtered_df, x='annual earnings', y='count', color='annual earnings', 
                 title='Roczne zarobki ofiar', 
                 template='plotly_dark')
    return fig

@app.callback(
    Output('vict-sex-bar-graph', 'figure'),
    [Input('sex-dropdown', 'value'),
     Input('descent-dropdown', 'value')]
)
def update_vict_sex_bar(selected_sex, selected_descent):
    filtered_df = df[df['Vict Sex'].isin(selected_sex) & df['Vict Descent'].isin(selected_descent)]
    fig = px.bar(filtered_df, x='Vict Sex', y='count', color='Vict Sex', 
                 title='Płeć ofiar', 
                 template='plotly_dark')
    return fig



@app.callback(
    Output('forecast-graph-container2', 'children'),
    Input('grouping-options', 'value')
)
def update_forecast_graph(selected_groupings):
    with open('forecast_plot4_2.html', 'r', encoding='utf-8') as f:
        plot_html = f.read()
    return html.Iframe(srcDoc=plot_html, style={"width": "100%", "height": "600px"})
@app.callback(
    Output('forecast-graph-container3', 'children'),
    Input('grouping-options', 'value')
)
def update_forecast_graph(selected_groupings):
    with open('forecast_plot4_3.html', 'r', encoding='utf-8') as f:
        plot_html = f.read()
    return html.Iframe(srcDoc=plot_html, style={"width": "100%", "height": "600px"})
@app.callback(
    Output('forecast-graph-container4', 'children'),
    Input('grouping-options', 'value')
)
def update_forecast_graph(selected_groupings):
    with open('forecast_plot4_4.html', 'r', encoding='utf-8') as f:
        plot_html = f.read()
    return html.Iframe(srcDoc=plot_html, style={"width": "100%", "height": "600px"})
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
