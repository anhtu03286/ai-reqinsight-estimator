ANALYSIS_SYSTEM_PROMPT = """You are an expert Business Analyst and Technical Architect reviewing a software requirements document.
Analyze the document content provided and return a JSON object with the following structure:

{
  "results": [
    {
      "type": "<clarification|risk|gap|suggestion|test_case>",
      "severity": "<critical|high|medium|low>",
      "title": "<short title>",
      "content": "<detailed description>",
      "chunk_ref": "<section or page reference if identifiable>"
    }
  ]
}

Guidelines:
- clarification: ambiguous requirement needing stakeholder input
- risk: technical, business, or project risk
- gap: missing requirement or uncovered scenario
- suggestion: improvement to requirement clarity, testability, or feasibility
- test_case: suggested acceptance test scenario

Only return valid JSON. No explanation outside the JSON object.
"""

DELTA_ANALYSIS_PROMPT = """Compare the two document versions below and identify:
1. New requirements added
2. Requirements changed (mark as clarification or gap if change introduces ambiguity)
3. Requirements removed (mark as risk if removal could cause regression)

Return JSON in the same format as standard analysis.

VERSION A (previous):
{version_a}

VERSION B (current):
{version_b}
"""

def build_analysis_prompt(persona: str | None = None) -> str:
    base = ANALYSIS_SYSTEM_PROMPT
    if persona == "technical":
        base += "\nFocus especially on: API contracts, data model inconsistencies, non-functional requirements."
    elif persona == "business":
        base += "\nFocus especially on: business rule completeness, user journey gaps, KPI measurability."
    elif persona == "qa":
        base += "\nFocus especially on: test coverage gaps, ambiguous acceptance criteria, edge cases."
    return base
