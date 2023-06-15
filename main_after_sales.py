import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import base64

def main():
    st.title("AFTER SALES PT INKA")
    st.write("Masukkan data gangguan kereta")

    # Create empty dataframe to store the train problem data
    #train_problems = pd.DataFrame(columns=[
    #    "Nama Proyek","Trainset", "Tanggal problem ditemukan", "Tanggal problem terselesaikan",
    #    "Nomor Kereta", "Deskripsi Problem", "Solusi Problem",
    #    "Klasifikasi Penyebab", "Klasifikasi Problem",
    #    "Nama Komponen", "Jumlah Komponen"
    #])

    # Create input fields for each column
    nama_proyek = st.selectbox("Nama Proyek",("438","LRT JAbodebek", "KRDE BIM", "BIAS"))
    trainset = st.text_input("Trainset")
    found_date = st.date_input("Tanggal problem ditemukan")
    closed_date = st.date_input("Tanggal problem terselesaikan")
    train_number = st.text_input("Nomor Kereta")
    description = st.text_input("Deskripsi Problem")
    solution = st.text_input("Solusi Problem")
    cause_classification = st.selectbox("Klasifikasi Penyebab",("Salah desain","Salah Manufaktur", "Komponen tidak berkualitas", "Salah operasional"))
    problem_classification = st.text_input("Klasifikasi Problem")
    component_name = st.text_input("Nama Komponen")
    num_component = st.number_input("Jumlah Komponen", min_value=0)

    # Create a button to submit the data
    if st.button("Masukkan Data Gangguan"):
        # Append the input data as a new row to the dataframe
        new_row = {
            "Nama Proyek":nama_proyek,
            "Trainset": trainset,
            "Tanggal problem ditemukan": found_date.strftime("%Y-%m-%d"),
            "Tanggal problem terselesaikan": closed_date.strftime("%Y-%m-%d"),
            "Nomor Kereta": train_number,
            "Deskripsi Problem": description,
            "Solusi Problem": solution,
            "Klasifikasi Penyebab": cause_classification,
            "Klasifikasi Problem": problem_classification,
            "Nama Komponen": component_name,
            "Jumlah Komponen": num_component
        }
        train_problems = train_problems.append(new_row, ignore_index=True)

        # Write the data to Google Drive
        write_to_google_drive(train_problems)

        st.success("Data Gangguan berhasil dimasukkan!")

    # Display the train problem data table
    st.write(train_problems)

    # Button to show all data
    if st.button("Tunjukkan semua data"):
        data = read_from_google_drive()
        st.write(data)

    # Button to download data
    st.markdown("[Buka Google Sheet](https://docs.google.com/spreadsheets/d/1QdAmuQleyDMxXROQtccwzrJNkSPMCCDQbCwW8SB8EVc)")


def write_to_google_drive(train_problems):
    # Authenticate and create a connection to Google Drive
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(credentials)

    # Open the Google Sheet
    sheet = client.open("after_sales").sheet1

    # Convert the dataframe to a list of lists
    data = [train_problems.columns.tolist()] + train_problems.values.tolist()

    # Append the data to the sheet
    sheet.append_rows(data)

def read_from_google_drive():
    # Authenticate and create a connection to Google Drive
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(credentials)

    # Open the Google Sheet
    sheet = client.open("after_sales").sheet1

    # Read all values from the sheet
    values = sheet.get_all_values()

    # Convert the values to a DataFrame
    data = pd.DataFrame(values[1:], columns=values[0])

    return data

if __name__ == "__main__":
    main()
