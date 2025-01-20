import json
import atproto

def connect():

    with open("/opt/service/secret/bsky.json", "r") as creds_file:
        creds = json.load(creds_file)

    client = atproto.Client(creds["url"])
    profile = client.login(creds["handle"], creds["password"])

    return client, profile
