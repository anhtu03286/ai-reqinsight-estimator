# Epic 03 — Collaboration & Review

> Planner Agent output — `.ai-factory/agents/planner-agent.md`

## Objective

The BA/PM/Tech Lead team can view AI results on the Dashboard, interact via chatbot, edit and approve each finding according to the workflow.

## Links

- PRD: FR-07, FR-08, FR-09, FR-10
- Architecture: `collaboration-service`, Web Dashboard
- DB: `analysis_results`, `approval_records`
- Business Rules: BR-11 → BR-14

## Epic scope

Dashboard → Interactive editing → Approval workflow → AI Chatbot → Deep-link citation

## User stories

| ID | Description | Priority |
|----|-------------|----------|
| S-11 | As a BA, I want to see all Gaps/Risks/Clarifications on the Dashboard to review everything | P0 |
| S-12 | As a PM, I want to Approve/Reject each finding to control quotation content | P0 |
| S-13 | As a BA, I want to click on a finding and see the original text in the document for cross-referencing | P0 |
| S-14 | As a BA, I want to edit AI finding content before approving | P1 |
| S-15 | As a Tech Lead, I want to chat with AI about the document to ask quick questions about content | P1 |
| S-16 | As a PM, I want to bulk approve multiple findings at once to save time | P2 |

## Epic completion criteria

- [ ] Dashboard displays all 5 result types with filter by type/status/severity
- [ ] Approval workflow follows roles correctly (BR-12)
- [ ] Deep-link navigates correctly to the source text in the document
- [ ] Edits save original AI version + record editor + timestamp (BR-14)
- [ ] AI chatbot responds with source chunk citations

## Dependencies & risks

- Dependency: EPIC-02 (analysis results must exist)
- Risk: Deep-link citation is complex for multi-page PDFs

## Milestone

Sprint 3-5
