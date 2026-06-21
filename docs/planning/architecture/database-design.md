# Database Design — AI ReqInsight & Estimator

> Output of Architect Agent — `.ai-factory/agents/architect-agent.md`

---

## 1. Scope

- **Primary DB:** PostgreSQL with Row-Level Security (RLS) for multi-tenant isolation
- **Vector DB:** pgvector extension (or Qdrant if scale requires separation) — stores embeddings for semantic matching
- **Cache:** Redis — job queue, session cache, rate limiting
- **Object Storage:** S3-compatible — stores original files AES-256 encrypted

**Constraints:**
- Every business table must have an `organization_id` column — mandatory in all queries
- No cross-organization foreign keys
- Soft delete (`deleted_at`) instead of hard delete for auditability

---

## 2. Main Entities

| Entity | Description | Key / Primary Relationships |
|--------|-------------|----------------------------|
| `organizations` | Tenant root — each company is 1 org | PK: `id` |
| `users` | User accounts | FK: `organization_id`; roles: enum |
| `projects` | Document group for 1 bid/project | FK: `organization_id` |
| `documents` | Uploaded file metadata + storage ref | FK: `project_id`, `organization_id` |
| `document_chunks` | Text segments after chunking | FK: `document_id`; has `embedding` vector |
| `analysis_results` | AI results (gap/risk/clarification/suggestion/test_case) | FK: `project_id`, `document_id` (optional) |
| `approval_records` | Approve/reject history | FK: `analysis_result_id`, `user_id` |
| `wbs_items` | Generated Epic/Story/Task | FK: `project_id`; self-ref `parent_id` |
| `rate_cards` | Daily rates by role + seniority | FK: `organization_id` |
| `rate_card_entries` | Details per level (Junior Dev, Senior BA…) | FK: `rate_card_id` |

---

## 3. Detailed Schema

```sql
-- Tenant root
CREATE TABLE organizations (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name          VARCHAR(255) NOT NULL,
  created_at    TIMESTAMPTZ DEFAULT NOW(),
  deleted_at    TIMESTAMPTZ
);

-- Users with RBAC
CREATE TABLE users (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES organizations(id),
  email           VARCHAR(255) NOT NULL UNIQUE,
  role            VARCHAR(50) NOT NULL CHECK (role IN ('admin','ba','pm','presales','tech_lead','qa')),
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  deleted_at      TIMESTAMPTZ
);

-- Projects
CREATE TABLE projects (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES organizations(id),
  name            VARCHAR(255) NOT NULL,
  status          VARCHAR(50) DEFAULT 'active',
  created_by      UUID REFERENCES users(id),
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  deleted_at      TIMESTAMPTZ
);

-- Documents
CREATE TABLE documents (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES organizations(id),
  project_id      UUID NOT NULL REFERENCES projects(id),
  filename        VARCHAR(500) NOT NULL,
  format          VARCHAR(20) NOT NULL,  -- pdf, docx, md, txt, xlsx, csv
  storage_key     VARCHAR(1000) NOT NULL, -- encrypted Object Storage path
  version_label   VARCHAR(50),           -- v1, v2, v3...
  language        VARCHAR(10),           -- vi, en, auto
  ocr_applied     BOOLEAN DEFAULT FALSE,
  parse_status    VARCHAR(50) DEFAULT 'pending', -- pending/processing/done/failed
  file_size_bytes BIGINT,
  uploaded_by     UUID REFERENCES users(id),
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Chunks after parsing
CREATE TABLE document_chunks (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  document_id     UUID NOT NULL REFERENCES documents(id),
  organization_id UUID NOT NULL REFERENCES organizations(id),
  chunk_index     INTEGER NOT NULL,
  content         TEXT NOT NULL,         -- plain text of the chunk
  page_number     INTEGER,
  section_header  VARCHAR(500),
  embedding       VECTOR(1536),          -- pgvector — used for semantic matching
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- AI results
CREATE TABLE analysis_results (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES organizations(id),
  project_id      UUID NOT NULL REFERENCES projects(id),
  document_id     UUID REFERENCES documents(id),
  chunk_id        UUID REFERENCES document_chunks(id),  -- deep-link citation
  result_type     VARCHAR(50) NOT NULL CHECK (result_type IN ('clarification','risk','gap','suggestion','test_case')),
  severity        VARCHAR(20) CHECK (severity IN ('high','medium','low')),  -- for risk/gap
  title           VARCHAR(500) NOT NULL,
  content         TEXT NOT NULL,
  ai_version      VARCHAR(50),           -- provider + model version at generation time
  status          VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending','approved','rejected')),
  original_content TEXT,                 -- stores original AI version if user edits
  edited_by       UUID REFERENCES users(id),
  edited_at       TIMESTAMPTZ,
  persona         VARCHAR(50),           -- tech_lead, ba, qa if using persona mode
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Approval history
CREATE TABLE approval_records (
  id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  analysis_result_id UUID NOT NULL REFERENCES analysis_results(id),
  user_id            UUID NOT NULL REFERENCES users(id),
  organization_id    UUID NOT NULL REFERENCES organizations(id),
  action             VARCHAR(20) NOT NULL CHECK (action IN ('approved','rejected')),
  comment            TEXT,
  created_at         TIMESTAMPTZ DEFAULT NOW()
);

-- WBS hierarchy
CREATE TABLE wbs_items (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES organizations(id),
  project_id      UUID NOT NULL REFERENCES projects(id),
  parent_id       UUID REFERENCES wbs_items(id),  -- self-ref: Epic→Story→Task
  item_type       VARCHAR(20) NOT NULL CHECK (item_type IN ('epic','story','task')),
  title           VARCHAR(500) NOT NULL,
  description     TEXT,
  complexity      VARCHAR(20) CHECK (complexity IN ('low','medium','high','very_high')),
  effort_dev_md   DECIMAL(8,2),   -- Man-days: developer
  effort_qa_md    DECIMAL(8,2),   -- Man-days: QA
  effort_ba_md    DECIMAL(8,2),   -- Man-days: BA
  effort_pm_md    DECIMAL(8,2),   -- Man-days: PM
  risk_buffer_pct DECIMAL(5,2),   -- % buffer
  historical_ref  VARCHAR(500),   -- reference project from historical matching
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Rate Card
CREATE TABLE rate_cards (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES organizations(id),
  name            VARCHAR(255) NOT NULL,
  currency        VARCHAR(10) DEFAULT 'USD',
  is_active       BOOLEAN DEFAULT TRUE,
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE rate_card_entries (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  rate_card_id  UUID NOT NULL REFERENCES rate_cards(id),
  role          VARCHAR(50) NOT NULL,      -- dev, qa, ba, pm, tech_lead
  seniority     VARCHAR(50) NOT NULL,      -- junior, mid, senior, lead
  daily_rate    DECIMAL(10,2) NOT NULL,
  currency      VARCHAR(10) DEFAULT 'USD'
);
```

---

## 4. Indexes & Constraints

```sql
-- Performance indexes
CREATE INDEX idx_documents_project ON documents(project_id, organization_id);
CREATE INDEX idx_chunks_document ON document_chunks(document_id);
CREATE INDEX idx_analysis_project_type ON analysis_results(project_id, result_type, status);
CREATE INDEX idx_approval_result ON approval_records(analysis_result_id);
CREATE INDEX idx_wbs_project ON wbs_items(project_id, parent_id);

-- Vector similarity search
CREATE INDEX idx_chunks_embedding ON document_chunks USING ivfflat (embedding vector_cosine_ops);

-- Row-Level Security
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE analysis_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE wbs_items ENABLE ROW LEVEL SECURITY;

-- RLS policies (use current_setting to inject organization_id from app)
CREATE POLICY tenant_isolation ON projects
  USING (organization_id = current_setting('app.current_org_id')::UUID);
-- (same pattern for other tables)
```

---

## 5. Migration & Versioning

- Tool: **Flyway** or **Liquibase** (TBD per stack)
- Convention: `V{timestamp}__{description}.sql`
- All migrations must be backward-compatible with the previous version (no column drops in the same release)
- Breaking changes (drop column, rename) → 2-phase: deprecate first, remove after 1 sprint

---

## 6. Links

- Architecture: `docs/planning/architecture/architecture.md`
- Module map: `docs/planning/architecture/module-map.md`
