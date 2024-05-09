import streamlit as st
from create_database import create_database
from SQLALCHEMY import load_data_to_database



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
            load_data_to_database(existing_database_name, csv_file)
        st.success("Dane zostały wczytane do bazy danych.")


