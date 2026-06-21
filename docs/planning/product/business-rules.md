# Business Rules — AI ReqInsight & Estimator

> Output of Product Agent — `.ai-factory/agents/product-agent.md`
> Reference: `docs/planning/product/prd.md`, `docs/specs/requirement.md`

---

## 1. Scope

Applies to all 4 modules: Ingestion & Parsing, AI Core & Delta Analysis, Collaboration & Review, Estimation & Integration.

Actors: BA, PM, Presales, Tech Lead, QA/QC, Admin.

---

## 2. Business Rules

### 2.1 File Upload & Ingestion

| ID | Rule | Condition / Trigger | Expected Result | Exception |
|----|------|---------------------|-----------------|-----------|
| BR-01 | File size limit | Each file upload | Reject files > 50MB, display a clear error message | None |
| BR-02 | Supported formats | File upload | Accept: PDF, DOCX, DOC, MD, TXT, XLSX, XLS, CSV. Reject all other formats | None |
| BR-03 | Multi-file for the same project | Upload multiple files | Group all files into the same Project context; process asynchronously | None |
| BR-04 | OCR mandatory for scanned PDFs | System detects PDF with no text layer | Automatically run OCR before parsing | None |
| BR-05 | Language detection | After text is parsed | Automatically detect language, prioritize Vietnamese or English models | Other languages: best-effort |

### 2.2 AI Analysis

| ID | Rule | Condition / Trigger | Expected Result | Exception |
|----|------|---------------------|-----------------|-----------|
| BR-06 | 3-level Risk classification | AI detects a Risk | High (red): blocks if not addressed; Medium (yellow): warning; Low (green): informational | None |
| BR-07 | Cross-document contradiction | Upload multiple files for the same project | AI detects and flags contradictions between documents, identifies the source of conflict | None |
| BR-08 | Persona-based analysis | User configures a viewpoint | Analysis results prioritized by role: Tech Lead (architectural risks), BA (business gaps), QA (testing risks) | None |
| BR-09 | Delta Analysis — new version | Upload document marked as v2/v3 of an existing project | AI must classify: Added / Removed / Changed scope. Automatically warn about impact on quotation | None |
| BR-10 | Deep-link citation mandatory | AI generates a finding (Gap/Risk/Clarification) | Each finding must include a reference to the specific paragraph/line in the source document | None |

### 2.3 Collaboration & Approval

| ID | Rule | Condition / Trigger | Expected Result | Exception |
|----|------|---------------------|-----------------|-----------|
| BR-11 | Approval status | All AI-generated findings | Default: Pending. Only Approved or Rejected by authorized users | None |
| BR-12 | Approval permission by role | User performs Approve/Reject | BA: approves Clarification Items; Tech Lead: approves technical Risks; PM: approves timeline Risks + all Suggestions | Admin can approve all |
| BR-13 | Only Approved → quotation | Quotation compilation | Only findings with Approved status are included in the WBS and Excel quotation | None |
| BR-14 | Edit AI results | User edits a finding | Save the original AI version, record the editor's identity + timestamp | None |

### 2.4 Estimation & Quotation

| ID | Rule | Condition / Trigger | Expected Result | Exception |
|----|------|---------------------|-----------------|-----------|
| BR-15 | Excel dynamic formulas | Export quotation file | All computed cells must be formulas (SUM, PRODUCT…), no hard-coded numbers | None |
| BR-16 | Mandatory Excel 4-tab structure | Export quotation file | Tab 1: Cover & Dashboard; Tab 2: Estimation Sheet (WBS); Tab 3: Rate Card & Cost; Tab 4: Assumptions & Exclusions | None |
| BR-17 | Automatic Risk Buffer | Effort calculation | Risk Buffer multiplier applied to Effort based on the ambiguity level of each feature (High gap → higher buffer) | None |
| BR-18 | Rate Card as the sole cost source | Cost calculation | Personnel costs must be calculated from the configured Rate Card, not entered directly into cells | None |
| BR-19 | Historical Matching | AI estimates effort | AI semantically matches against historical projects before producing a figure. Documents the reference source in the "Estimation Basis" column | If no similar project exists: explicitly note "No historical match" |
| BR-20 | WBS from Approved items only | WBS generation | WBS only contains features/modules that have been Approved in the Review step | None |

### 2.5 Security & Data

| ID | Rule | Condition / Trigger | Expected Result | Exception |
|----|------|---------------------|-----------------|-----------|
| BR-21 | Strict tenant isolation | All data queries | Users can only access data within their Organization | System Admin may have super-access with audit log |
| BR-22 | No data used for training | Document storage | Uploaded documents must not be sent to LLM endpoints that have a training-data retention policy | None |
| BR-23 | Encrypt documents at rest | Upload complete | Documents stored as AES-256 encrypted; decrypted only when processing is required | None |
| BR-24 | Users can only view assigned projects | Project access | RBAC enforced at the API layer, not just the UI | None |

### 2.6 Integration

| ID | Rule | Condition / Trigger | Expected Result | Exception |
|----|------|---------------------|-----------------|-----------|
| BR-25 | PM tools sync — Approved only | One-click sync to Jira/Linear/ClickUp | Only sync Tasks/Stories with Approved status; do not sync Pending or Rejected findings | None |
| BR-26 | Idempotent sync | Second sync attempt | Do not create duplicate items in the PM tool; update existing items | None |

---

## 3. Constraints & Validation

- File size: maximum 50MB/file
- Valid formats: PDF, DOCX, DOC, MD, TXT, XLSX, XLS, CSV
- Project name: required, must not be empty
- Rate Card: must have at least 1 role with a daily rate > 0 before a quotation can be exported
- Effort: must be a positive number; if AI cannot estimate → display "TBD" and require manual entry
- Valid finding status transitions: Pending → Approved or Pending → Rejected (not reversible after Approved/Rejected except by Admin)

---

## 4. Permissions & Authorization (Business)

| Permission | BA | PM | Presales | Tech Lead | QA/QC | Admin |
|------------|----|----|----------|-----------|-------|-------|
| Upload documents | ✓ | ✓ | ✓ | ✓ | — | ✓ |
| View analysis results | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Edit AI findings | ✓ | ✓ | — | ✓ | — | ✓ |
| Approve Clarification | ✓ | ✓ | — | — | — | ✓ |
| Approve technical Risks | — | ✓ | — | ✓ | — | ✓ |
| Approve Suggestions | — | ✓ | — | — | — | ✓ |
| Export Excel quotation | — | ✓ | ✓ | — | — | ✓ |
| Sync PM tools | — | ✓ | — | — | — | ✓ |
| Export Test Cases | ✓ | — | — | — | ✓ | ✓ |
| Configure Rate Card | — | — | — | — | — | ✓ |
| Manage users/org | — | — | — | — | — | ✓ |

---

## 5. Links

- PRD: `docs/planning/product/prd.md`
- Original specification: `docs/specs/requirement.md`
