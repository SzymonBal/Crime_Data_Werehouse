'''import streamlit as st
from create_database import create_database
from SQLALCHEMY import load_data_to_database
from pyspark.sql.functions import *


# Tytuł aplikacji
st.title("Aplikacja ETL")


# Formularz do tworzenia nowej bazy danych
st.header("Utwórz nową bazę danych")
new_database_name = st.text_input("Wprowadź nazwę nowej bazy danych:")
create_button = st.button("Utwórz bazę danych")

if create_button:
    create_database(new_database_name)
    st.success(f"Baza danych {new_database_name} została utworzona.")

# Formularz do wczytywania danych do bazy danych
st.header("Wczytaj dane do istniejącej bazy danych")
existing_database_name = st.text_input("Wprowadź nazwę istniejącej bazy danych:")
csv_file = st.file_uploader("Wybierz plik CSV do wczytania:")

if csv_file is not None:
    load_button = st.button("Wczytaj dane")

    if load_button:
        with st.spinner("Trwa wczytywanie danych..."):
            df = load_data_to_database(existing_database_name, csv_file)
        st.success("Dane zostały wczytane do bazy danych.")


st.header("ETLE operacje na kolumnach czyszczące dane")



df1 = df.withColumn("value_divided", col("Time OCC") / 100)

# Zamiana kropki na dwukropek w kolumnie "value_divided" i tworzenie nowej kolumny "time_fixed"
df1 = df1.withColumn("Time", round(col("value_divided"), 0))

df1 = df1.withColumn("Time", col("Time").cast("integer"))

# Wyświetlenie wyniku
st.write(df1.select('Time').show())'''








import streamlit as st
import pyodbc
import pandas as pd
from sqlalchemy import create_engine


def create_database(database_name):
    # Parametry połączenia
    server = 'localhost'
    username = 'sa'
    password = 'YourStrongPassword123'
    driver = '{ODBC Driver 17 for SQL Server}'

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
        
        st.success(f"Baza danych {database_name} została utworzona.")
        
    except pyodbc.Error as e:
        error_code = e.args[0]
        if error_code == '42000':
            st.warning("Baza o takiej nazwie już istnieje.")
        else:
            st.error(f"Wystąpił błąd: {str(e)}")
        
    finally:
        # Zamykanie kursora i połączenia
        cursor.close()
        conn.close()


def import_csv_to_database(database_name, csv_file_path):
    # Parametry połączenia
    server = 'localhost'
    username = 'SA'
    password = 'YourStrongPassword123'
    driver = 'ODBC Driver 17 for SQL Server'

    # Tworzenie silnika SQLAlchemy
    engine = create_engine(f'mssql+pyodbc://{username}:{password}@{server}/{database_name}?driver={driver}')

    try:
        # Ładowanie danych z pliku CSV
        df = pd.read_csv('LA_crimes_generate_data.csv', encoding='utf-8')
        df = df.iloc[::10000]
        # Mapowanie DataFrame na istniejącą tabelę w bazie danych
        df.to_sql(database_name, engine, if_exists='append', index=False)

        st.success("Dane zostały zaimportowane do tabeli w bazie danych.")
    except Exception as e:
        st.error(f"Wystąpił błąd podczas importowania danych: {str(e)}")


def main():
    st.sidebar.title("Nawigacja")
    selection = st.sidebar.radio("Wybierz stronę:", ["Utwórz bazę danych", "Wczytaj dane", "Importuj dane z CSV"])

    if selection == "Utwórz bazę danych":
        st.title("Kreator bazy danych")
        database_name = st.text_input("Nazwa bazy danych")
        if st.button("Utwórz bazę danych"):
            if database_name:
                create_database(database_name)
            else:
                st.warning("Proszę wprowadzić nazwę bazy danych.")
    
    elif selection == "Importuj dane z CSV":
        st.title("Import danych z pliku CSV do bazy danych")

    # Formularz do wprowadzenia danych
        database_name = st.text_input("Nazwa bazy danych")

        csv_file_path = st.file_uploader("Wybierz plik CSV")

        if st.button("Importuj dane"):
            if database_name and csv_file_path:
                import_csv_to_database(database_name, csv_file_path)
            else:
                st.warning("Proszę uzupełnić wszystkie pola.")

if __name__ == "__main__":
    main()

