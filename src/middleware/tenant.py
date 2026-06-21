from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from src.auth.jwt import decode_access_token
from jose import JWTError

PUBLIC_PATHS = {"/auth/login", "/auth/refresh", "/docs", "/openapi.json", "/health"}


class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in PUBLIC_PATHS or request.url.path.startswith("/docs"):
            return await call_next(request)

        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return await call_next(request)

        try:
            token = auth_header.split(" ", 1)[1]
            payload = decode_access_token(token)
            request.state.organization_id = payload["org"]
            request.state.user_id = payload["sub"]
            request.state.role = payload["role"]
        except (JWTError, KeyError, IndexError):
            pass  # Auth errors handled by RBAC dependency

        return await call_next(request)


async def set_tenant_context(db, organization_id: str) -> None:
    """Inject organization_id into PostgreSQL session for RLS."""
    await db.execute(
        f"SET LOCAL app.current_org_id = '{organization_id}'"
    )
