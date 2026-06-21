# Success Metrics — AI ReqInsight & Estimator

> Output of Product Agent — `.ai-factory/agents/product-agent.md`
> Reference: `docs/planning/product/prd.md`, `docs/specs/requirement.md`

---

## 1. Measurement Goals

- Shorten the time from receiving documents to having a draft quotation
- Improve quotation accuracy, reduce revisions after sending to clients
- Reduce the rate of Scope Creep in delivery projects
- Ensure the system operates stably, securely, and handles concurrent load

---

## 2. Metrics

### 2.1 System Performance

| ID | Metric | Definition | Baseline | Target | Measurement Frequency | Data Source |
|----|--------|------------|----------|--------|-----------------------|-------------|
| SM-01 | Document processing time < 50 pages | Time from upload completion to report ready | TBD (manual ~60-120 min) | ≤ 2 minutes (NFR-01) | Each processing run | Application logs |
| SM-02 | Concurrent sessions without degradation | Number of parallel processing sessions where response time does not increase > 20% | TBD | ≥ 50 sessions (NFR-02) | Periodic load test | Performance monitoring |
| SM-03 | System uptime | Percentage of time the system operates normally | TBD | ≥ 99.5% / month | Monthly | Uptime monitor |

### 2.2 AI Quality

| ID | Metric | Definition | Baseline | Target | Measurement Frequency | Data Source |
|----|--------|------------|----------|--------|-----------------------|-------------|
| SM-04 | Gap detection accuracy | % of Gaps AI detected that match BA/Tech Lead manual review | TBD | ≥ 80% | Monthly (sample review) | Manual audit |
| SM-05 | Risk false positive rate | % of Risks flagged by AI but Rejected by reviewers | TBD | ≤ 20% | Monthly | Approval workflow data |
| SM-06 | Effort estimation deviation | % deviation between AI-estimated Effort and actual Effort after project completion | TBD | ≤ 25% deviation | Per completed project | Project historical data |
| SM-07 | Historical match rate | % of features that AI matched against historical projects (not "No historical match") | TBD (0% at launch) | ≥ 60% after 6 months of operation | Monthly | AI analysis logs |

### 2.3 User Experience

| ID | Metric | Definition | Baseline | Target | Measurement Frequency | Data Source |
|----|--------|------------|----------|--------|-----------------------|-------------|
| SM-08 | Quotation acceptance rate without major edits | % of exported quotations accepted with fewer than 2 major revision rounds | TBD (manual ~50%) | ≥ 70% | Monthly | PM feedback |
| SM-09 | Average end-to-end process time | Time from upload to final quotation export | TBD | ≤ 2 hours (working time, excluding approval wait) | Weekly | Application logs |
| SM-10 | Adoption rate | % of the organization's new projects using the system instead of manual process | TBD (0% at launch) | ≥ 80% after 3 months | Monthly | Usage analytics |
| SM-11 | First-pass approval rate | % of AI findings Approved on first review (no editing required) | TBD | ≥ 65% | Monthly | Approval workflow data |

### 2.4 Business Impact

| ID | Metric | Definition | Baseline | Target | Measurement Frequency | Data Source |
|----|--------|------------|----------|--------|-----------------------|-------------|
| SM-12 | Pre-sales time reduction | % reduction in time BA/PM spends on analysis and quotation | TBD | ≥ 50% | Quarterly | Time tracking |
| SM-13 | Scope Creep reduction | % of projects with scope changes > 20% after contract signing | TBD | ≤ 15% (compared to before using the system) | Quarterly | Project retrospective |
| SM-14 | PM tools sync success rate | % of Jira/Linear/ClickUp syncs that complete without errors | TBD | ≥ 98% | Weekly | Integration logs |

---

## 3. Success / Failure Thresholds

**MVP launch — achieved when:**
- SM-01 ≤ 2 minutes (mandatory — NFR hard requirement)
- SM-02 ≥ 50 concurrent sessions (mandatory — NFR hard requirement)
- SM-04 ≥ 70% (minimum to trust AI results)
- SM-10 ≥ 50% adoption after the first month (signal that users see value)

**Needs adjustment when:**
- SM-05 (false positive) > 35% — AI is generating noise, prompt tuning required
- SM-06 (effort deviation) > 40% — more historical data or model adjustment needed
- SM-01 > 5 minutes consistently — serious performance issue

---

## 4. Assumptions & Measurement Limitations

- SM-06 (effort deviation) can only be measured after projects are completed → 3-12 month lag
- SM-07 (historical match) will be low in the first 3-6 months due to insufficient historical data
- SM-12, SM-13 require comparison against a pre-system baseline → need to collect manual data from 2-3 months before launch
- Some metrics (SM-04, SM-11) require manual sample audits → resource-intensive, require scheduled reviews

---

## 5. Links

- PRD: `docs/planning/product/prd.md`
- Business rules: `docs/planning/product/business-rules.md`
- Original specification: `docs/specs/requirement.md`
