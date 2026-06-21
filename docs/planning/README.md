# Planning (AI Factory artefacts)

Output của Product → Architect → Planner → Reviewer agents.

| Thư mục | Agent | Nội dung |
|---------|-------|----------|
| [product/](product/) | Product | PRD, business rules, success metrics |
| [architecture/](architecture/) | Architect | Kiến trúc, module map, DB, API |
| [plan/](plan/) | Planner | Epics, stories, tasks |
| [reviews/](reviews/) | Reviewer | Kết quả review PR |

Luồng: `docs/planning/product/` → `docs/planning/architecture/` → `docs/planning/plan/` → code/PR → `docs/planning/reviews/`.

Template khung: `.ai-factory/templates/`. Định nghĩa agent: `.ai-factory/agents/`.
