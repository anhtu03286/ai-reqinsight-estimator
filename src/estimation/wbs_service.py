import uuid
import json
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.models.analysis_result import AnalysisResult, ApprovalStatus
from src.models.wbs_item import WBSItem, WBSItemType, Complexity
from src.ai.ai_factory import get_llm_provider
from decimal import Decimal


WBS_GENERATION_PROMPT = """You are a software estimation expert. Based on the approved analysis results below, generate a Work Breakdown Structure (WBS) in JSON.

Return a JSON object:
{
  "wbs": [
    {
      "item_type": "<epic|story|task>",
      "title": "<title>",
      "description": "<optional>",
      "complexity": "<simple|medium|complex>",
      "effort_dev_md": <float>,
      "effort_qa_md": <float>,
      "effort_ba_md": <float>,
      "effort_pm_md": <float>,
      "risk_buffer_pct": <float 0-50>,
      "children": [...]
    }
  ]
}

Rules:
- complexity simple: dev 1-3 md, medium: 3-8 md, complex: 8-20 md
- QA effort = dev * 0.5 for medium/complex, 0.3 for simple
- BA effort = 0.5 md per story, PM effort = 10% of total
- risk_buffer_pct: 10% for simple, 20% medium, 30% complex
- Only include items derivable from the requirements; do not invent features
"""


def generate_wbs(
    project_id: uuid.UUID,
    organization_id: uuid.UUID,
    db: Session,
) -> list[WBSItem]:
    approved = db.execute(
        select(AnalysisResult).where(
            AnalysisResult.project_id == project_id,
            AnalysisResult.organization_id == organization_id,
            AnalysisResult.status == ApprovalStatus.approved,
        )
    ).scalars().all()

    if not approved:
        return []

    context = "\n\n".join(f"[{r.result_type.value}] {r.title}: {r.content}" for r in approved)
    provider = get_llm_provider()
    response = provider.analyze(WBS_GENERATION_PROMPT, [context])

    wbs_data = []
    if response.results:
        # The WBS comes back as a single item wrapping the wbs list
        raw = json.dumps(response.results)
        try:
            parsed = json.loads(raw)
            wbs_data = parsed if isinstance(parsed, list) else parsed.get("wbs", [])
        except (json.JSONDecodeError, AttributeError):
            wbs_data = response.results

    items = []

    def create_items(entries: list[dict], parent_id: uuid.UUID | None = None) -> list[WBSItem]:
        result = []
        for entry in entries:
            item = WBSItem(
                organization_id=organization_id,
                project_id=project_id,
                parent_id=parent_id,
                item_type=WBSItemType(entry.get("item_type", "task")),
                title=entry.get("title", "")[:500],
                description=entry.get("description"),
                complexity=Complexity(entry.get("complexity", "medium")) if entry.get("complexity") else None,
                effort_dev_md=Decimal(str(entry.get("effort_dev_md", 0))),
                effort_qa_md=Decimal(str(entry.get("effort_qa_md", 0))),
                effort_ba_md=Decimal(str(entry.get("effort_ba_md", 0))),
                effort_pm_md=Decimal(str(entry.get("effort_pm_md", 0))),
                risk_buffer_pct=Decimal(str(entry.get("risk_buffer_pct", 20))),
            )
            db.add(item)
            db.flush()  # get item.id for children
            children = create_items(entry.get("children", []), item.id)
            result.append(item)
            result.extend(children)
        return result

    items = create_items(wbs_data)
    db.commit()
    return items
