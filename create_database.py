import pyodbc

# Parametry połączenia
server = 'localhost'
database = 'master'  # Połącz się z bazą master, aby móc utworzyć nową bazę danych
username = 'sa'
password = 'YourStrongPassword123'
driver = '{ODBC Driver 17 for SQL Server}'

# Tworzenie ciągu połączenia
conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Nawiązanie połączenia
conn = pyodbc.connect(conn_str)
conn.autocommit = True
# Utworzenie kursora
cursor = conn.cursor()

# Polecenie SQL CREATE DATABASE
create_db_query = "CREATE DATABASE ETL"

# Wykonanie polecenia
cursor.execute(create_db_query)

# Zatwierdzenie zmian
conn.commit()

# Zamykanie kursora i połączenia
cursor.close()
conn.close()

print("Baza danych NowaBazaDanych2 została utworzona.")