import uuid
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from src.models.rate_card import RateCard, RateCardEntry


async def get_active_rate_card(organization_id: uuid.UUID, db: AsyncSession) -> RateCard | None:
    result = await db.execute(
        select(RateCard).where(
            RateCard.organization_id == organization_id,
            RateCard.is_active == True,
        ).limit(1)
    )
    return result.scalar_one_or_none()


async def compute_cost(
    project_id: uuid.UUID,
    organization_id: uuid.UUID,
    db: AsyncSession,
) -> dict:
    from sqlalchemy import select as sa_select
    from src.models.wbs_item import WBSItem

    rate_card = await get_active_rate_card(organization_id, db)
    if not rate_card:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="No active rate card")

    entries_result = await db.execute(
        select(RateCardEntry).where(RateCardEntry.rate_card_id == rate_card.id)
    )
    entries = entries_result.scalars().all()
    rate_map: dict[str, Decimal] = {f"{e.role}:{e.seniority}": e.daily_rate for e in entries}
    default_rate = {
        "dev": rate_map.get("dev:mid", Decimal("500")),
        "qa": rate_map.get("qa:mid", Decimal("300")),
        "ba": rate_map.get("ba:mid", Decimal("400")),
        "pm": rate_map.get("pm:mid", Decimal("500")),
    }

    wbs_result = await db.execute(
        sa_select(WBSItem).where(
            WBSItem.project_id == project_id,
            WBSItem.organization_id == organization_id,
        )
    )
    items = wbs_result.scalars().all()

    total = Decimal("0")
    breakdown = []
    for item in items:
        buffer = (item.risk_buffer_pct or Decimal("20")) / Decimal("100")
        dev_cost = (item.effort_dev_md or Decimal("0")) * default_rate["dev"]
        qa_cost = (item.effort_qa_md or Decimal("0")) * default_rate["qa"]
        ba_cost = (item.effort_ba_md or Decimal("0")) * default_rate["ba"]
        pm_cost = (item.effort_pm_md or Decimal("0")) * default_rate["pm"]
        item_base = dev_cost + qa_cost + ba_cost + pm_cost
        item_total = item_base * (1 + buffer)
        total += item_total
        breakdown.append({
            "item_id": str(item.id),
            "title": item.title,
            "base_cost": float(item_base),
            "risk_buffer_pct": float(item.risk_buffer_pct or 20),
            "total_cost": float(item_total),
        })

    return {
        "currency": rate_card.currency,
        "total": float(total),
        "breakdown": breakdown,
    }
