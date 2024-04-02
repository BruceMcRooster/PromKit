from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from credentials import get_credentials
from utilities import get_ticket_number

SHEET_ID = "1KXDCrIQOtmQSq8qNsFJU6rgBdCJysihnllNukc44Wk0"
SHEET_NAME = "Sheet1"
FULL_FILE_RANGE = "A1:G"
WITHOUT_HEADER_RANGE = "A2:G"


def read_data():
    creds = get_credentials()

    try:
        service = build('sheets', 'v4', credentials=creds)

        result = service.spreadsheets().values().get(
            spreadsheetId=SHEET_ID, range=WITHOUT_HEADER_RANGE).execute()
        rows = result.get('values', [])
        print(f"{len(rows)} rows retrieved")
        return rows
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


def set_value(pos: str, values):
    creds = get_credentials()
    # pylint: disable=maybe-no-member
    try:
        service = build('sheets', 'v4', credentials=creds)

        body = {
            'values': values
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=SHEET_ID, range=F'{SHEET_NAME}!{pos}',
            valueInputOption="USER_ENTERED", body=body).execute()
        return result

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


if __name__ == "__main__":
    data = read_data()
    print(sorted(data, key=get_ticket_number))
