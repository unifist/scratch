import gspread
import Levenshtein


def connect():
    """ Conencts to gspread using the deaful secret file """

    return gspread.service_account(filename="/opt/service/secret/gcloud.json")


def rows(client, sheet, worksheet):
    """ Returns all rows """

    return client.open(sheet).worksheet(worksheet).get_all_records()


def values(client, sheet, worksheet, column):
    """ Returns all the values for a column"""

    return [row.get(column) for row in rows(client, sheet, worksheet)]


def closest(client, sheet, worksheet, column, needle):
    """ Finds the closet match in a Sheet """

    haystack = values(client, sheet, worksheet, column)

    if haystack:
        return sorted(haystack, key=lambda value: Levenshtein.distance(value, needle))[0]

    return None
