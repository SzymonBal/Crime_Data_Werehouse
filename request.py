from pyspark.sql import SparkSession

def load_data_from_mssql(server_name, table_name, database_name, username="sa", password="YourStrongPassword123", num_rows=5):
    try:
        # Tworzenie sesji Spark
        spark = SparkSession.builder \
            .appName("PySpark SQL Server Connection") \
            .config("spark.jars", "mssql-jdbc-12.6.1.jre8.jar") \
            .getOrCreate()

        # Parametry połączenia z bazą danych MSSQL
        port = "1433"
        url = f"jdbc:sqlserver://{server_name}:{port};databaseName={database_name}"

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

        print(f"Dane zostały pomyślnie wczytane z MSSQL. Wyświetlanie pierwszych {num_rows} wierszy:")
        df.show(num_rows)
        return df

    except Exception as e:
        print("Wystąpił błąd podczas łączenia z bazą danych:", str(e))
        return None

# Przykładowe użycie funkcji
server_name = "mssql-server"
table_name = "BAZUNIA1"
database_name = "BAZUNIA1"
num_rows = 10  # Określona liczba wierszy do wyświetlenia

#df = load_data_from_mssql(server_name, table_name, database_name, num_rows=num_rows)
