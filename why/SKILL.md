---
name: why
description: >-
  Investigate the historical reasons for code, design choices, defensive behavior,
  or thresholds using cited evidence. Use when asking why a system has its current
  shape or which constraints a change must preserve. Not for inferring author
  intent from code alone or merely explaining runtime behavior.
---

# Why

Reconstruct decisions without inventing a tidy history. Read
[references/confidence.md](references/confidence.md) before synthesizing evidence.

## Investigate the decision

1. Identify the relevant symbols, behavior, and question. Treat the user's suggested
   reason as a hypothesis.
2. Inspect current code and tests, then trace substantive changes through history.
   Use bounded blame and log searches; follow renames when necessary. Distinguish
   introduction from later edits. Fetch linked reviews only through available tools.
3. Pursue the evidence appropriate to the question: reviews for implementation
   tradeoffs, issues for requirements, design documents for alternatives, incident
   records for defenses, or measurements for numeric thresholds. Search connected
   sources within scope; neither git nor external integrations are guaranteed.
4. Track dates, contradictions, and missing records. Stop when the answer is supported
   or additional accessible searches are unlikely to resolve the material gap.

Parallel investigation is optional when available and authorized. Each investigator
should return citations, findings, and search limits; the lead checks the synthesis.

## Present

Separate documented reasons, interpretations, and unknowns. Cite claims near their
evidence and report meaningful search gaps. Before a planned change, identify
constraints to preserve and assumptions to recheck today. Do not contact authors,
modify code, or expand the investigation without authorization.

Adapted from poteto's [pstack why](https://github.com/cursor/plugins/blob/main/pstack/skills/why/SKILL.md).
