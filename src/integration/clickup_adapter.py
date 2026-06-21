import requests
from src.config import get_settings
from .pm_adapter import PMAdapter, PMTask

settings = get_settings()
CLICKUP_API = "https://api.clickup.com/api/v2"


class ClickUpAdapter(PMAdapter):
    def push_tasks(self, project_key: str, tasks: list[PMTask]) -> list[str]:
        headers = {"Authorization": settings.clickup_api_token, "Content-Type": "application/json"}
        created = []
        for task in tasks:
            payload = {
                "name": task.title,
                "description": task.description,
                "time_estimate": int(task.estimate_days * 8 * 3600 * 1000),  # ms
                "tags": task.labels,
            }
            resp = requests.post(
                f"{CLICKUP_API}/list/{project_key}/task",
                json=payload,
                headers=headers,
                timeout=30,
            )
            resp.raise_for_status()
            created.append(resp.json()["id"])
        return created
