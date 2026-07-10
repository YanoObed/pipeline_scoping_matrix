import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json",
    scope
)

client = gspread.authorize(creds)

SPREADSHEET_NAME = "Pipeline Scoping Matrix"


def get_pipeline_sheet():
    spreadsheet = client.open(SPREADSHEET_NAME)
    return spreadsheet.worksheet("Pipeline")