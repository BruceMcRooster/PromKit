import re


def get_ticket_number(row):
    return int(re.sub("[A-Za-z]", "", row[0]))


if __name__ == "__main__":
    print()
