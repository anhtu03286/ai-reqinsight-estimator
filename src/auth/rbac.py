from enum import Enum
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from src.auth.jwt import decode_access_token
from src.models.user import UserRole

bearer_scheme = HTTPBearer()


class Permission(str, Enum):
    upload_document = "upload_document"
    view_analysis = "view_analysis"
    edit_analysis = "edit_analysis"
    approve_clarification = "approve_clarification"
    approve_risk_technical = "approve_risk_technical"
    approve_suggestion = "approve_suggestion"
    export_quotation = "export_quotation"
    sync_pm_tools = "sync_pm_tools"
    export_test_cases = "export_test_cases"
    manage_rate_card = "manage_rate_card"
    manage_users = "manage_users"


ROLE_PERMISSIONS: dict[UserRole, set[Permission]] = {
    UserRole.admin: set(Permission),  # all permissions
    UserRole.ba: {
        Permission.upload_document, Permission.view_analysis, Permission.edit_analysis,
        Permission.approve_clarification, Permission.export_test_cases,
    },
    UserRole.pm: {
        Permission.upload_document, Permission.view_analysis, Permission.edit_analysis,
        Permission.approve_clarification, Permission.approve_risk_technical,
        Permission.approve_suggestion, Permission.export_quotation, Permission.sync_pm_tools,
    },
    UserRole.presales: {
        Permission.upload_document, Permission.view_analysis, Permission.export_quotation,
    },
    UserRole.tech_lead: {
        Permission.upload_document, Permission.view_analysis, Permission.edit_analysis,
        Permission.approve_risk_technical,
    },
    UserRole.qa: {
        Permission.view_analysis, Permission.export_test_cases,
    },
}


class CurrentUser:
    def __init__(self, user_id: str, organization_id: str, role: UserRole):
        self.user_id = user_id
        self.organization_id = organization_id
        self.role = role

    def has_permission(self, permission: Permission) -> bool:
        return permission in ROLE_PERMISSIONS.get(self.role, set())


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> CurrentUser:
    try:
        payload = decode_access_token(credentials.credentials)
        return CurrentUser(
            user_id=payload["sub"],
            organization_id=payload["org"],
            role=UserRole(payload["role"]),
        )
    except (JWTError, KeyError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")


def require_permission(permission: Permission):
    async def checker(user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if not user.has_permission(permission):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN")
        return user
    return checker
