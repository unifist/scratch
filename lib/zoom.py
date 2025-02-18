import json
import base64
import requests

class Client:

    session = None

    def __init__(self):

        with open("/opt/service/secret/zoom.json", "r") as creds_file:
            creds = json.load(creds_file)

        base64_creds = base64.b64encode(f"{creds['client_id']}:{creds['client_secret']}".encode()).decode()
        headers = {
            "Authorization": f"Basic {base64_creds}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "account_credentials", "account_id": creds["account_id"]}

        response = requests.post("https://zoom.us/oauth/token", headers=headers, data=data)
        response.raise_for_status()
        access_token = response.json()["access_token"]

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        })

    def meeting_summaries(self):

        response = self.session.get("https://api.zoom.us/v2/meetings/meeting_summaries").json()

        while response:

            for summary in response["summaries"]:
                yield summary

            if response.get("next_page_token"):
                response = self.session.get(
                    "https://api.zoom.us/v2/meetings/meeting_summaries",
                    json={"next_page_token": response["next_page_token"]}
                ).json()
            else:
                response = None

    def meeting_summary(self, summary):

        return self.session.get(f"https://api.zoom.us/v2/meetings/{summary['meeting_uuid']}/meeting_summary").json()
