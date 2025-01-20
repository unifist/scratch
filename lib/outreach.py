import json

def config():

    with open("/opt/service/config/outreach.json", "r") as outreach_file:
        return json.load(outreach_file)
