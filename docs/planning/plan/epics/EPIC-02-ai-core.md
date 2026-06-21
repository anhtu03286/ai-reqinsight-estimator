# Epic 02 — AI Core & Delta Analysis

> Planner Agent output — `.ai-factory/agents/planner-agent.md`

## Objective

AI automatically analyzes parsed documents, produces 5 result types (Clarification, Risk, Gap, Suggestion, Test Case), and supports Delta comparison between document versions.

## Links

- PRD: FR-04, FR-05, FR-06
- Architecture: `ai-core-service`, AI Abstraction Layer
- DB: `document_chunks`, `analysis_results`

## Epic scope

AI Abstraction Layer → Analysis pipeline → Delta analysis → Persona mode → Semantic matching (FR-12)

## User stories

| ID | Description | Priority |
|----|-------------|----------|
| S-05 | As a system, I want an AI Abstraction Layer so that switching LLM providers does not affect business logic | P0 |
| S-06 | As a BA, I want AI to automatically detect Gaps and Risks so that no scope is missed | P0 |
| S-07 | As a BA, I want AI to detect contradictions between files to clarify with the customer | P1 |
| S-08 | As a Tech Lead, I want to run analysis from a Tech Lead perspective to find architecture risks | P1 |
| S-09 | As a PM, I want to upload v2 documents and immediately see what changed to update the quotation | P1 |
| S-10 | As a system, I want semantic matching with historical projects to estimate effort accurately | P2 |

## Epic completion criteria

- [ ] LLM Abstraction Layer working with at least 1 provider (Claude Enterprise)
- [ ] Analysis produces all 5 result types (clarification, risk, gap, suggestion, test_case)
- [ ] Each result has a deep-link to its source chunk
- [ ] Delta analysis correctly classifies Added/Removed/Modified
- [ ] Persona mode working for BA, Tech Lead, QA
- [ ] Analysis of < 50 pages completes in ≤ 2 minutes (NFR-01)

## Dependencies & risks

- Dependency: EPIC-01 (chunks must exist first)
- Risk: LLM hallucination → requires prompt engineering + approval workflow
- Risk: LLM API latency → requires async + timeout handling

## Milestone

Sprint 2-4
