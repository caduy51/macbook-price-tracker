#!/Users/admin/opt/anaconda3/bin/python3
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import datetime
import mysql.connector
import pandas as pd
import json
from env import DATA_DIR
from logging_config import setup_logging

# Set up logger
logger = setup_logging(os.path.join(DATA_DIR, "logging.txt"))

# python sheets: https://docs.google.com/spreadsheets/d/1AkUttAItO-b9dEH2unxeCC-arH8pUAomCQfxntgduzs/edit?gid=0#gid=0
SPREADSHEET_ID = '1AkUttAItO-b9dEH2unxeCC-arH8pUAomCQfxntgduzs'
RANGE_NAME = 'Data!A1:C8'
API_KEY = 'AIzaSyCv1-KzDV3Vsr0HDYkVkvvQ6rXc4mHXpRs'
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def create_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=3000)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def create_service():
    creds = create_credentials()
    sheets = build(serviceName='sheets', version='v4',
                   credentials=creds).spreadsheets()
    return sheets

def read_values(spreadsheet_id, range_name):
    sheets = create_service()
    rows = sheets.values().get(spreadsheetId=spreadsheet_id,
                               range=range_name).execute().get('values', [])
    for row in rows:
        print(row)

def update_values(spreadsheet_id, range_name, value_input_option, values):
    creds = create_credentials()
    sheets = build(serviceName='sheets', version='v4',
                   credentials=creds).spreadsheets()

    data_dumps = sheets.values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption=value_input_option,
        body=values,
    ).execute()

def create_new_tab(spreadsheet_id, tab_name):
    creds = create_credentials()
    sheetservice = build(serviceName='sheets', version='v4',
                         credentials=creds).spreadsheets()

    body = {
        "requests": [{
            "addSheet": {
                "properties": {
                    "title": tab_name
                }
            }
        }]
    }

    sheetservice.batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()

def load_to_sheets():
    create_credentials()

    # Read data, full load
    with open(os.path.join(DATA_DIR, "output/output.json"), "r") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    # Transform data into body
    data = df.values.tolist()
    headers = [df.columns.values.tolist()]
    body = {"values": headers + data}

    # Create a new sheet tab
    # sheet_tab_name = datetime.datetime.now().strftime("%Y-%m-%d at %H:%M %p")
    sheet_tab_name = "DATA_02"
    # create_new_tab(SPREADSHEET_ID, sheet_tab_name)
    # print("Created new tab. OK")
    # Load to Google Sheets
    update_values(SPREADSHEET_ID, sheet_tab_name + "!A1:I9999", "USER_ENTERED", body)
    logger.info("> Updated Values to Google Sheeets. OK")
    logger.info("Link to google sheets: https://docs.google.com/spreadsheets/d/1AkUttAItO-b9dEH2unxeCC-arH8pUAomCQfxntgduzs/edit?gid=551366507#gid=551366507")
    logger.info("Link to Dashboard: https://lookerstudio.google.com/u/0/reporting/a6940b3b-b157-4e37-be85-a5b0059b5ed1/page/xeYDE")

if __name__ == "__main__":
    load_to_sheets()




