import re

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from credentials import get_credentials

SHEET_ID = "1KXDCrIQOtmQSq8qNsFJU6rgBdCJysihnllNukc44Wk0"
SHEET_NAME = "Sheet1"
FULL_FILE_RANGE = "A1:F"
WITHOUT_HEADER_RANGE = "A2:F"


# From Google Sheets API docs (https://developers.google.com/sheets/api/guides/values#read_a_single_range)
def read_data() -> list[list[str]] | HttpError:
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


# From Google Sheets API docs (https://developers.google.com/sheets/api/guides/values#append_values)
def append_values(values: list[list[str]]) -> dict | HttpError:
    creds = get_credentials()
    try:
        service = build('sheets', 'v4', credentials=creds)

        body = {
            'values': values
        }
        result = service.spreadsheets().values().append(
            spreadsheetId=SHEET_ID, range=SHEET_NAME,
            valueInputOption="USER_ENTERED", body=body).execute()
        print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
        return result

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


def get_ticket_number(row: list[str]):
    return int(re.sub("[A-Za-z]", "", row[0]))


def get_new_id(name: str):
    try:
        number = get_ticket_number(sorted(read_data(), key=get_ticket_number)[-1]) + 1
    except IndexError:
        number = 1  # Because there aren't any tickets
    initials = name.split()[0][0].capitalize() + name.split()[1][0].capitalize()
    return str(number) + initials


if __name__ == "__main__":
    append_values(
        [
            ["0DR", "Donut Reply", "test@email.com", "No", "N/A", "No"], # TODO: Set up test email
        ]
    )
    data = read_data()
    print(sorted(data, key=get_ticket_number))

