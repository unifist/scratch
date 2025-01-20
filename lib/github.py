import json
import requests

class QL:

    PROJECTS = '{organization(login: "unifist") {projectsV2(first: 100) {nodes {id title number}}}}'

    project_id = None
    project_number = None

    def __init__(self, org, project):

        with open("/opt/service/secret/github.json", "r") as creds_file:

            token = json.load(creds_file)["token"]

            self.session = requests.Session()
            self.session.headers.update({'Authorization': f'Bearer {token}'})

        for node in self.graph(self.PROJECTS)["organization"]["projectsV2"]["nodes"]:

            if node["title"] == project:
                self.project_id = node["id"]
                self.project_number = node["number"]

    def dump(self, data):

        print(json.dumps(data, indent=2, sort_keys=True))

    def graph(self, query):

        response = self.session.post("https://api.github.com/graphql", json={"query": query}).json()

        if "data" not in response:
            self.dump(response)

        return response["data"]

    def draft(self, title, body):

        response = self.graph(
            'mutation {addProjectV2DraftIssue(input: {projectId: "' + self.project_id +
            '" title: "' + title + '" body: "' + body + '"}) {projectItem {id fullDatabaseId}}}'
        )

        if "addProjectV2DraftIssue" not in response:
            self.dump(response)

        item_id = response["addProjectV2DraftIssue"]["projectItem"]["fullDatabaseId"]

        return f"https://github.com/orgs/unifist/projects/{self.project_number}/views/1?pane=issue&itemId={item_id}"
