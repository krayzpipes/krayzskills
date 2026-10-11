---
name: interrogate
description: >-
  Perform an adversarial review of a diff or design, investigate candidate defects,
  and return a prioritized verdict. Use when asked to challenge a change, find blind
  spots, or conduct independent reviews. Review does not authorize applying fixes.
---

# Interrogate

Challenge the implementation against its actual goal. Seek reachable defects,
then exercise lead judgment instead of forwarding every criticism.

## Prepare and review

Establish the intended behavior, exact review scope, comparison base, and relevant
constraints. Include callers, contracts, and tests needed to understand the change.
Read [references/review-guide.md](references/review-guide.md) for the review criteria.

For consequential changes, independent reviewers can help when available and
authorized. Give each the same intent and artifacts without feeding them earlier
conclusions. Model diversity can add perspective but is not required. Do not claim
independent review when only one pass occurred; a focused single review remains useful.

## Judge findings

Check candidate defects against real call paths and scope. Use bounded local
diagnostics where useful. Merge duplicates, resolve disagreements, and retain a
strong isolated finding even when other reviewers missed it. Agreement is a lead
to investigate, not proof.

Classify findings as actionable defects, worthwhile tradeoffs, useful context,
or rejected claims. Give locations, triggers, impact, evidence, and a brief rationale.
Keep uncertain risks explicitly uncertain. Report coverage limits; absence of
findings is not a correctness guarantee. Leave implementation untouched unless
the user also requested changes.

Adapted from poteto's [pstack interrogate](https://github.com/cursor/plugins/blob/main/pstack/skills/interrogate/SKILL.md).
