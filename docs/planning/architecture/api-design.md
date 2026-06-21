# API Design — AI ReqInsight & Estimator

> Output of Architect Agent — `.ai-factory/agents/architect-agent.md`

---

## 1. Scope

- **Style:** REST over HTTPS
- **Base path:** `/api/v1`
- **Auth:** Bearer JWT — header `Authorization: Bearer <token>`
- **Versioning:** URL path (`/v1`, `/v2`) — no header versioning
- **Tenant context:** JWT payload contains `organization_id`; all endpoints are automatically scoped
- **Standard error format:**
```json
{
  "error": {
    "code": "DOCUMENT_TOO_LARGE",
    "message": "File exceeds 50MB limit",
    "details": {}
  }
}
```

---

## 2. Main Endpoints

### 2.1 Auth

| Method | Path | Description | Auth | Request | Response |
|--------|------|-------------|------|---------|----------|
| POST | `/auth/login` | Login | None | `{email, password}` | `{access_token, refresh_token}` |
| POST | `/auth/refresh` | Refresh token | Refresh token | `{refresh_token}` | `{access_token}` |
| POST | `/auth/logout` | Logout | JWT | — | 204 |

### 2.2 Projects

| Method | Path | Description | Auth | Request | Response |
|--------|------|-------------|------|---------|----------|
| GET | `/projects` | List projects for the org | JWT | `?page&limit&status` | `{data: Project[], total}` |
| POST | `/projects` | Create a new project | JWT (ba/pm/admin) | `{name, description?}` | `Project` |
| GET | `/projects/:id` | Project details | JWT | — | `Project` |
| PATCH | `/projects/:id` | Update project | JWT (ba/pm/admin) | `{name?, status?}` | `Project` |
| DELETE | `/projects/:id` | Soft delete project | JWT (admin) | — | 204 |

### 2.3 Documents (Ingestion)

| Method | Path | Description | Auth | Request | Response |
|--------|------|-------------|------|---------|----------|
| POST | `/projects/:id/documents` | Upload file(s) | JWT | `multipart/form-data`: files + `{version_label?}` | `{documents: Document[], job_ids: string[]}` |
| GET | `/projects/:id/documents` | List documents | JWT | — | `Document[]` |
| GET | `/documents/:id/status` | Parse status | JWT | — | `{status, progress_pct}` |
| DELETE | `/documents/:id` | Delete document | JWT (admin/ba) | — | 204 |

### 2.4 Analysis (AI Core)

| Method | Path | Description | Auth | Request | Response |
|--------|------|-------------|------|---------|----------|
| GET | `/projects/:id/analysis` | Get all AI results | JWT | `?type=risk,gap,clarification,suggestion,test_case&status=pending,approved,rejected` | `AnalysisResult[]` |
| GET | `/analysis/:id` | Single result details | JWT | — | `AnalysisResult` (with chunk citation) |
| PATCH | `/analysis/:id` | Edit AI result content | JWT (ba/tech_lead/pm) | `{title?, content?}` | `AnalysisResult` |
| POST | `/projects/:id/analysis/rerun` | Re-run analysis | JWT (admin/pm) | `{persona?: 'ba','tech_lead','qa', document_ids?: string[]}` | `{job_id}` |
| POST | `/projects/:id/delta` | Trigger delta analysis | JWT | `{new_document_id, base_document_id}` | `{job_id}` |

### 2.5 Approval (Collaboration)

| Method | Path | Description | Auth | Request | Response |
|--------|------|-------------|------|---------|----------|
| POST | `/analysis/:id/approve` | Approve finding | JWT (role-based, BR-12) | `{comment?}` | `AnalysisResult` |
| POST | `/analysis/:id/reject` | Reject finding | JWT (role-based, BR-12) | `{comment}` | `AnalysisResult` |
| GET | `/analysis/:id/history` | Approval history | JWT | — | `ApprovalRecord[]` |
| POST | `/projects/:id/bulk-approve` | Bulk approve | JWT (pm/admin) | `{analysis_result_ids: string[]}` | `{approved: number, failed: number}` |

### 2.6 AI Chatbot (Collaboration)

| Method | Path | Description | Auth | Request | Response |
|--------|------|-------------|------|---------|----------|
| POST | `/projects/:id/chat` | Chat with AI about documents | JWT | `{message, thread_id?}` | `{reply, citations: ChunkRef[], thread_id}` |
| GET | `/projects/:id/chat/:thread_id` | Thread history | JWT | — | `Message[]` |

### 2.7 Estimation & Export

| Method | Path | Description | Auth | Request | Response |
|--------|------|-------------|------|---------|----------|
| GET | `/projects/:id/wbs` | Get current WBS | JWT | — | `WBSItem[]` (tree) |
| POST | `/projects/:id/wbs/generate` | Generate WBS from Approved items | JWT (pm/admin) | `{rate_card_id}` | `{job_id}` |
| PATCH | `/wbs/:id` | Edit WBS item | JWT (pm/admin) | `{title?, effort_*?, risk_buffer_pct?}` | `WBSItem` |
| POST | `/projects/:id/export/excel` | Export Excel quotation | JWT (pm/presales/admin) | `{rate_card_id}` | `{download_url, expires_at}` |
| POST | `/projects/:id/sync/jira` | Sync to Jira | JWT (pm/admin) | `{jira_project_key, board_id?}` | `{synced: number, errors: []}` |
| POST | `/projects/:id/sync/linear` | Sync to Linear | JWT (pm/admin) | `{team_id}` | `{synced: number, errors: []}` |
| POST | `/projects/:id/sync/clickup` | Sync to ClickUp | JWT (pm/admin) | `{list_id}` | `{synced: number, errors: []}` |

### 2.8 Rate Card (Admin)

| Method | Path | Description | Auth | Request | Response |
|--------|------|-------------|------|---------|----------|
| GET | `/rate-cards` | List Rate Cards for the org | JWT | — | `RateCard[]` |
| POST | `/rate-cards` | Create Rate Card | JWT (admin) | `{name, currency, entries: [{role, seniority, daily_rate}]}` | `RateCard` |
| PUT | `/rate-cards/:id` | Full update | JWT (admin) | `{name?, entries}` | `RateCard` |

---

## 3. Key Request Flows

### Upload → Analysis (Async)
```
POST /projects/:id/documents
  → 202 Accepted + {job_ids}
  → Client poll: GET /documents/:id/status
  → status: "done" → GET /projects/:id/analysis
```

### Approval → Export
```
POST /analysis/:id/approve  (multiple times for multiple items)
  → POST /projects/:id/wbs/generate
  → 202 + {job_id}
  → POST /projects/:id/export/excel
  → {download_url} → Client download
```

---

## 4. Errors & Status Codes

| HTTP Code | Error Code | When |
|-----------|------------|------|
| 400 | `VALIDATION_ERROR` | Invalid input |
| 400 | `DOCUMENT_TOO_LARGE` | File > 50MB |
| 400 | `UNSUPPORTED_FORMAT` | Unsupported file format |
| 401 | `UNAUTHORIZED` | Token missing or expired |
| 403 | `FORBIDDEN` | Valid user but insufficient permissions (RBAC) |
| 403 | `CROSS_TENANT_ACCESS` | Attempt to access another org's resource |
| 404 | `NOT_FOUND` | Resource does not exist |
| 409 | `ALREADY_APPROVED` | Approving an already Approved/Rejected item |
| 422 | `NO_APPROVED_ITEMS` | Exporting when no Approved items exist |
| 429 | `RATE_LIMITED` | Rate limit exceeded |
| 500 | `INTERNAL_ERROR` | Server error |
| 503 | `AI_UNAVAILABLE` | LLM provider not responding |

---

## 5. Idempotency & Rate Limiting

- Upload: idempotent via `Idempotency-Key` header (optional)
- PM tools sync: idempotent — check existing item before creating a new one (BR-26)
- Rate limit: 100 req/min per user; 10 uploads/min per org
- AI analysis jobs: max 5 concurrent per org

---

## 6. Links

- Architecture: `docs/planning/architecture/architecture.md`
- Database: `docs/planning/architecture/database-design.md`
