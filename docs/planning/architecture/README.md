# Architecture

Directory containing **Architect Agent output** (Agent 02).

| File | Description |
|------|-------------|
| `architecture.md` | System overview, modules, bounded context, infrastructure |
| `module-map.md` | Module map, dependencies, boundaries |
| `database-design.md` | Data design: entities, relationships, indexes |
| `api-design.md` | API contract: resources, endpoints, request/response |

## When creating new files

- Agent definition: [architect-agent.md](../.ai-factory/agents/architect-agent.md)
- Input: `docs/planning/product/prd.md` (+ `docs/planning/product/business-rules.md`, `docs/planning/product/success-metrics.md` when needed)
- Templates: [architecture-template.md](../.ai-factory/templates/architecture-template.md), [module-map-template.md](../.ai-factory/templates/module-map-template.md), [database-design-template.md](../.ai-factory/templates/database-design-template.md), [api-design-template.md](../.ai-factory/templates/api-design-template.md)

The files above are generated when the Architect Agent runs — the original template leaves this directory empty (README only).
