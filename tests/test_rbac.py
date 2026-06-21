import uuid
import pytest
from src.auth.rbac import ROLE_PERMISSIONS, Permission, CurrentUser
from src.models.user import UserRole


def _user(role: UserRole) -> CurrentUser:
    return CurrentUser(str(uuid.uuid4()), str(uuid.uuid4()), role)


def test_admin_has_all_permissions():
    user = _user(UserRole.admin)
    for perm in Permission:
        assert user.has_permission(perm), f"Admin missing {perm}"


def test_ba_can_upload_and_view():
    user = _user(UserRole.ba)
    assert user.has_permission(Permission.upload_document)
    assert user.has_permission(Permission.view_analysis)
    assert user.has_permission(Permission.edit_analysis)


def test_ba_cannot_export_quotation():
    user = _user(UserRole.ba)
    assert not user.has_permission(Permission.export_quotation)


def test_presales_can_export_quotation():
    user = _user(UserRole.presales)
    assert user.has_permission(Permission.export_quotation)


def test_qa_cannot_approve_risk():
    user = _user(UserRole.qa)
    assert not user.has_permission(Permission.approve_risk_technical)


def test_tech_lead_can_approve_risk():
    user = _user(UserRole.tech_lead)
    assert user.has_permission(Permission.approve_risk_technical)


def test_pm_can_sync_pm_tools():
    user = _user(UserRole.pm)
    assert user.has_permission(Permission.sync_pm_tools)
