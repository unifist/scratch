import gspread

def connect():

    return gspread.service_account(filename="/opt/service/secret/gcloud.json")
