import streamlit as st
import pandas as pd
import gspread
import base64
from oauth2client.service_account import ServiceAccountCredentials

def main():
    st.title("Train Problem Tracker")
    st.write("Enter the details of train problems")

    # Create empty dataframe to store the train problem data
    train_problems = pd.DataFrame(columns=[
        "Trainset", "Date problem's found", "Date problem's closed",
        "Train Number", "Problem Description", "Problem Solution",
        "Cause Classification", "Problem Classification",
        "Component name", "Number of Component"
    ])

    # Create input fields for each column
    trainset = st.text_input("Trainset")
    found_date = st.date_input("Date problem's found")
    closed_date = st.date_input("Date problem's closed")
    train_number = st.text_input("Train Number")
    description = st.text_input("Problem Description")
    solution = st.text_input("Problem Solution")
    cause_classification = st.text_input("Cause Classification")
    problem_classification = st.text_input("Problem Classification")
    component_name = st.text_input("Component name")
    num_component = st.number_input("Number of Component", min_value=0)

    # Create a button to submit the data
    if st.button("Add Train Problem"):
        # Append the input data as a new row to the dataframe
        new_row = {
            "Trainset": trainset,
            "Date problem's found": found_date.strftime("%Y-%m-%d"),
            "Date problem's closed": closed_date.strftime("%Y-%m-%d"),
            "Train Number": train_number,
            "Problem Description": description,
            "Problem Solution": solution,
            "Cause Classification": cause_classification,
            "Problem Classification": problem_classification,
            "Component name": component_name,
            "Number of Component": num_component
        }
        train_problems = train_problems.append(new_row, ignore_index=True)

        # Write the data to Google Drive
        write_to_google_drive(train_problems)

        st.success("Train problem added successfully!")

    # Display the train problem data table
    st.write(train_problems)

    # Button to show all data
    if st.button("Show All Data"):
        data = read_from_google_drive()
        st.write(data)
        
    # Button to download data
    if st.button("Download Data"):
        data = read_from_google_drive()
        file_path = "train_problems.xlsx"
        data.to_excel(file_path, index=False)
        download_file(file_path, "train_problems.xlsx")

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

def download_file(file_path, file_name):
    with open(file_path, "rb") as file:
        data = file.read()
    base64_data = base64.b64encode(data).decode("utf-8")
    st.markdown(
        f'<a href="data:application/octet-stream;base64,{base64_data}" download="{file_name}">Download File</a>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
