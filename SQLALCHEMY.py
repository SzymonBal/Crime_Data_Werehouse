'''import pandas as pd
from sqlalchemy import create_engine

# Parametry połączenia
server = 'localhost'
database = 'BAZUNIA1'
username = 'SA'
password = 'YourStrongPassword123'
driver = 'ODBC Driver 17 for SQL Server'

# Tworzenie silnika SQLAlchemy
engine = create_engine(f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}')

# Ładowanie danych z pliku CSV
df = pd.read_csv('LA_crimes_generate_data.csv', encoding='utf-8')

# Wybierz tylko co 1000 wiersz
df = df.iloc[::1000]

# Mapowanie DataFrame na istniejącą tabelę w bazie danych
df.to_sql('BAZUNIA1', engine, if_exists='append', index=False)

print("Wybrane dane zostały dodane do tabeli w bazie danych.")
'''
import pandas as pd
from sqlalchemy import create_engine

def load_data_to_database(database_name, csv_file_path, server='localhost', username='SA', password='YourStrongPassword123', driver='ODBC Driver 17 for SQL Server'):
    # Tworzenie silnika SQLAlchemy
    engine = create_engine(f'mssql+pyodbc://{username}:{password}@{server}/{database_name}?driver={driver}')

    # Ładowanie danych z pliku CSV
    df = pd.read_csv(csv_file_path, encoding='utf-8')

    # Wybierz tylko co 1000 wiersz
    df = df.iloc[::1000]

    # Mapowanie DataFrame na istniejącą tabelę w bazie danych
    df.to_sql(database_name, engine, if_exists='append', index=False)

    print("Wybrane dane zostały dodane do tabeli w bazie danych.")

# Przykładowe użycie funkcji
database_name = 'BAZUNIA2'
csv_file_path = 'LA_crimes_generate_data.csv'
load_data_to_database(database_name, csv_file_path)
