import uuid
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.models.wbs_item import WBSItem
from src.integration.pm_adapter import PMTask


def sync_to_pm(
    project_id: uuid.UUID,
    organization_id: uuid.UUID,
    tool: str,
    project_key: str,
    db: Session,
) -> dict:
    items = db.execute(
        select(WBSItem).where(
            WBSItem.project_id == project_id,
            WBSItem.organization_id == organization_id,
        )
    ).scalars().all()

    tasks = [
        PMTask(
            title=item.title,
            description=item.description or "",
            estimate_days=float((item.effort_dev_md or 0) + (item.effort_qa_md or 0)),
            labels=[item.item_type.value, item.complexity.value if item.complexity else ""],
        )
        for item in items
    ]

    adapter = _get_adapter(tool)
    created_ids = adapter.push_tasks(project_key, tasks)
    return {"tool": tool, "created": len(created_ids), "ids": created_ids}


def _get_adapter(tool: str):
    if tool == "jira":
        from src.integration.jira_adapter import JiraAdapter
        return JiraAdapter()
    elif tool == "linear":
        from src.integration.linear_adapter import LinearAdapter
        return LinearAdapter()
    elif tool == "clickup":
        from src.integration.clickup_adapter import ClickUpAdapter
        return ClickUpAdapter()
    raise ValueError(f"Unknown PM tool: {tool}")
