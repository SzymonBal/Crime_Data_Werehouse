import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

# Load data from CSV file
df = pd.read_csv(r'afteretl.csv')

df['count'] = 1
df = df.groupby(
    ['Year', 'Quarter','Month','Day','Day of Week','education levels','drug substances','marital status of criminal ','previously punished']
).agg({'count': 'sum'}).reset_index()

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Define the layout of the app
app.layout = dbc.Container([
    html.H1(children='Ilość popełnianych przestępstw w odniesieniu do czasu, poziomu wykształcenia przestępcy, używek w latach 2020-2023'),

    dcc.Dropdown(
        id='education-dropdown',
        options=[{'label': level, 'value': level} for level in df['education levels'].unique()],
        value=df['education levels'].unique().tolist(),
        multi=True,
        placeholder='Wybierz poziom edukacji',
        style={'background-color': '#343a40', 'margin-bottom': '10px'}  # dark background color and margin
    ),

    dcc.Dropdown(
        id='drug-dropdown',
        options=[{'label': drug, 'value': drug} for drug in df['drug substances'].unique()],
        value=df['drug substances'].unique().tolist(),
        multi=True,
        placeholder='Wybierz substancję narkotykową',
        style={'background-color': '#343a40', 'margin-bottom': '10px'}  # dark background color and margin
    ),

    dbc.Row([
        dbc.Col(dcc.Graph(id='previously-punished-bar-graph'), width=4),
        dbc.Col(dcc.Graph(id='education-drug-pie-graph'), width=4),
        dbc.Col(dcc.Graph(id='marital-status-bar-graph'), width=4),
        
    ]),


    dcc.Checklist(
        id='grouping-options',
        options=[
            {'label': 'Rok', 'value': 'Year'},
            {'label': 'Kwartał', 'value': 'Quarter'},
            {'label': 'Miesiąc', 'value': 'Month'},
            {'label': 'Dzień tygodnia', 'value': 'Day of Week'},
            {'label': 'Poziom edukacji', 'value': 'education levels'},
            {'label': 'Stan cywilny', 'value': 'marital status of criminal '},
            {'label': 'Susbtancje odużające', 'value': 'drug substances'},
            {'label': 'Karany wcześniej', 'value': 'previously punished'},
        ],
        value= ['Year', 'Day of Week','education levels',],
        inline=True,
        style={'margin-bottom': '10px'} 
    ),

    dbc.Row([
        dbc.Col(dcc.Graph(id='sunburst-graph'), width=6,),
        dbc.Col(dcc.Graph(id='day-week-bar-graph'), width=6),
          
    ]),
    
    dbc.Row([ 
        dbc.Col(html.Div(id='forecast-graph-container1'), width=4),
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
        selected_groupings = ['Year', 'Day of Week','education levels',]
    else:
        selected_groupings = [col for col in selected_groupings if col in df.columns]  # Filter out columns not in DataFrame
    
    fig_sunburst = px.sunburst(df, path=selected_groupings, values='count',template='plotly_dark')
    fig_sunburst.update_traces(textinfo='label+percent entry')
    return fig_sunburst


# Callback to update the bar graph for days of the week
@app.callback(
    Output('day-week-bar-graph', 'figure'),
    [Input('education-dropdown', 'value'),
     Input('drug-dropdown', 'value')]
)
def update_day_week_bar(selected_education, selected_drugs):
    filtered_df = df[df['education levels'].isin(selected_education) & df['drug substances'].isin(selected_drugs)]
    fig = px.bar(filtered_df, x='Day of Week', y='count', color='Day of Week', 
                 title='Liczba incydentów w poszczególne dni tygodnia', 
                 template='plotly_dark')
    return fig

# Callback to update the pie chart for education levels and drug substances
@app.callback(
    Output('education-drug-pie-graph', 'figure'),
    [Input('education-dropdown', 'value'),
     Input('drug-dropdown', 'value')]
)
def update_education_drug_pie(selected_education, selected_drugs):
    filtered_df = df[df['education levels'].isin(selected_education) & df['drug substances'].isin(selected_drugs)]
    fig = px.pie(filtered_df, names='education levels', values='count', 
                 title='Proporcja poziomów edukacji', 
                 template='plotly_dark')
    return fig

# Callback to update the bar graph for marital status of criminals
@app.callback(
    Output('marital-status-bar-graph', 'figure'),
    [Input('education-dropdown', 'value'),
     Input('drug-dropdown', 'value')]
)
def update_marital_status_bar(selected_education, selected_drugs):
    filtered_df = df[df['education levels'].isin(selected_education) & df['drug substances'].isin(selected_drugs)]
    fig = px.bar(filtered_df, x='marital status of criminal ', y='count', color='marital status of criminal ', 
                 title='Stan cywilny przestępcy', 
                 template='plotly_dark')
    return fig

# Callback to update the bar graph for previously punished status
@app.callback(
    Output('previously-punished-bar-graph', 'figure'),
    [Input('education-dropdown', 'value'),
     Input('drug-dropdown', 'value')]
)
def update_previously_punished_bar(selected_education, selected_drugs):
    filtered_df = df[df['education levels'].isin(selected_education) & df['drug substances'].isin(selected_drugs)]
    fig = px.bar(filtered_df, x='previously punished', y='count', color='previously punished', 
                 title='Czy przestępca był wcześniej karany', 
                 template='plotly_dark')
    return fig

# Aktualizacja wykresu z HTML


@app.callback(
    Output('forecast-graph-container1', 'children'),
    Input('grouping-options', 'value')
)
def update_forecast_graph(selected_groupings):
    with open('forecast_plot3_1.html', 'r', encoding='utf-8') as f:
        plot_html = f.read()
    return html.Iframe(srcDoc=plot_html, style={"width": "100%", "height": "600px"})
@app.callback(
    Output('forecast-graph-container2', 'children'),
    Input('grouping-options', 'value')
)
def update_forecast_graph(selected_groupings):
    with open('forecast_plot3_2.html', 'r', encoding='utf-8') as f:
        plot_html = f.read()
    return html.Iframe(srcDoc=plot_html, style={"width": "100%", "height": "600px"})
@app.callback(
    Output('forecast-graph-container3', 'children'),
    Input('grouping-options', 'value')
)
def update_forecast_graph(selected_groupings):
    with open('forecast_plot3_3.html', 'r', encoding='utf-8') as f:
        plot_html = f.read()
    return html.Iframe(srcDoc=plot_html, style={"width": "100%", "height": "600px"})
@app.callback(
    Output('forecast-graph-container4', 'children'),
    Input('grouping-options', 'value')
)
def update_forecast_graph(selected_groupings):
    with open('forecast_plot3_4.html', 'r', encoding='utf-8') as f:
        plot_html = f.read()
    return html.Iframe(srcDoc=plot_html, style={"width": "100%", "height": "600px"})

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
