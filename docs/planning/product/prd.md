# PRD — AI ReqInsight & Estimator

> Source of truth: `docs/specs/requirement.md` v1.1.0
> Output of Product Agent — `.ai-factory/agents/product-agent.md`

---

## 1. Summary

- **Problem:** The requirements analysis and quotation phase in software bidding is highly manual, prone to Scope Creep, and creates financial risk during delivery because client documents are often ambiguous, multi-format, and logically incomplete.
- **Proposed solution:** An AI platform that automatically reads and understands multi-format documents, extracts requirements, detects gaps/risks, and generates Excel quotations with dynamic formulas based on historical data.
- **Expected outcomes:** Shorten the pre-sales cycle, improve quotation accuracy, and protect the business from scope disputes with clients.

---

## 2. Users & Context

**Primary Actors:**

| Actor | Role | Business Permissions |
|-------|------|----------------------|
| **BA (Business Analyst)** | Analyze and clarify requirements | Upload documents, view/edit AI results, submit survey questions |
| **PM (Project Manager)** | Manage project and quotation | Approve results, export quotation, sync PM tools |
| **Presales** | Consulting and bidding | View quotation, export commercial files |
| **Tech Lead** | Technical evaluation | Approve architectural risks, propose tech stack |
| **QA/QC** | Testing | View and export draft test cases |
| **Admin** | System administration | Configure Rate Card, manage users/permissions |

**Usage context:** A software company during the bidding or new-project initiation phase, handling multiple sets of requirement documents from multiple clients simultaneously.

---

## 3. Scope

**In-scope for MVP:**

| Module | Description |
|--------|-------------|
| Ingestion & Parsing | Multi-format upload (PDF, DOCX, MD, TXT, XLSX, CSV), OCR, semantic chunking |
| AI Core & Delta Analysis | Requirements analysis, contradiction detection, version comparison (Delta), persona-based analysis |
| Collaboration & Review | Interactive dashboard, AI chatbot, approval workflow (Pending/Approved/Rejected), deep-link citation |
| Estimation & Integration | Automatic WBS, effort estimation, Rate Card, Excel 4-tab export, Jira/Linear/ClickUp sync |

**Out of scope:**
- Contract management after signing
- Project execution progress tracking
- Billing / invoicing
- Mobile app

---

## 4. Modules & Workflows

### 4.1 Main Business Flow (End-to-End)

```
[Upload documents] → [Parse & normalize] → [AI analysis] → [Review & approval] → [Export output]
```

**Step-by-step details:**

| Step | Actor | Action | Result |
|------|-------|--------|--------|
| 1. Intake | BA / PM | Upload document set (multi-file, drag-drop) | System processes async, notifies when done |
| 2. Analysis | AI Engine | Extract, classify by module, run Delta comparison if v2 exists | 5-component output report |
| 3. Review | BA, Tech Lead, PM | View results on Dashboard, ask AI chatbot, edit | Results edited + approved by role |
| 4. Approval | PM | Approve/Reject each AI finding | Transition state Pending → Approved/Rejected |
| 5. Export | Presales / PM | Export Excel quotation, Word survey questions, CSV test cases | Output files ready to send to client or sync PM tools |

### 4.2 Delta Analysis Workflow

When uploading v2 document:
1. System identifies the document as an update to an existing project
2. AI compares and extracts Added / Removed / Changed scope
3. Warns about impact on the current quotation
4. BA/PM confirms scope changes before updating the quotation

### 4.3 Approval Workflow

```
AI generates finding → Pending → BA/Tech Lead/PM reviews → Approved or Rejected
```
- Each finding (Gap, Risk, Suggestion) has its own status
- Only Approved findings are included in the final quotation

---

## 5. System Output (5 Components)

| # | Component | Content | Format |
|---|-----------|---------|--------|
| 1 | Clarification Items | Ambiguous sentences/requirements, missing KPIs, broken flows | Web table + Word export |
| 2 | Risks & Gaps | Gaps (missing mandatory features) + Risks (technical, timeline, security) classified High/Medium/Low | Color-coded Red/Yellow/Green |
| 3 | Suggestions & Exclusions | Technical solutions, Best Practices, automatic Out of Scope list | Alongside Risk/Gap |
| 4 | Draft Test Cases | Happy Path + Edge Cases per feature | Separate tab + CSV/Excel export |
| 5 | AI-Driven Quotation | WBS (Epic→Story→Task), Effort (Man-day), Risk Buffer, cost per Rate Card | Excel 4-tab with dynamic formulas |

---

## 6. Business Rules

See details: `docs/planning/product/business-rules.md`

Summary:
- Maximum 50MB/file; supports PDF (scan + text), DOCX, MD, TXT, XLSX, CSV
- Risk classified at 3 levels: High (red) / Medium (yellow) / Low (green)
- Approval states: Pending → Approved / Rejected
- Excel output must have dynamic formulas, no hard-coded numbers
- Data isolation: each Organization is an independent tenant
- LLM must not use customer data as training data

---

## 7. Success Metrics

See details: `docs/planning/product/success-metrics.md`

Summary:
- Document analysis time for < 50 pages: ≤ 2 minutes (NFR-01)
- Support ≥ 50 concurrent processing sessions (NFR-02)
- Gap/Risk detection accuracy ≥ 80% compared to manual review
- Quotation acceptance rate without major edits after export ≥ 70%

---

## 8. Non-Functional Requirements (Summary)

| NFR | Requirement |
|-----|-------------|
| NFR-01 | Analyze documents < 50 pages in ≤ 2 minutes |
| NFR-02 | ≥ 50 concurrent sessions without performance degradation |
| NFR-03 | AES-256 at-rest; TLS 1.3 in-transit |
| NFR-04 | Data isolation per-org; must not be used as LLM training data |
| NFR-05 | RBAC — users can only view projects they are assigned to |
| NFR-06 | Microservices + AI abstraction layer; LLM pluggable |
| NFR-07 | Smart dashboard filters, friendly for non-technical users |

---

## 9. Risks & Assumptions

**Risks:**
- Low OCR accuracy with poor-quality scanned documents → manual review fallback required
- LLM hallucination generating incorrect Gap/Risk → mandatory approval workflow required
- Client documents may contain sensitive content → strict data isolation required
- Jira/Linear/ClickUp integration depends on third-party APIs that may change

**Assumptions:**
- Users have stable internet connectivity to upload files
- Organizations already have Jira/Linear/ClickUp accounts if they want to sync
- Selected LLM provider has an Enterprise contract with data privacy commitments

---

## 10. Approval

- Owner: TBD
- Stakeholders: BA, PM, Presales, Tech Lead, QA/QC
