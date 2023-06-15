import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
import openpyxl
import pandas as pd
import requests
import joblib
from io import BytesIO
from github import Github
import io
import base64
import pickle
from github import Github, UnknownObjectException
from google.oauth2 import service_account
import pyparsing
import gspread


# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"
    ],
)
client=gspread.authorize(credentials)

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
        train_problems = train_problems.append({
            "Trainset": trainset,
            "Date problem's found": found_date,
            "Date problem's closed": closed_date,
            "Train Number": train_number,
            "Problem Description": description,
            "Problem Solution": solution,
            "Cause Classification": cause_classification,
            "Problem Classification": problem_classification,
            "Component name": component_name,
            "Number of Component": num_component
        }, ignore_index=True)
        # Write the data to Google Drive
        write_to_google_drive(train_problems)
        st.success("Train problem added successfully!")
    # Display the train problem data table
    st.write(train_problems)
 #sheet_url = st.secrets["private_gsheets_url"]
 #               sheet=client.open("database").sheet1
 #               sheet.update([database_df.columns.values.tolist()]+database_df.values.tolist())
 #               st.info("Total rows :"+str(len(database_df)))       

if __name__ == "__main__":
    main()
