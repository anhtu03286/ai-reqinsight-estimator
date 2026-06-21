"""
KL-P-001: Cross-tenant access must return 404, not 403.
Tests confirm that services checking organization_id raise 404 (not expose resource existence).
"""
import uuid
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import HTTPException
from src.collaboration.approval_service import approve_result
from src.models.approval_record import ApprovalAction
from src.auth.rbac import CurrentUser
from src.models.user import UserRole


def make_user(role=UserRole.pm):
    return CurrentUser(str(uuid.uuid4()), str(uuid.uuid4()), role)


@pytest.mark.asyncio
async def test_approve_nonexistent_result_returns_404():
    """Cross-tenant or missing resource: 404, not 403 or 500."""
    db = AsyncMock()
    scalar_mock = MagicMock()
    scalar_mock.scalar_one_or_none.return_value = None
    db.execute = AsyncMock(return_value=scalar_mock)

    user = make_user(UserRole.pm)
    with pytest.raises(HTTPException) as exc:
        await approve_result(uuid.uuid4(), ApprovalAction.approved, None, user, db)

    assert exc.value.status_code == 404, "Must return 404, not 403 (KL-P-001)"
