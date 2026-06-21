# Epic 04 — Estimation & Integration

> Planner Agent output — `.ai-factory/agents/planner-agent.md`

## Objective

The system automatically generates WBS, calculates effort and cost against the Rate Card, exports a 4-tab Excel file with dynamic formulas, and syncs to PM tools in one click.

## Links

- PRD: FR-11, FR-12, FR-13, FR-14
- Architecture: `estimation-service`
- DB: `wbs_items`, `rate_cards`, `rate_card_entries`
- Business Rules: BR-15 → BR-26

## Epic scope

Rate Card config → WBS generation → Effort + Risk Buffer calc → Excel export (4 tabs) → PM tools sync

## User stories

| ID | Description | Priority |
|----|-------------|----------|
| S-17 | As an Admin, I want to configure the Rate Card by role and seniority as the basis for cost calculation | P0 |
| S-18 | As a PM, I want the system to auto-generate WBS from Approved items to avoid manual entry | P0 |
| S-19 | As a Presales, I want to export a professional Excel quotation file with dynamic formulas to send to customers | P0 |
| S-20 | As a PM, I want to sync WBS to Jira/Linear/ClickUp in one click to save data entry time | P1 |
| S-21 | As a PM, I want AI to estimate effort based on historical projects for more accurate numbers | P2 |

## Epic completion criteria

- [ ] Rate Card CRUD working with at least these roles: Dev, QA, BA, PM (Junior/Mid/Senior)
- [ ] WBS generates correct Epic→Story→Task structure from Approved items
- [ ] Excel 4-tab with mandatory structure (BR-16), entirely dynamic formulas (BR-15)
- [ ] Risk Buffer automatically calculated by complexity level (BR-17)
- [ ] Jira/Linear sync is idempotent (BR-26)
- [ ] Tab 4 (Assumptions & Exclusions) auto-populated from Rejected items + Out-of-scope

## Dependencies & risks

- Dependency: EPIC-03 (Approved items must exist before generating WBS)
- Risk: PM Tool API schema changes → need adapter pattern per-tool
- Risk: Complex Excel formulas → requires thorough QA before release

## Milestone

Sprint 5-7
