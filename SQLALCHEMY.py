import pandas as pd
from sqlalchemy import create_engine

# Parametry połączenia
server = 'localhost'
database = 'NowaBazaDanych2'
username = 'SA'
password = 'YourStrongPassword123'
driver = 'ODBC Driver 17 for SQL Server'

# Tworzenie silnika SQLAlchemy
engine = create_engine(f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}')

# Ładowanie danych z pliku CSV
df = pd.read_csv('LA_crimes_generate_data.csv', encoding='utf-8')

# Wybierz tylko co 1000 wiersz
df = df.iloc[::100]

# Mapowanie DataFrame na istniejącą tabelę w bazie danych
df.to_sql('Pracownicy15', engine, if_exists='append', index=False)

print("Wybrane dane zostały dodane do tabeli w bazie danych.")

