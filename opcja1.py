from pyspark.sql import SparkSession
from pyspark.sql.functions import count
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

try:
    # Tworzenie sesji Spark
    spark = SparkSession.builder \
        .appName("PySpark SQL Server Connection") \
        .config("spark.jars", "mssql-jdbc-12.6.1.jre8.jar") \
        .getOrCreate()

    # Parametry połączenia z bazą danych MSSQL
    server_name = "mssql-server"
    port = "1433"
    database_name = "ETLKI"
    url = f"jdbc:sqlserver://{server_name}:{port};databaseName={database_name}"

    table_name = "ETLKI"
    username = "sa"
    password = "YourStrongPassword123"

    # Wczytanie danych z bazy danych MSSQL
    df = spark.read \
        .format("jdbc") \
        .option("url", url) \
        .option("dbtable", table_name) \
        .option("user", username) \
        .option("password", password) \
        .option("encrypt", "false") \
        .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
        .load()

    print("Dane zostały pomyślnie wczytane z MSSQL.")
    # Wyświetlenie pierwszych kilku wierszy DataFrame
    # df.show(5)

except Exception as e:
    print("Wystąpił błąd podczas łączenia z bazą danych:", str(e))

# Tworzenie zestawienia wielowymiarowego danych (kostki OLAP)
df_agg = df.groupby("Year", "Quarter", "Month", "Day", "AREA NAME", "gender of criminal", "age of criminal") \
           .agg(count("*").alias("IncidentCount")) \
           .toPandas()

# Inicjalizacja aplikacji Dash
app = dash.Dash(__name__)

# Layout aplikacji
app.layout = html.Div([
    dcc.Graph(id='sunburst-graph')
])

# Callback do aktualizacji sunburst graph
@app.callback(
    Output('sunburst-graph', 'figure'),
    [Input('sunburst-graph', 'hoverData')]
)
def update_sunburst_graph(hoverData):
    # Tworzenie wizualizacji sunburst
    fig = px.sunburst(df_agg, path=["Year", "Quarter", "Month", "Day", "AREA NAME", "gender of criminal", "age of criminal"], values="IncidentCount")
    fig.update_traces(textinfo='label+percent entry')
    return fig

# Uruchomienie aplikacji
if __name__ == '__main__':
    app.run_server(debug=True,port=8899)
