import requests
from src.config import get_settings
from .pm_adapter import PMAdapter, PMTask

settings = get_settings()


class JiraAdapter(PMAdapter):
    def __init__(self):
        self._base = settings.jira_url.rstrip("/")
        self._auth = (settings.jira_email, settings.jira_api_token)

    def push_tasks(self, project_key: str, tasks: list[PMTask]) -> list[str]:
        created = []
        for task in tasks:
            payload = {
                "fields": {
                    "project": {"key": project_key},
                    "summary": task.title,
                    "description": {
                        "type": "doc",
                        "version": 1,
                        "content": [{"type": "paragraph", "content": [{"type": "text", "text": task.description}]}],
                    },
                    "issuetype": {"name": "Story"},
                    "story_points": task.estimate_days,
                    "labels": task.labels,
                }
            }
            resp = requests.post(
                f"{self._base}/rest/api/3/issue",
                json=payload,
                auth=self._auth,
                timeout=30,
            )
            resp.raise_for_status()
            created.append(resp.json()["key"])
        return created
