import requests
from src.config import get_settings
from .pm_adapter import PMAdapter, PMTask

settings = get_settings()
LINEAR_API = "https://api.linear.app/graphql"


class LinearAdapter(PMAdapter):
    def push_tasks(self, project_key: str, tasks: list[PMTask]) -> list[str]:
        headers = {"Authorization": settings.linear_api_key, "Content-Type": "application/json"}
        created = []
        for task in tasks:
            query = """
            mutation CreateIssue($input: IssueCreateInput!) {
              issueCreate(input: $input) { issue { id identifier } }
            }
            """
            variables = {
                "input": {
                    "title": task.title,
                    "description": task.description,
                    "teamId": project_key,
                    "estimate": task.estimate_days,
                    "labelIds": [],
                }
            }
            resp = requests.post(LINEAR_API, json={"query": query, "variables": variables}, headers=headers, timeout=30)
            resp.raise_for_status()
            issue = resp.json()["data"]["issueCreate"]["issue"]
            created.append(issue["identifier"])
        return created
