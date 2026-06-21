# Architecture — AI ReqInsight & Estimator

> Output of Architect Agent — `.ai-factory/agents/architect-agent.md`
> Input: `docs/planning/product/prd.md`, `docs/specs/requirement.md`

---

## 1. Context

**Technical goals:**
- Process multi-format documents asynchronously, support ≥ 50 concurrent sessions
- AI analysis pipeline with pluggable LLM (no vendor lock-in)
- Multi-tenant with strict data isolation per-organization
- AES-256 encryption at-rest, TLS 1.3 in-transit

**Constraints:**
- NFR-04: Private LLM / Enterprise API — customer data must not be used for training
- NFR-06: Microservices + AI abstraction layer
- NFR-01: Analyze < 50 pages in ≤ 2 minutes

---

## 2. System Overview

### High-Level Diagram

```
┌──────────────────────────────────────────────────────────┐
│                      CLIENT LAYER                        │
│              Web Dashboard (SPA)                         │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTPS / TLS 1.3
┌───────────────────────▼─────────────────────────────────┐
│                    API GATEWAY                           │
│         Auth (JWT + RBAC) · Rate Limiting · Routing      │
└───┬───────────┬──────────────┬──────────────┬───────────┘
    │           │              │              │
┌───▼───┐  ┌───▼───┐    ┌─────▼────┐   ┌────▼──────┐
│Ingest │  │AI Core│    │Collabora-│   │Estimation │
│Service│  │Service│    │tion Svc  │   │Service    │
└───┬───┘  └───┬───┘    └─────┬────┘   └────┬──────┘
    │           │              │              │
┌───▼───────────▼──────────────▼──────────────▼──────────┐
│                    MESSAGE QUEUE (Async)                  │
│                    (File parsed events, AI job events)    │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│                    DATA LAYER                            │
│  PostgreSQL (multi-tenant)  │  Object Storage (encrypted)│
│  Redis (cache + queue)      │  Vector DB (embeddings)    │
└─────────────────────────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│                  AI ABSTRACTION LAYER                    │
│        Claude Enterprise / Azure OpenAI / Gemini          │
│              (pluggable — no vendor lock-in)             │
└─────────────────────────────────────────────────────────┘
```

### Bounded Context Boundaries

| Context | Service | Responsibility |
|---------|---------|----------------|
| `ingestion` | Ingestion Service | Upload, parse, OCR, chunk, store encrypted |
| `ai-core` | AI Core Service | Analysis, delta, persona, semantic matching |
| `collaboration` | Collaboration Service | Dashboard state, approval workflow, chatbot, citation |
| `estimation` | Estimation Service | WBS generation, effort calc, Excel export, PM sync |

---

## 3. Main Flows

### 3.1 Upload & Parse (Async)

```
Client → API Gateway → Ingestion Service
  → Validate (size, format)
  → Store encrypted (Object Storage)
  → OCR if PDF scan
  → Semantic chunking
  → Emit event: "document.parsed" → Message Queue
  → AI Core Service receives event → begins analysis
```

### 3.2 AI Analysis Pipeline

```
AI Core Service receives "document.parsed"
  → Load chunks from Object Storage
  → Call AI Abstraction Layer (LLM)
  → Parse response → create: Clarification Items, Risks, Gaps, Suggestions, Draft Test Cases
  → Store results in PostgreSQL (tenant-scoped)
  → Emit event: "analysis.completed"
  → Collaboration Service updates Dashboard state
```

### 3.3 Delta Analysis

```
User uploads v2 document, marked as update to project X
  → Ingestion Service parses v2
  → AI Core Service compares chunks v1 vs v2
  → Classify: Added / Removed / Modified
  → Update Risk/Gap report
  → Flag impact on current quotation
```

### 3.4 Approval & Export

```
User approves finding on Dashboard
  → Collaboration Service updates status → PostgreSQL
  → When Export is requested:
    → Estimation Service queries all Approved items
    → Fetch Rate Card
    → Calculate Effort × Risk Buffer × Rate
    → Generate Excel (4 tabs, dynamic formulas)
    → Return download link
```

### 3.5 PM Tools Sync

```
User clicks "Sync to Jira/Linear/ClickUp"
  → Estimation Service retrieves Approved WBS
  → Call PM Tool API (idempotent — check existing items first)
  → Create / Update items
  → Return sync result
```

---

## 4. Data Model

Details: `docs/planning/architecture/database-design.md`

**Main entities:**
- `Organization` — tenant root
- `Project` — document group for a single bid/project
- `Document` — uploaded file, metadata, encrypted storage reference
- `DocumentChunk` — text segment after chunking, used for analysis + citation
- `AnalysisResult` — AI result (type: gap/risk/clarification/suggestion/test-case)
- `ApprovalRecord` — approve/reject history for each AnalysisResult
- `WBSItem` — generated Epic/Story/Task
- `RateCard` — daily rates by role and seniority
- `User` — linked to Organization, has a Role

---

## 5. Security & Operations

**AuthN / AuthZ:**
- JWT with short expiry + refresh token
- RBAC at the API Gateway layer — not just the UI
- All DB queries have a mandatory `organization_id` filter (row-level security)

**Encryption:**
- Object Storage: AES-256 server-side encryption
- PostgreSQL: Transparent Data Encryption or field-level encryption for sensitive content
- Transport: TLS 1.3 throughout

**AI Data Privacy:**
- AI Abstraction Layer only calls LLM endpoints with a no-training commitment
- Do not log prompts/responses containing document content to standard log systems
- Separate audit log for AI calls (truncated — metadata only)

**Logging & Observability:**
- Structured logging (JSON), no PII / document content logged
- Distributed tracing (trace_id per request)
- Metrics: request rate, AI latency, queue depth, error rate

**Async & Queue:**
- Message queue for file processing jobs (recommended: Redis Streams or AWS SQS)
- Job timeout: 5 minutes; retry 3 times with exponential backoff
- Dead letter queue for failed jobs → alert

---

## 6. AI Abstraction Layer

**Design:**
```
interface LLMProvider {
  analyze(prompt: string, context: Chunk[]): Promise<AnalysisResponse>
  embed(text: string): Promise<number[]>
  chat(messages: Message[]): Promise<string>
}
```

**Implementations:**
- `ClaudeEnterpriseProvider` (preferred — Anthropic Enterprise contract)
- `AzureOpenAIProvider`
- `GeminiEnterpriseProvider`

Provider selected via config/env — not hardcoded in business logic.

---

## 7. Trade-offs & Decisions (ADR Summary)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Microservices vs Monolith | Microservices | NFR-06 requires it; each service scales independently (AI Core needs GPU/high compute, Ingestion needs I/O) |
| Sync vs Async processing | Async (queue) | File parsing + AI analysis can take > 30s; must not block HTTP request |
| PostgreSQL vs NoSQL | PostgreSQL | Multi-tenant RBAC, relational data (approval chains, WBS hierarchy); Row-Level Security built-in |
| Vector DB | Separate (pgvector or Qdrant) | Semantic matching FR-12 requires embedding search; decoupled from relational DB for independent scaling |
| LLM provider | Pluggable abstraction | NFR-06 + NFR-04; avoid vendor lock-in; easy to switch when pricing/policy changes |

---

## 8. Future Extensions

- **Historical Learning** (FR-12): After 6 months with sufficient data, train a fine-tuned model or build a RAG pipeline from project history
- **Mobile**: API-first design → add mobile client without backend changes
- **Webhook**: Real-time approval notifications → Slack/Teams integration
- **Self-hosted LLM**: Abstraction layer allows adding Ollama/vLLM provider for on-premise deployments
