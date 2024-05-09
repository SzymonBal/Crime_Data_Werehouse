'''import pyodbc

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

print("Baza danych Clean_Database_1 została utworzona.")'''

import pyodbc

def create_database(database_name, server='localhost', username='sa', password='YourStrongPassword123', driver='{ODBC Driver 17 for SQL Server}'):
    # Tworzenie ciągu połączenia
    conn_str = f'DRIVER={driver};SERVER={server};DATABASE=master;UID={username};PWD={password}'

    try:
        # Nawiązanie połączenia
        conn = pyodbc.connect(conn_str)
        conn.autocommit = True
        # Utworzenie kursora
        cursor = conn.cursor()
        # Polecenie SQL CREATE DATABASE
        create_db_query = f"CREATE DATABASE {database_name}"
        # Wykonanie polecenia
        cursor.execute(create_db_query)
        # Zatwierdzenie zmian
        conn.commit()
        print(f"Baza danych {database_name} została utworzona.")
    except Exception as e:
        print(f"Wystąpił błąd podczas tworzenia bazy danych: {str(e)}")
    finally:
        # Zamykanie kursora i połączenia
        cursor.close()
        conn.close()

# Przykładowe użycie funkcji
#create_database('BAZUNIA2')
