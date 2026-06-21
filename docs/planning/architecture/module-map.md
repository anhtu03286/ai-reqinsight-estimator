# Module Map — AI ReqInsight & Estimator

> Output of Architect Agent — `.ai-factory/agents/architect-agent.md`

---

## 1. Overview

The system is divided into 6 main modules. 4 business modules (Ingestion, AI Core, Collaboration, Estimation) + 2 platform modules (API Gateway, Shared/Common).

---

## 2. Module List

| Module | Responsibility | Dependencies (in) | Dependencies (out) | Notes |
|--------|----------------|-------------------|--------------------|-------|
| **api-gateway** | Auth (JWT+RBAC), routing, rate limiting, TLS termination | Client requests | All services | Single entry point |
| **ingestion-service** | Upload validation, OCR, parsing, semantic chunking, encrypted storage | api-gateway | Message Queue, Object Storage, PostgreSQL | Async — emit events |
| **ai-core-service** | Analysis pipeline, delta analysis, persona mode, semantic matching, embedding | Message Queue, Object Storage | PostgreSQL, Vector DB, AI Abstraction Layer | CPU/GPU intensive |
| **collaboration-service** | Dashboard state, approval workflow (CRUD), AI chatbot proxy, deep-link citation | api-gateway, PostgreSQL | ai-core-service (chatbot), PostgreSQL | Stateless service |
| **estimation-service** | WBS generation, effort + cost calculation, Excel export, PM tools sync | api-gateway, PostgreSQL | Rate Card DB, PM Tools APIs (Jira/Linear/ClickUp) | I/O heavy during sync |
| **shared** | Auth middleware, tenant context, encryption utils, logger, error types | — | All services | Library — not deployed separately |

---

## 3. Boundaries & Coupling

**Communication rules:**

| From → To | Communication Method | Notes |
|-----------|---------------------|-------|
| Client → api-gateway | REST / HTTP (TLS 1.3) | Only entry point |
| api-gateway → services | REST internal or gRPC | Service-to-service within private network |
| ingestion-service → ai-core-service | Message Queue (async event) | No direct calls |
| collaboration-service → ai-core-service | REST (chatbot only — sync) | Only for real-time chat |
| ai-core-service → LLM | HTTP via AI Abstraction Layer | No other services call LLM directly |
| estimation-service → PM Tools | REST / OAuth (external API) | Via separate adapter per tool |

**Circular dependency rules (forbidden):**
- `ingestion-service` must not import `estimation-service`
- `ai-core-service` must not call `collaboration-service`
- `shared` must not import any service

---

## 4. Bounded Context

| Context | Ubiquitous Language | Module |
|---------|---------------------|--------|
| **Document Ingestion** | Document, Chunk, OCR, Parse, Upload, Project | ingestion-service |
| **AI Analysis** | AnalysisResult, Gap, Risk, Clarification, Suggestion, TestCase, Delta, Persona, Embedding | ai-core-service |
| **Collaboration** | Approval, Review, Status (Pending/Approved/Rejected), Citation, Thread, Comment | collaboration-service |
| **Estimation** | WBS, Epic, Story, Task, Effort, ManDay, RateCard, RiskBuffer, Quotation, Sync | estimation-service |

---

## 5. Links

- Overall architecture: `docs/planning/architecture/architecture.md`
- Database design: `docs/planning/architecture/database-design.md`
- API design: `docs/planning/architecture/api-design.md`
