from pyspark.sql import SparkSession, Row
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import pyspark.pandas as ps

try:
    # Tworzenie sesji Spark
    spark = SparkSession.builder \
        .appName("PySpark SQL Server Connection") \
        .config("spark.jars", "mssql-jdbc-12.6.1.jre8.jar") \
        .getOrCreate()

    # Parametry połączenia z bazą danych MSSQL
    server_name = "mssql-server"
    port = "1433"
    database_name = "BAZUNIA1"
    url = f"jdbc:sqlserver://{server_name}:{port};databaseName={database_name}"

    table_name = "BAZUNIA1"
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
 

except Exception as e:
    print("Wystąpił błąd podczas łączenia z bazą danych:", str(e))

