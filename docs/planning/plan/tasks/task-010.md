# Task 010 — AI Abstraction Layer (LLM Provider Interface)

## Metadata
- **Epic:** EPIC-02 AI Core
- **Story:** S-05
- **Owner:** Backend Dev
- **Status:** Done ✓

## Goal

Implement the AI Abstraction Layer — a standard interface for LLM operations (analyze, embed, chat) with Claude Enterprise as the first implementation. Swapping providers requires only a config change.

## Files

- `src/ai/llm_interface.py`
- `src/ai/providers/claude_provider.py`
- `src/ai/providers/azure_openai_provider.py`
- `src/ai/ai_factory.py`
- `tests/test_ai_factory.py`

## Dependencies

- Task 001 (tech stack)

## Acceptance Criteria

- [x] Interface `LLMProvider` defines: `analyze()`, `embed()`, `chat()`
- [x] `ClaudeProvider` fully implements all 3 methods
- [x] `AzureOpenAIProvider` implements the interface (may throw NotImplemented for MVP)
- [x] `AIFactory.create()` reads `LLM_PROVIDER` env var → returns the correct implementation
- [x] API key read from env var, not hardcoded
- [x] Retry logic: 3 attempts with exponential backoff when LLM returns 5xx
- [x] Timeout: 60 seconds per request
- [x] 503 when LLM is unavailable → throws `AIUnavailableError`
- [x] Do not log prompt content (log metadata only: provider, latency, status)

## Tests Required

- Unit: factory returns correct provider based on env var
- Unit: retry logic with mock LLM returning 503 on attempt 1, 200 on attempt 2
- Unit: timeout after 60s
- Integration (with real API key in CI secrets): `embed("test")` → vector length 1536

## Notes

- Hard rule #11 AGENTS.md: must confirm Claude Enterprise contract has a no-training-data clause before using a production key
- Do not test with real API in unit tests — use mocks
