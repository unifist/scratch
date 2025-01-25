import gspread
import unum


class API:

    def __init__(self):
        """ Conencts to gspread using the deaful secret file """

        self.gspread = gspread.service_account(filename="/opt/service/secret/gcloud.json")


    def rows(self, sheet, worksheet):
        """ Returns all rows """

        return self.gspread.open(sheet).worksheet(worksheet).get_all_records()


    def values(self, sheet, worksheet, column):
        """ Returns all the values for a column"""

        return [row.get(column) for row in self.rows(sheet, worksheet)]


    def closest(self, sheet, worksheet, column, needle):
        """ Finds the closet match in a Sheet """

        haystack = self.values(sheet, worksheet, column)

        if haystack:
            return unum.closest(haystack, needle)

        return None

    def list(self, sheet, worksheet, fields):
        """ List any sheet """

        rows = []

        for row in self.rows(sheet, worksheet):
            values = []
            for field in fields:
                if row.get(field):
                    values.append(row[field])
            rows.append(values)

        return rows
